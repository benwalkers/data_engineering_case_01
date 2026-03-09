from __future__ import annotations
import json
from typing import Any
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from pii_session_tokenisation import tokenise_session_id

class ParseJson(beam.DoFn):
    def process(self, element: bytes):
        payload = element.decode("utf-8") if isinstance(element, (bytes, bytearray)) else element
        yield json.loads(payload)

class ValidateModules(beam.DoFn):
    VALID_TAG = "valid"
    DQ_TAG = "dq"

    def process(self, row: dict[str, Any]):
        dq_flags = []
        session_id = str(row.get("session_id") or "").strip()
        views = row.get("views")
        clicks = row.get("clicks")
        view_time = row.get("view_time")
        if not session_id:
            dq_flags.append("MISSING_SESSION_ID")
        try:
            if views is not None and clicks is not None and int(clicks) > int(views):
                dq_flags.append("CLICK_GT_VIEWS")
        except Exception:
            dq_flags.append("CLICK_GT_VIEWS")
        try:
            if views is not None and view_time is not None and int(views) > 0 and int(view_time) == 0:
                dq_flags.append("VIEWS_GT_0_WITH_VIEW_TIME_0")
        except Exception:
            pass
        out = dict(row)
        out["session_token"] = tokenise_session_id(session_id)
        out.pop("session_id", None)
        out["dq_flags"] = dq_flags
        out["severity"] = "BLOCKING" if any(f in dq_flags for f in ["MISSING_SESSION_ID", "CLICK_GT_VIEWS"]) else ("WARNING" if dq_flags else None)
        tag = self.DQ_TAG if dq_flags else self.VALID_TAG
        yield beam.pvalue.TaggedOutput(tag, out)

def run(argv=None):
    options = PipelineOptions(argv)
    options.view_as(StandardOptions).streaming = True
    with beam.Pipeline(options=options) as p:
        rows = (
            p
            | "ReadPubSub" >> beam.io.ReadFromPubSub(topic="projects/PROJECT/topics/flixmedia-events")
            | "ParseJson" >> beam.ParDo(ParseJson())
        )
        _ = rows | "WriteRawArchive" >> beam.io.WriteToText("gs://BUCKET/raw/events", file_name_suffix=".jsonl")
        validated = rows | "ValidateModules" >> beam.ParDo(ValidateModules()).with_outputs(ValidateModules.VALID_TAG, ValidateModules.DQ_TAG)
        valid_rows = validated[ValidateModules.VALID_TAG]
        dq_rows = validated[ValidateModules.DQ_TAG]
        _ = valid_rows | "WriteCurated" >> beam.io.WriteToText("gs://BUCKET/curated/modules_curated", file_name_suffix=".jsonl")
        _ = dq_rows | "WriteDQ" >> beam.io.WriteToText("gs://BUCKET/dq/modules_dq", file_name_suffix=".jsonl")
        _ = dq_rows | "WriteSanitisedArchive" >> beam.io.WriteToText("gs://BUCKET/archive/failed_events", file_name_suffix=".jsonl")

if __name__ == "__main__":
    run()

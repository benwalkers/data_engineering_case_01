#!/usr/bin/env python3
from __future__ import annotations
import argparse, pathlib, sys, yaml

REQUIRED_TOP_LEVEL = {"contract_name","version","source","target","fields","rules"}
REQUIRED_FIELD_KEYS = {"name","type","required"}
REQUIRED_RULE_KEYS = {"id","severity","expression"}

def validate_contract(path: pathlib.Path) -> list[str]:
    errors = []
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        return [f"{path}: root must be a mapping"]
    missing = REQUIRED_TOP_LEVEL - set(data.keys())
    if missing:
        errors.append(f"{path}: missing top-level keys: {sorted(missing)}")
    for idx, field in enumerate(data.get("fields", [])):
        if not isinstance(field, dict):
            errors.append(f"{path}: field[{idx}] must be a mapping")
            continue
        miss = REQUIRED_FIELD_KEYS - set(field.keys())
        if miss:
            errors.append(f"{path}: field[{idx}] missing keys: {sorted(miss)}")
    for idx, rule in enumerate(data.get("rules", [])):
        if not isinstance(rule, dict):
            errors.append(f"{path}: rule[{idx}] must be a mapping")
            continue
        miss = REQUIRED_RULE_KEYS - set(rule.keys())
        if miss:
            errors.append(f"{path}: rule[{idx}] missing keys: {sorted(miss)}")
    return errors

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contracts-dir", default=str(pathlib.Path(__file__).resolve().parents[1] / "contracts"))
    args = ap.parse_args()
    cdir = pathlib.Path(args.contracts_dir)
    files = sorted(cdir.glob("*.yaml"))
    if not files:
        print("No contract files found.", file=sys.stderr)
        return 2
    errors = []
    for f in files:
        errors.extend(validate_contract(f))
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print(f"Validated {len(files)} contracts successfully.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

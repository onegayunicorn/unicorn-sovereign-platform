"""Schema validation tests."""
import json, os, sys

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")

def test_all_schemas_valid_json():
    for f in os.listdir(SCHEMA_DIR):
        if f.endswith(".json"):
            with open(os.path.join(SCHEMA_DIR, f)) as fh:
                data = json.load(fh)
            assert "$schema" in data or "properties" in data

def test_evidence_manifest_required_fields():
    with open(os.path.join(SCHEMA_DIR, "evidence_manifest.schema.json")) as f:
        s = json.load(f)
    required = set(s["required"])
    expected = {"experiment_id","node_ids","source_format","circuit_checksum",
                "backend","shots","classification","result_artifact_uri",
                "independent_review_status"}
    assert expected.issubset(required)

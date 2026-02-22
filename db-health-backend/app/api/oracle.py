from fastapi import APIRouter, UploadFile, File
from typing import List

from app.engines.oracle.structured_parser import parse_structured_awr
from app.engines.oracle.normalizer import (
    normalize_top_events,
    normalize_wait_classes,
    normalize_load_profile,
    normalize_efficiency
)

from app.services.awr_metadata_extractor import extract_awr_metadata
from app.services.awr_validator import validate_cluster

router = APIRouter()


# -------------------------------------------------
# ✅ Single File Oracle Analysis (Structured + Normalized)
# -------------------------------------------------
@router.post("/oracle")
async def analyze_oracle(file: UploadFile = File(...)):

    content = await file.read()
    text = content.decode(errors="ignore")

    # Step 1: Structured Parsing
    structured = parse_structured_awr(text)

    # Step 2: Numeric Normalization
    structured["top_events"] = normalize_top_events(structured.get("top_events", []))
    structured["wait_classes"] = normalize_wait_classes(structured.get("wait_classes", {}))
    structured["load_profile"] = normalize_load_profile(structured.get("load_profile", {}))
    structured["instance_efficiency"] = normalize_efficiency(structured.get("instance_efficiency", {}))

    return structured


# -------------------------------------------------
# 🚀 Enterprise Multi-File Oracle Analysis (Cluster Validation)
# -------------------------------------------------
@router.post("/oracle/multi")
async def analyze_oracle_multi(files: List[UploadFile] = File(...)):

    metadata_list = []
    texts = []

    for file in files:
        content = await file.read()
        text = content.decode(errors="ignore")
        texts.append(text)

        metadata = extract_awr_metadata(text)
        metadata_list.append(metadata)

    validation = validate_cluster(metadata_list)

    if validation["status"] == "rejected":
        return validation

    return {
        "status": "accepted",
        "files_uploaded": len(files),
        "metadata": [m.dict() for m in metadata_list]
    }

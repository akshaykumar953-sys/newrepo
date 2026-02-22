from datetime import timedelta
from typing import List, Dict
from app.models.awr_metadata import AwrMetadata


SEVEN_DAYS = timedelta(days=7)


def validate_cluster(metadata_list: List[AwrMetadata]) -> Dict:
    if not metadata_list:
        return {"status": "rejected", "reason": "No files uploaded"}

    base = metadata_list[0]

    for meta in metadata_list[1:]:

        # DBID check
        if meta.dbid != base.dbid:
            return {
                "status": "rejected",
                "reason": "DBID_MISMATCH",
                "message": "Uploaded AWR reports belong to different databases."
            }

        # Unique name check
        if meta.unique_name != base.unique_name:
            return {
                "status": "rejected",
                "reason": "UNIQUE_NAME_MISMATCH",
                "message": "Reports belong to different clusters."
            }

        # Snapshot window check (7-day tolerance)
        if abs(meta.begin_time - base.begin_time) > SEVEN_DAYS or \
           abs(meta.end_time - base.end_time) > SEVEN_DAYS:
            return {
                "status": "rejected",
                "reason": "SNAPSHOT_WINDOW_MISMATCH",
                "message": "Snapshot windows differ by more than 7 days."
            }

    # Duplicate instance check
    instance_numbers = [
        m.instance_number for m in metadata_list if m.instance_number is not None
    ]
    if len(instance_numbers) != len(set(instance_numbers)):
        return {
            "status": "rejected",
            "reason": "DUPLICATE_INSTANCE",
            "message": "Duplicate instance reports detected."
        }

    return {
        "status": "accepted",
        "message": "Cluster validation successful."
    }

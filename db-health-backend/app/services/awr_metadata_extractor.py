import re
from datetime import datetime
from app.models.awr_metadata import AwrMetadata


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%d-%b-%y %H:%M:%S")


def extract_awr_metadata(content: str) -> AwrMetadata:
    # DBID
    dbid_match = re.search(r"<td align=\"right\" class='awrnc'>(\d+)</td>", content)
    dbid = dbid_match.group(1) if dbid_match else None

    # DB Name
    dbname_match = re.search(r"<td scope=\"row\" class='awrnc'>(\w+)</td>", content)
    db_name = dbname_match.group(1) if dbname_match else None

    # Unique Name
    unique_match = re.search(r"<td class='awrnc'>(\w+_?\w+)</td><td class='awrnc'>PRIMARY", content)
    unique_name = unique_match.group(1) if unique_match else None

    # RAC detection
    rac = "RAC</th>" in content and "YES</td>" in content

    # Instance Name
    inst_match = re.search(r"<td scope=\"row\" class='awrnc'>(\w+)</td><td align=\"right\" class='awrnc'>(\d+)</td>", content)
    instance_name = None
    instance_number = None
    if inst_match:
        instance_name = inst_match.group(1)
        instance_number = int(inst_match.group(2))

    # Snapshot times
    begin_match = re.search(r"Begin Snap:</td><td align=\"right\" class='awrnc'>\d+</td><td align=\"center\" class='awrnc'>(.*?)</td>", content)
    end_match = re.search(r"End Snap:</td><td align=\"right\" class='awrc'>\d+</td><td align=\"center\" class='awrc'>(.*?)</td>", content)

    begin_time = parse_datetime(begin_match.group(1)) if begin_match else None
    end_time = parse_datetime(end_match.group(1)) if end_match else None

    # Detect Global AWR
    is_global = "RAC Report Summary" in content

    return AwrMetadata(
        dbid=dbid,
        db_name=db_name,
        unique_name=unique_name,
        rac=rac,
        instance_name=instance_name,
        instance_number=instance_number,
        begin_time=begin_time,
        end_time=end_time,
        is_global=is_global,
    )

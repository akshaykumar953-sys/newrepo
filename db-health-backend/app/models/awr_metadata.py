from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AwrMetadata(BaseModel):
    dbid: str
    db_name: str
    unique_name: str
    rac: bool
    instance_name: Optional[str]
    instance_number: Optional[int]
    begin_time: datetime
    end_time: datetime
    is_global: bool

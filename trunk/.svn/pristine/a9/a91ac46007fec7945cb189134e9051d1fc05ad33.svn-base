from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class VersionInfo:
    id: str
    version_number: str
    version_name: str
    release_date: datetime
    description: str
    status: str
    build_number: str
    changelog: str
    author: str


class VersionInfoRepository:
    def __init__(self):
        self._versions: Dict[str, VersionInfo] = {}

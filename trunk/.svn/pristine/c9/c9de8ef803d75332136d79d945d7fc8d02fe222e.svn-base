from dataclasses import dataclass
from typing import Any, Optional


class Events:
    USER_PROFILE_UPDATED = "user_profile_updated"
    USER_INFO_CHANGED = "user_info_changed"
    STATUS_BAR = "status_bar"


@dataclass
class EventData:
    event_type: str
    data: Optional[Any] = None
    source: Optional[str] = None

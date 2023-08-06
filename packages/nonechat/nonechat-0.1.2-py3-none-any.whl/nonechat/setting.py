from typing import Optional
from dataclasses import dataclass

from textual.color import Color


@dataclass
class ConsoleSetting:
    title: str = "Console"
    sub_title: str = "powered by Textual"
    room_title: str = "Chat"
    title_color: Optional[Color] = None
    icon: Optional[str] = None
    icon_color: Optional[Color] = None
    bg_color: Optional[Color] = None
    header_color: Optional[Color] = None

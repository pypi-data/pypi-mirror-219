"""
info
===============================================================================
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import defcon

if TYPE_CHECKING:
    from ufoLib2.objects.info import Info as UFOlib2_Info
    from .font import Font

class Info(defcon.Info):

    def __init__(self, font:Optional[Font]=None):
        super().__init__(font)
        self._openTypeHeadFlags = []
        self._openTypeOS2Selection = []
        self._openTypeOS2Type = []
        self._openTypeOS2CodePageRanges = []
        self._openTypeOS2UnicodeRanges = []

    @classmethod
    def fromUFOlib2_Info(cls, font:Font, ufolib2_info:UFOlib2_Info) -> Info:
        info = cls(font)
        info.disableNotifications()
        for name in info._properties:
            if hasattr(ufolib2_info, name):
                value = getattr(ufolib2_info, name)
                if value:
                    setattr(info, name, value)
        info.dirty = True
        info.enableNotifications()
        return info


"""This module provides utilities for streaming lambda logs."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import os
from typing import Dict, Final, Iterable, TypeVar

from .streaming import AtmResultStreamer

LOG_LEVELS: Final[Dict[str, int]] = {
    "debug": 7,
    "info": 6,
    "notice": 5,
    "warning": 4,
    "error": 3,
    "critical": 2,
    "alert": 1,
    "emergency": 0,
}

DEFAULT_LOG_LEVEL: Final[str] = "info"


def normalize_severity(severity: str) -> str:
    return severity if severity in LOG_LEVELS else DEFAULT_LOG_LEVEL


def get_log_level() -> str:
    try:
        return normalize_severity(os.environ["ATM_LOG_LEVEL"])
    except:
        return DEFAULT_LOG_LEVEL


T = TypeVar("T")


class AtmLogger(AtmResultStreamer[T]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def stream_items(self, items: Iterable[T]) -> None:
        log_level_int = LOG_LEVELS[get_log_level()]

        super().stream_items(
            [
                item
                for item in items
                if LOG_LEVELS[self._get_item_severity(item)] <= log_level_int
            ]
        )

    @staticmethod
    def _get_item_severity(item: T) -> str:
        try:
            return normalize_severity(item["severity"])
        except:
            return DEFAULT_LOG_LEVEL

    def stream_log(self, severity, log_content):
        self.stream_item(
            {
                "severity": severity,
                "content": log_content,
            }
        )

    def debug(self, log_content):
        self.stream_log("debug", log_content)

    def info(self, log_content):
        self.stream_log("info", log_content)

    def notice(self, log_content):
        self.stream_log("notice", log_content)

    def warning(self, log_content):
        self.stream_log("warning", log_content)

    def error(self, log_content):
        self.stream_log("error", log_content)

    def critical(self, log_content):
        self.stream_log("critical", log_content)

    def alert(self, log_content):
        self.stream_log("alert", log_content)

    def emergency(self, log_content):
        self.stream_log("emergency", log_content)

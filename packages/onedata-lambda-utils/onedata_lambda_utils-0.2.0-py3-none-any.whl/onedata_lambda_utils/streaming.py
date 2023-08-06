"""This module provides utilities for streaming lambda results."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import json
from contextlib import nullcontext
from threading import Lock
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class AtmResultStreamer(Generic[T]):
    def __init__(self, *, result_name: str, synchronized: bool) -> None:
        """Inits AtmResultStreamer.

        Args:
            result_name:
                The name of result.
            synchronized:
                The flag telling whether streaming should be thread-safe or not.
        """
        self.result_name = result_name
        self._synchronized_context = Lock() if synchronized else nullcontext()

        super().__init__()

    def stream_item(self, item: T) -> None:
        self.stream_items([item])

    def stream_items(self, items: Iterable[T]) -> None:
        if not items:
            return

        with self._synchronized_context, open(f"/out/{self.result_name}", "a") as f:
            for item in items:
                json.dump(item, f)
                f.write("\n")

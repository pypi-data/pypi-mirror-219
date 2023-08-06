"""This module provides utilities for building time series measurements."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time
from typing import Optional

from .types import AtmTimeSeriesMeasurement


class AtmTimeSeriesMeasurementBuilder:
    """Base class for time series measurement builders.

    In order to create a builder for concrete time series measurement, create 
    a class deriving from AtmTimeSeriesMeasurementBuilder with following 
    metadata specified:
    - ts_name - used as exact name of the measurement
    - unit - stored only as metadata and not processed in any way

    Example usage:
    >>>
    >>> import pprint
    >>>
    >>> from onedata_lambda_utils.stats import AtmTimeSeriesMeasurementBuilder
    >>>
    >>>
    >>> class FilesProcessed(
    >>>     AtmTimeSeriesMeasurementBuilder, ts_name="filesProcessed", unit=None
    >>> ):
    >>>     pass
    >>>
    >>>
    >>> pprint.pprint(FilesProcessed.build(value=34, timestamp=100))

         {'timestamp': 100, 'tsName': 'filesProcessed', 'value': 34}
    """

    def __init_subclass__(cls, ts_name: str, unit: Optional[str]) -> None:
        cls._ts_name = ts_name
        cls._unit = unit

    @classmethod
    def build(
        cls, value: float, *, timestamp: Optional[int] = None
    ) -> AtmTimeSeriesMeasurement:
        return {
            "tsName": cls._ts_name,
            "timestamp": int(time.time()) if timestamp is None else timestamp,
            "value": value,
        }

#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, Optional, Union

from typing_extensions import TypedDict


class TimeSeriesPredictParams(TypedDict):
    """Typed dict for time series predict parameters"""

    forecastPoint: Optional[str]
    predictionsStartDate: Optional[str]
    predictionsEndDate: Optional[str]
    type: Optional[str]
    relaxKnownInAdvanceFeaturesCheck: Optional[bool]


class AutopilotModelType:
    """Type for type checking if an AutopilotModel"""

    def set_params(self, **kwargs: Any) -> AutopilotModelType:
        raise NotImplementedError()

    def get_params(self) -> Union[Dict[Any, Any], Any]:
        raise NotImplementedError()

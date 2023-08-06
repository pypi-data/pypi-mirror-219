# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

from typing import Any, Dict, Optional

from comet_mpm.constants import (
    EVENT_FEATURES,
    EVENT_PREDICTION,
    EVENT_PREDICTION_PROBABILITY,
    EVENT_PREDICTION_VALUE,
)
from comet_mpm.events.base_event import BaseEvent


class PredictionEvent(BaseEvent):
    """
    This class represents a single prediction event. Events are identified by the
    mandatory prediction_id parameter. Many events can have the same
    prediction_id. The MPM backend merges events with the same prediction_id
    automatically.
    Args:
        workspace: The project workspace.
        model_name: The name of model
        model_version: The version of model
        prediction_id: The unique prediction ID, could be provided by the
            framework, you or a random unique value could be provided like
            str(uuid4())
        input_features: If provided must be a flat Dictionary where the
            keys are the feature name and the value are native Python
            scalars, int, floats, booleans or strings. For example:
            `{“age”: 42, “income”: 42894.89}`
        output_value: The prediction as a native Python scalar, int,
            float, boolean or string.
        output_probability: If provided, must be a float between 0 and 1
            indicating the confidence of the model in the prediction
    """

    def __init__(
        self,
        workspace: str,
        model_name: str,
        model_version: str,
        prediction_id: str,
        input_features: Optional[Dict[str, Any]] = None,
        output_value: Any = None,
        output_probability: Optional[float] = None,
        timestamp: Optional[float] = None,
    ):
        super(PredictionEvent, self).__init__(
            workspace=workspace,
            model_name=model_name,
            model_version=model_version,
            prediction_id=prediction_id,
            timestamp=timestamp,
        )
        self.input_features = input_features
        self.output_value = output_value
        self.output_probability = output_probability

    def _get_event_dict(self) -> Dict[str, Any]:
        prediction: Dict[str, Any] = {}
        if self.output_value is not None:
            prediction[EVENT_PREDICTION_VALUE] = self.output_value
        if self.output_probability is not None:
            prediction[EVENT_PREDICTION_PROBABILITY] = self.output_probability

        event: Dict[str, Any] = {}
        if self.input_features is not None:
            event[EVENT_FEATURES] = self.input_features

        if prediction:
            event[EVENT_PREDICTION] = prediction

        return event

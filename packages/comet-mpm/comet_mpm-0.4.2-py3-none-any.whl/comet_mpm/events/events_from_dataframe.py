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
from typing import List, Optional

from .prediction_event import PredictionEvent


def generate(  # type: ignore[no-untyped-def]
    workspace: str,
    model_name: str,
    model_version: str,
    dataframe,
    prediction_id_column: str,
    feature_columns: Optional[List[str]] = None,
    output_value_column: Optional[str] = None,
    output_probability_column: Optional[str] = None,
    timestamp_column: Optional[str] = None,
):
    return (
        _event(
            workspace=workspace,
            model_name=model_name,
            model_version=model_version,
            row=row,
            prediction_id_column=prediction_id_column,
            feature_columns=feature_columns,
            output_value_column=output_value_column,
            output_probability_column=output_probability_column,
            timestamp_column=timestamp_column,
        )
        for row in dataframe.to_dict(orient="records")
    )


def _event(  # type: ignore[no-untyped-def]
    workspace: str,
    model_name: str,
    model_version: str,
    row,
    prediction_id_column,
    feature_columns,
    output_value_column,
    output_probability_column,
    timestamp_column: Optional[str] = None,
) -> PredictionEvent:
    prediction_id = str(row[prediction_id_column])
    input_features = None
    if feature_columns is not None:
        input_features = {key: row[key] for key in feature_columns}

    output_value = None
    if output_value_column is not None:
        output_value = row[output_value_column]

    output_probability = None
    if output_probability_column is not None:
        output_probability = row[output_probability_column]

    timestamp = None
    if timestamp_column is not None:
        timestamp = row[timestamp_column]

    return PredictionEvent(
        workspace=workspace,
        model_name=model_name,
        model_version=model_version,
        prediction_id=prediction_id,
        input_features=input_features,
        output_value=output_value,
        output_probability=output_probability,
        timestamp=timestamp,
    )

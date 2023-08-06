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

import asyncio as asyncio_module
import atexit
import os
from typing import Any, Awaitable, Dict, Iterable, List, Optional, Union

from . import optional_update
from .connection import MPM_BASE_PATH, REST_API_BASE_PATH, sanitize_url, url_join
from .events import events_from_dataframe
from .events.label_event import LabelEvent
from .events.prediction_event import PredictionEvent
from .sender import get_sender
from .settings import MPMSettings, get_model

LogEventsResult = Union[List[Any], Awaitable[List[Any]]]


class CometMPM:
    """
    The Comet MPM class is used to upload a model's input and output features to MPM
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        workspace_name: Optional[str] = None,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        disabled: Optional[bool] = None,
        asyncio: bool = False,
        max_batch_size: Optional[int] = None,
        max_batch_time: Optional[int] = None,
    ):
        """
        Creates the Comet MPM Event logger object.
        Args:
            api_key: The Comet API Key
            workspace_name: The Comet Workspace Name of the model
            model_name: The Comet Model Name of the model
            model_version: The Comet Model Version of the model
            disabled: If set to True, CometMPM will not send anything to the backend.
            asyncio: Set to True if you are using an Asyncio-based framework like FastAPI.
            max_batch_size: Maximum number of MPM events sent in a batch, can also be configured using the environment variable MPM_MAX_BATCH_SIZE.
            max_batch_time: Maximum time before a batch of events is submitted to MPM, can also be configured using the environment variable MPM_MAX_BATCH_SIZE.
        """

        settings_user_values = {}  # type: Dict[str, str|int]
        optional_update.update(
            settings_user_values,
            {
                "api_key": api_key,
                "mpm_model_name": model_name,
                "mpm_model_version": model_version,
                "mpm_workspace_name": workspace_name,
                "mpm_max_batch_size": max_batch_size,
                "mpm_max_batch_time": max_batch_time,
            },
        )

        self._settings = get_model(
            MPMSettings,
            **settings_user_values,
        )
        if disabled:
            self.disabled = disabled  # type: bool
        else:
            self.disabled = bool(os.getenv("COMET_MPM_DISABLED"))
        self._asyncio = asyncio

        self._mpm_url = url_join(sanitize_url(self._settings.url), MPM_BASE_PATH)
        self._api_url = url_join(sanitize_url(self._settings.url), REST_API_BASE_PATH)

        if self.disabled:
            self._sender = None
        else:
            self._sender = get_sender(
                api_key=self._settings.api_key,
                server_address=self._mpm_url,
                max_batch_size=self._settings.mpm_max_batch_size,
                max_batch_time=self._settings.mpm_max_batch_time,
                asyncio=self._asyncio,
                batch_sending_timeout=self._settings.mpm_batch_sending_timeout,
            )

            atexit.register(self._on_end)

        # TODO: Do handshake

    def log_event(
        self,
        prediction_id: str,
        input_features: Optional[Dict[str, Any]] = None,
        output_value: Optional[Any] = None,
        output_probability: Optional[Any] = None,
        timestamp: Optional[float] = None,
    ) -> Optional[Awaitable[None]]:
        """
        Asynchronously log a single event to MPM. Events are identified by the
        mandatory prediction_id parameter. You can send multiple events with
        the same prediction_id, and the events will be automatically merged
        on the backend side.

        Args:
            prediction_id: The unique prediction ID. It can be provided by the
                framework, you, or a random unique value such as str(uuid4()).
            input_features: If provided, it must be a flat dictionary where the
                keys are the feature names, and the values are native Python
                scalars, such as integers, floats, booleans, or strings. For
                example: `{"age": 42, "income": 42894.89}`.
            output_value: The prediction as a native Python scalar, such as an
                 integer, float, boolean, or string.
            output_probability: If provided, it must be a float between 0 and
                 1, indicating the model's confidence in the prediction.
            timestamp: An optional timestamp to associate with the event
                (seconds since epoch in UTC timezone). If not provided, the
                 current time will be used."""
        if self.disabled:
            if self._asyncio is False:
                return None
            else:
                return asyncio_module.sleep(0)

        event = PredictionEvent(
            workspace=self._settings.mpm_workspace_name,
            model_name=self._settings.mpm_model_name,
            model_version=self._settings.mpm_model_version,
            prediction_id=prediction_id,
            input_features=input_features,
            output_value=output_value,
            output_probability=output_probability,
            timestamp=timestamp,
        )
        return self._log_event(event)

    def log_label(self, prediction_id: str, label: Any) -> Optional[Awaitable[None]]:
        """
        Send an MPM event containing the ground truth value for a prediction whose input and output
        features are already stored in Comet.
        Args:
            prediction_id: The unique prediction ID
            label: The ground truth value for the prediction
        """
        if self.disabled:
            if self._asyncio is False:
                return None
            else:
                return asyncio_module.sleep(0)

        event = LabelEvent(
            workspace=self._settings.mpm_workspace_name,
            model_name=self._settings.mpm_model_name,
            model_version=self._settings.mpm_model_version,
            prediction_id=prediction_id,
            label=label,
        )
        return self._log_event(event)

    def log_dataframe(  # type: ignore[no-untyped-def]
        self,
        dataframe,
        prediction_id_column: str,
        feature_columns: Optional[List[str]] = None,
        output_value_column: Optional[str] = None,
        output_probability_column: Optional[str] = None,
        timestamp_column: Optional[str] = None,
    ) -> LogEventsResult:
        """
        This function logs each row of a Pandas DataFrame as an MPM event. The
        events are structured as described in the [log_event]
        (#cometmpmlog_event) method, so please refer to it for full context.

        Args:
            dataframe: The Pandas DataFrame to be logged.
            prediction_id_column: This column should contain the prediction_id values for the
                events.
            feature_columns: If provided, these columns will be used as the input_features parameter
                for the events.
            output_value_column: If provided, this column will be used as the output_value for the
                events.
            output_probability_column: If provided, this column will be used as the
                output_probability for the events.
            timestamp_column: If provided, this column will be used as the timestamp (seconds since
                epoch start in UTC timezone) for the events.
        """
        events = events_from_dataframe.generate(
            workspace=self._settings.mpm_workspace_name,
            model_name=self._settings.mpm_model_name,
            model_version=self._settings.mpm_model_version,
            dataframe=dataframe,
            prediction_id_column=prediction_id_column,
            feature_columns=feature_columns,
            output_value_column=output_value_column,
            output_probability_column=output_probability_column,
            timestamp_column=timestamp_column,
        )

        return self._log_events(events)

    def connect(self) -> None:
        """
        When using CometMPM in asyncio mode, this coroutine needs to be awaited
        at the server start.
        """
        if self._sender is not None:
            self._sender.connect()

    def join(self, timeout: Optional[int] = None) -> Optional[Awaitable[None]]:
        """
        When using CometMPM in asyncio mode, this coroutine needs to be awaited
        at the server stop.
        """
        if timeout is None:
            timeout = self._settings.mpm_join_timeout

        if not self.disabled:
            assert self._sender is not None
            return self._sender.join(timeout)
        else:
            if self._asyncio is False:
                return None
            else:
                return asyncio_module.sleep(0)

    def _on_end(self) -> None:
        if not self.disabled:
            assert self._sender is not None
            self._sender.close()

    def _log_events(self, events: Iterable[PredictionEvent]) -> LogEventsResult:
        results = []
        for event in events:
            result = self._log_event(event)
            if result is not None:
                results.append(result)

        if self._asyncio and len(results) > 0:
            return asyncio_module.gather(*results)

        return results

    def _log_event(
        self, event: Union[PredictionEvent, LabelEvent]
    ) -> Optional[Awaitable[None]]:
        assert self._sender is not None
        return self._sender.put(event)

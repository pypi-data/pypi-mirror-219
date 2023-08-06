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

import logging
import queue
from threading import Lock, Thread
from typing import Any, Optional, Tuple

from ..batch_utils import ThreadSafeBatch
from ..connection import get_http_session, get_retry_strategy, send_batch_requests
from ..events.label_event import LabelEvent
from ..events.prediction_event import PredictionEvent
from ..logging_messages import (
    BATCH_SENDING_EXCEPTION,
    LABEL_EVENT_SEND_ERROR,
    UNEXPECTED_EVENT_TYPE,
)
from .base import CLOSE_MESSAGE, BaseSender, batch_endpoint_url, labels_endpoint_url

LOGGER = logging.getLogger(__name__)


class ThreadBackgroundSender:
    def __init__(
        self,
        api_key: str,
        server_address: str,
        sender_queue: "queue.Queue[Any]",
        max_batch_size: int,
        max_batch_time: int,
        batch_sending_timeout: int,
    ):
        self.api_key = api_key
        self.server_address = server_address
        self.sender_queue = sender_queue
        self.max_batch_time = max_batch_time
        self.batch = ThreadSafeBatch(max_batch_size, self.max_batch_time)
        self.session = get_http_session(retry_strategy=get_retry_strategy())
        self.batch_sending_timeout = batch_sending_timeout

        self.stop_processing = False

        # Pre-compute URLs
        self.batch_endpoint = batch_endpoint_url(self.server_address)
        self.labels_endpoint = labels_endpoint_url(self.server_address)

    def run(self) -> None:
        """This is meant to be run in an independent Thread"""
        while self.stop_processing is False:
            stop = self._loop()

            if stop is True:
                break

        # We force stop the processing of the queue
        self._check_batch_sending()
        return

    def _loop(self) -> bool:
        try:
            data = self.sender_queue.get(block=True, timeout=self.max_batch_time)
            if data is None:
                return False

            if data is CLOSE_MESSAGE:
                self.stop_processing = True
                return True

            if isinstance(data, PredictionEvent):
                self._process_prediction_event(event=data)
            elif isinstance(data, LabelEvent):
                self._process_label_event(event=data)
            else:
                LOGGER.error(UNEXPECTED_EVENT_TYPE, data)
        except queue.Empty:
            pass

        self._check_batch_sending()

        return False

    def _process_label_event(self, event: LabelEvent) -> None:
        try:
            send_batch_requests(
                self.session,
                self.labels_endpoint,
                api_key=self.api_key,
                batch=event.create_event_dict(),
                batch_sending_timeout=self.batch_sending_timeout,
            )
        except Exception:
            LOGGER.error(LABEL_EVENT_SEND_ERROR, exc_info=True)

    def _process_prediction_event(self, event: PredictionEvent) -> None:
        to_send = event.create_event_dict()
        self.batch.append(to_send)

    def _check_batch_sending(self) -> None:
        try:
            if self.batch.should_be_uploaded(self.stop_processing):
                batch = self.batch.get_and_clear()

                send_batch_requests(
                    self.session,
                    self.batch_endpoint,
                    api_key=self.api_key,
                    batch=batch,
                    batch_sending_timeout=self.batch_sending_timeout,
                )
        except Exception:
            LOGGER.error(BATCH_SENDING_EXCEPTION, exc_info=True)

    def close(self) -> None:
        """For the BackgroundSender to stop processing messages"""
        self.stop_processing = True
        # This shouldn't happen outside of the background sender thread
        self._check_batch_sending()

        self.session.close()


class ThreadSender(BaseSender):
    def __init__(
        self,
        api_key: str,
        server_address: str,
        max_batch_size: int,
        max_batch_time: int,
        batch_sending_timeout: int,
    ) -> None:
        self.lock = Lock()
        self.sender_queue: Optional["queue.Queue[Any]"] = None
        self.background_sender: Optional[ThreadBackgroundSender] = None
        self.background_thread: Optional[Thread] = None
        self.drain = False

        self.api_key = api_key
        self.server_address = server_address
        self.max_batch_time = max_batch_time
        self.max_batch_size = max_batch_size
        self.batch_sending_timeout = batch_sending_timeout

    def _prepare(self) -> "queue.Queue[Any]":
        """We need to create the background thread on the first request to support application
        pre-loading.
        """
        if self.sender_queue is None:
            sender_queue: "queue.Queue[Any]" = queue.Queue()
            self.sender_queue = sender_queue
            self.background_sender = ThreadBackgroundSender(
                api_key=self.api_key,
                server_address=self.server_address,
                sender_queue=self.sender_queue,
                max_batch_size=self.max_batch_size,
                max_batch_time=self.max_batch_time,
                batch_sending_timeout=self.batch_sending_timeout,
            )

        if self.background_thread is None:
            assert self.background_sender is not None
            self.background_thread = Thread(
                target=self.background_sender.run, daemon=True, name="ThreadSender"
            )
            self.background_thread.start()

        assert self.sender_queue is not None
        return self.sender_queue

    def put(self, item: Any) -> None:
        with self.lock:
            if not self.drain:

                if self.sender_queue is None:
                    sender_queue = self._prepare()
                else:
                    sender_queue = self.sender_queue

                sender_queue.put(item)

    def close(self) -> None:
        with self.lock:
            self.drain = True

        if self.sender_queue is not None:
            self.sender_queue.put(CLOSE_MESSAGE)

        if self.background_thread is not None:
            self.background_thread.join(10)

        if self.background_sender is not None:
            self.background_sender.close()

    def join(self, timeout: int) -> None:
        """There is no easy way to plug a shutdown callback with Flask, the "normal" cleaning
        process for Flask is to use the close method"""
        return None

    def connect(self) -> None:
        """There is no easy way nor need to plug a startup callback as we can create everything and
        do the handshake during Python import"""
        return None


def get_thread_sender(
    api_key: str,
    server_address: str,
    max_batch_size: int,
    max_batch_time: int,
    batch_sending_timeout: int,
) -> "ThreadSender":
    sender = ThreadSender(
        api_key=api_key,
        server_address=server_address,
        max_batch_size=max_batch_size,
        max_batch_time=max_batch_time,
        batch_sending_timeout=batch_sending_timeout,
    )

    return sender


def _get_thread_background_sender(
    api_key: str,
    server_address: str,
    max_batch_size: int,
    max_batch_time: int,
    batch_sending_timeout: int,
) -> Tuple["queue.Queue[Any]", "ThreadBackgroundSender"]:
    sender_queue: queue.Queue[Any] = queue.Queue()
    background_sender = ThreadBackgroundSender(
        api_key=api_key,
        server_address=server_address,
        sender_queue=sender_queue,
        max_batch_size=max_batch_size,
        max_batch_time=max_batch_time,
        batch_sending_timeout=batch_sending_timeout,
    )

    return sender_queue, background_sender

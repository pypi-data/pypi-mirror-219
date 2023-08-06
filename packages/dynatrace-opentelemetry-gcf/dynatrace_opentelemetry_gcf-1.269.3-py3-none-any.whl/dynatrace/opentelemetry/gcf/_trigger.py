# Copyright 2022 Dynatrace LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import contextlib
import threading
from typing import Any, Dict, Iterator, NamedTuple, Optional

import flask
from opentelemetry import trace as api_trace
from opentelemetry.context.context import Context
from opentelemetry.propagate import extract
from opentelemetry.trace.span import Span
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.util.types import AttributeValue

from dynatrace.odin.semconv import v1 as semconv
from dynatrace.opentelemetry.gcf._resource import (
    detect_resource,
    get_function_name,
)
from dynatrace.opentelemetry.tracing._logging.loggers import gcf_logger
from dynatrace.opentelemetry.tracing._util.exceptions import record_exception

_INSTRUMENTATION_LIBRARY_NAME = "dynatrace.opentelemetry.gcf"
_FLUSH_TIMEOUT_MILLIS = 6000


class _TriggerGlobals(NamedTuple):
    tracer: api_trace.Tracer
    resource_attrs: Dict[str, AttributeValue]


class Trigger(abc.ABC):
    _TRIGGER_GLOBALS = None  # type: Optional[_TriggerGlobals]
    _TRIGGER_GLOBALS_LOCK = threading.Lock()

    @staticmethod
    def _get_or_prepare_globals() -> _TriggerGlobals:
        if Trigger._TRIGGER_GLOBALS is not None:
            return Trigger._TRIGGER_GLOBALS

        with Trigger._TRIGGER_GLOBALS_LOCK:
            if Trigger._TRIGGER_GLOBALS is not None:
                return Trigger._TRIGGER_GLOBALS

            Trigger._TRIGGER_GLOBALS = _TriggerGlobals(
                tracer=api_trace.get_tracer(_INSTRUMENTATION_LIBRARY_NAME),
                resource_attrs=detect_resource(),
            )

            return Trigger._TRIGGER_GLOBALS

    @contextlib.contextmanager
    def start_as_current_span(self, flush_on_exit: bool) -> Iterator[Span]:
        _globals = self._get_or_prepare_globals()
        parent_context = self._extract_parent()
        attrs = {**_globals.resource_attrs}
        self._add_start_attributes(attrs)

        activation = _globals.tracer.start_as_current_span(
            get_function_name() or "invoke",
            parent_context,
            api_trace.SpanKind.SERVER,
            attributes=attrs,
            record_exception=False,
            set_status_on_exception=False,
            end_on_exit=True,
        )
        span = activation.__enter__()  # pylint:disable=unnecessary-dunder-call
        try:
            yield span
        except Exception as ex:  # pylint:disable=broad-except
            record_exception(span, ex)
            span.set_status(Status(StatusCode.ERROR))
            raise ex
        finally:
            self._on_exit(activation, span, flush_on_exit)

    def _extract_parent(self) -> Context:  # pylint:disable=no-self-use
        return Context()

    @abc.abstractmethod
    def _add_start_attributes(self, attrs: Dict[str, AttributeValue]) -> None:
        pass

    def set_exit_attributes(self, span: Span, result: Any) -> None:
        pass

    def _on_exit(
        self, activation: Iterator[Span], span: Span, flush_on_exit: bool
    ):  # pylint:disable=no-self-use
        activation.__exit__(None, None, None)
        if flush_on_exit:
            _flush_spans()


class GenericTrigger(Trigger):
    def _add_start_attributes(self, attrs: Dict[str, AttributeValue]) -> None:
        attrs[semconv.FAAS_TRIGGER] = semconv.FaasTriggerValues.OTHER.value


class HttpTrigger(Trigger):
    _CAPTURE_HEADERS = {
        "user-agent": semconv.HTTP_USER_AGENT,
        "referer": semconv.DT_HTTP_REQUEST_HEADER_REFERER,
    }

    def __init__(self, request: flask.Request):
        self._request = request

    def _extract_parent(self) -> Context:
        return extract(self._request.headers, Context())

    def _add_start_attributes(self, attrs: Dict[str, AttributeValue]) -> None:
        attrs[semconv.FAAS_TRIGGER] = semconv.FaasTriggerValues.HTTP.value
        attrs[semconv.HTTP_URL] = self._request.url
        attrs[semconv.HTTP_METHOD] = self._request.method or "GET"

        self._capture_http_headers(attrs)

    def _capture_http_headers(self, attrs: Dict[str, AttributeValue]) -> None:
        for header_name, semconv_key in self._CAPTURE_HEADERS.items():
            header_value = self._request.headers.get(header_name)
            if header_value is not None:
                attrs[semconv_key] = header_value

            # TODO capture headers from config

        forwarded_semconv_key = semconv.DT_HTTP_REQUEST_HEADER_FORWARDED
        forwarded_header = self._request.headers.get("forwarded")
        if forwarded_header is None:
            forwarded_semconv_key = (
                semconv.DT_HTTP_REQUEST_HEADER_X_FORWARDED_FOR
            )
            forwarded_header = self._request.headers.get("x-forwarded-for")
        if forwarded_header is not None:
            attrs[forwarded_semconv_key] = forwarded_header

    def set_exit_attributes(self, span: Span, result: Any) -> None:
        if isinstance(result, flask.Response):
            span.set_attribute(semconv.HTTP_STATUS_CODE, result.status_code)
            if result.status_code >= 500:
                span.set_status(Status(StatusCode.ERROR))

    def _on_exit(
        self, activation: Iterator[Span], span: Span, flush_on_exit: bool
    ):
        _super_on_exit = super()._on_exit

        def _after_request(response: flask.Response) -> flask.Response:
            self.set_exit_attributes(span, response)
            _super_on_exit(activation, span, flush_on_exit)

            return response

        try:
            # defer span end until the current flask request is finished
            flask.after_this_request(_after_request)
        except Exception as ex:  # pylint: disable=broad-except
            gcf_logger.warning(
                "Error when registering 'flask.after_this_request' callback: %s",
                ex,
            )
            _super_on_exit(activation, span, flush_on_exit)


def _flush_spans() -> None:
    tracer_provider = api_trace.get_tracer_provider()
    if hasattr(tracer_provider, "force_flush"):
        tracer_provider.force_flush(_FLUSH_TIMEOUT_MILLIS)


def determine_trigger(args, kwargs) -> Trigger:
    arglist = [*args, *kwargs.values()]
    if len(arglist) == 1 and isinstance(arglist[0], flask.Request):
        return HttpTrigger(arglist[0])

    return GenericTrigger()

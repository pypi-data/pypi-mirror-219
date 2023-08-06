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

import contextlib
from typing import Optional

from dynatrace.opentelemetry.tracing._otel.api import (
    _SUPPRESS_INSTRUMENTATION_KEY,
    Context,
    attach,
    create_key,
    detach,
    get_value,
    set_value,
)
from dynatrace.opentelemetry.tracing._propagator.tags import RumTag

TRACING_SUPPRESSION_KEY = create_key("dt-suppress-tracing")

_CTX_RUM_TAG_KEY = create_key("dynatrace-rum-tag")


def get_ctx_rum_tag(context: Context) -> Optional["RumTag"]:
    return get_value(_CTX_RUM_TAG_KEY, context)


def set_ctx_rum_tag(context: Context, rum_tag: RumTag) -> Context:
    return set_value(_CTX_RUM_TAG_KEY, rum_tag, context)


@contextlib.contextmanager
def suppressed_tracing():
    """Suppress recording of spans by updating the current `Context`.

    Sets a context variable to indicate tracers that only suppressed spans should
    be created. A suppressed span is a noop span with the same span context as
    the current active span.

    Sets a context variable to indicate that sensors should skip instrumentation
    code and call the instrumented library directly.
    """
    # instruct sensors to bypass instrumentation (not all sensors might comply)
    context = set_value(_SUPPRESS_INSTRUMENTATION_KEY, True)
    # instruct the tracer to only create suppressed spans
    context = set_value(TRACING_SUPPRESSION_KEY, True, context=context)
    token = attach(context)
    try:
        yield
    finally:
        detach(token)

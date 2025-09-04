import json
from typing import Any, Mapping
from opentelemetry import trace, metrics

class Observability:
    def __init__(self, tracer_name: str = "default_tracer", meter_name: str = "default_meter"):
        self.tracer_name = tracer_name
        self.meter_name = meter_name
        self.tracer = trace.get_tracer(self.tracer_name)
        self.meter = metrics.get_meter(self.meter_name)
        self.publish_items_counter = self.meter.create_counter(
            name="publish_items_total",
            description="Total number of publish items"
        )

    def get_tracer_name(self) -> str:
        return self.tracer_name

    def get_meter_name(self) -> str:
        return self.meter_name

    def _normalize_item(self, item: Any) -> dict:
        # Accept Pydantic model, dict-like, or plain object
        if hasattr(item, "dict") and callable(getattr(item, "dict")):
            return item.dict()
        if isinstance(item, Mapping):
            return dict(item)
        try:
            return dict(vars(item))
        except Exception:
            return {}

    def create_traced_publish_item(self, item: Any):
        data = self._normalize_item(item)
        with self.tracer.start_as_current_span(self.tracer_name) as span:
            item_str = json.dumps(data, default=str)
            span.set_attribute("publish.value", item_str)
        return item

    def create_metric_publish_item(self, item: Any):
        """
        Records a simple counter metric for published items.
        The counter instrument is cached to avoid creating it on every call.
        """
        data = self._normalize_item(item)
        labels = {"item_name": data.get("name", "")}
        self.publish_items_counter.add(1, labels)
        return item
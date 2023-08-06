"""Fake device for testing purposes. No parameters needed."""
from collections.abc import Iterable

from flowchem.components.base_component import FlowchemComponent
from flowchem.devices.flowchem_device import DeviceInfo
from flowchem.devices.flowchem_device import FlowchemDevice
from flowchem.utils.people import dario

from .test_component import TestComponent


class FakeDevice(FlowchemDevice):
    device_info = DeviceInfo(
        authors=[dario],
        maintainers=[dario],
        manufacturer="virtual-device",
        model="FakeDevice",
        serial_number=42,
        version="v1.0",
    )

    def components(self) -> Iterable[FlowchemComponent]:
        """Returns a test Component."""
        component = TestComponent(name="test-component", hw_device=self)
        component.add_api_route("/test", lambda: True, methods=["GET"])
        return (component,)

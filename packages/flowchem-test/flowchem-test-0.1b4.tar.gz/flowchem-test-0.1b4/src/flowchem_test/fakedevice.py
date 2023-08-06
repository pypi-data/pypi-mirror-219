"""Fake device for testing purposes. No parameters needed."""
from flowchem.components.flowchem_component import FlowchemComponent
from flowchem.devices.flowchem_device import DeviceInfo
from flowchem.devices.flowchem_device import FlowchemDevice

from flowchem.utils.people import dario


class TestComponent(FlowchemComponent):
    def __init__(self, name: str, hw_device: FlowchemDevice):
        """Initialize a TestComponent with the provided endpoints."""
        super().__init__(name, hw_device)
        self.add_api_route("/test", lambda: True, methods=["GET"])


class FakeDevice(FlowchemDevice):
    device_info = DeviceInfo(
            authors=[dario],
            maintainers=[dario],
            manufacturer="virtual-device",
            model="FakeDevice",
            serial_number=42,
            version="v1.0",
        )

    async def initialize(self):
        """Add component to device."""
        self.components.append(TestComponent(name="test-component", hw_device=self))

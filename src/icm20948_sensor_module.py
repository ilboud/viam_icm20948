import asyncio
from math import atan2
from typing import Any, ClassVar, Dict, Mapping, Optional, Tuple
from dataclasses import dataclass
from typing_extensions import Self

from viam.components.sensor import Sensor
from viam.components.movement_sensor import MovementSensor, Vector3, Orientation, GeoPoint
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.errors import MethodNotImplementedError, NotSupportedError
from viam.proto.component.movementsensor import GetPropertiesResponse
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_COMPONENT, Subtype
#from viam.components.movement_sensor.movement_sensor import MovementSensor, Vector3, Orientation, GeoPoint

from icm20948 import ICM20948

class ICM20948MovementSensor(MovementSensor):
    # Define the model for this sensor
    MODEL: ClassVar[Model] = Model(ModelFamily("ilboud", "movementsensor"), "icm20948_sensor")
    
    def __init__(self, name: str):
        super().__init__(name)
        self.imu = ICM20948()

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> 'ICM20948MovementSensor':
        movement_sensor = cls(config.name)
        return movement_sensor

    async def get_position(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> Tuple[GeoPoint, float]:
        # The ICM20948 doesn't provide GPS data, so raise a NotImplementedError
        raise NotImplementedError("Position data is not supported by ICM20948.")

    async def get_linear_velocity(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> Vector3:
        # The ICM20948 doesn't provide linear velocity directly, so raise a NotImplementedError
        raise NotImplementedError("Linear velocity is not supported by ICM20948.")

    async def get_angular_velocity(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> Vector3:
        gx, gy, gz, _, _, _ = self.imu.read_accelerometer_gyro_data()
        return Vector3(x=gx, y=gy, z=gz)

    async def get_linear_acceleration(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> Vector3:
        _, _, _, ax, ay, az = self.imu.read_accelerometer_gyro_data()
        return Vector3(x=ax, y=ay, z=az)

    async def get_compass_heading(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> float:
        mx, my, mz = self.imu.read_magnetometer_data()
        # Compute heading from magnetometer data (simplified, you might need a more complex formula depending on your setup)
        heading = atan2(my, mx)
        return heading

    async def get_orientation(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> Orientation:
        # The ICM20948 doesn't provide orientation directly, you'd need more complex algorithms like a quaternion filter to get this.
        raise NotImplementedError("Orientation computation is not implemented.")

    async def get_properties(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> MovementSensor.Properties:
        # Return the properties supported by the ICM20948 sensor
        return MovementSensor.Properties(
            linear_acceleration_supported=True,
            angular_velocity_supported=True,
            orientation_supported=False,
            position_supported=False,
            compass_heading_supported=True,
            linear_velocity_supported=False
        )

    async def get_accuracy(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> Mapping[str, float]:
        # This is a mock, as accuracy would depend on real sensor calibration and other factors
        return {
            "angular_velocity": 0.1,   # Just for example
            "linear_acceleration": 0.05,  # Just for example
            "compass_heading": 2.0  # Just for example
        }

async def main():
    # Create a configuration with the desired sensor name
    config = ComponentConfig(name="My_ICM20948_Sensor")
    
    # Instantiate the ICM20948MovementSensor using the class method 'new'
    icm_sensor = ICM20948MovementSensor.new(config=config, dependencies={})

    # Fetch the properties of the sensor to know what's supported
    properties = await icm_sensor.get_properties()
    print("Sensor Properties:", properties)

    # If linear acceleration is supported, fetch and print it
    if properties.linear_acceleration_supported:
        la = await icm_sensor.get_linear_acceleration()
        print("Linear Acceleration:", la)

    # If angular velocity is supported, fetch and print it
    if properties.angular_velocity_supported:
        av = await icm_sensor.get_angular_velocity()
        print("Angular Velocity:", av)

    # If compass heading is supported, fetch and print it
    if properties.compass_heading_supported:
        heading = await icm_sensor.get_compass_heading()
        print("Compass Heading:", heading)

    # Fetch all readings (this will include error messages for unsupported ones)
    readings = await icm_sensor.get_readings()
    print("All Sensor Readings:", readings)

if __name__ == '__main__':
    asyncio.run(main())

import asyncio

from viam.module.module import Module
from .icm20948_sensor_module import ICM20948MovementSensor
#from viam.components.movement_sensor.movement_sensor import MovementSensor
from viam.components.movement_sensorimport MovementSensor

async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `gizmo.__init__.py` file.
    """

    module = Module.from_args()
    module.add_model_from_registry(MovementSensor.SUBTYPE, ICM20948MovementSensor.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())
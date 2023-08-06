from rclpy.node import Node
from raya.enumerations import ANGLE_UNIT, POSITION_UNIT
from raya.constants import *
from raya_constants.interfaces import *
from raya.exceptions_handler import *
from raya.controllers.base_controller import BaseController
from raya.exceptions import *

TIME_TIMEOUT_SRV = DEFAULT_COMMAND_TIMEOUT


class StatusController(BaseController):

    def __init__(self, name: str, node: Node, interface, extra_info):
        pass

    async def get_raya_status(self) -> dict:
        return

    async def get_available_arms(self) -> dict:
        return

    async def get_battery_status(self) -> dict:
        return

    async def get_localization_status(self, ang_unit: ANGLE_UNIT,
                                      pos_unit: POSITION_UNIT) -> dict:
        return

    async def get_manipulation_status(self) -> dict:
        return

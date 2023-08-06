from rclpy.node import Node
from raya.enumerations import ANGLE_UNIT
from raya.controllers.base_controller import BaseController


class LidarController(BaseController):

    def __init__(self, name: str, node: Node, interface, extra_info):
        pass

    def get_laser_info(self,
                       ang_unit: ANGLE_UNIT = ANGLE_UNIT.DEGREES) -> dict:
        return

    def get_raw_data(self):
        return

    def check_obstacle(self,
                       lower_angle: float,
                       upper_angle: float,
                       lower_distance: float = 0.0,
                       upper_distance: float = float('inf'),
                       ang_unit: ANGLE_UNIT = ANGLE_UNIT.DEGREES) -> bool:
        return

    def create_obstacle_listener(
            self,
            listener_name: str,
            lower_angle: float,
            upper_angle: float,
            callback=None,
            callback_async=None,
            lower_distance: float = 0.0,
            upper_distance: float = float('inf'),
            ang_unit: ANGLE_UNIT = ANGLE_UNIT.DEGREES) -> None:
        pass

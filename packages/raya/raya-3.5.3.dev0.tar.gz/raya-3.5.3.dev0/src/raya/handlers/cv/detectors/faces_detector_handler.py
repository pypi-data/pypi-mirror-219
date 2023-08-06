from rclpy.node import Node
from raya.handlers.cv.detectors.detector_handler import DetectorHandler


class FacesDetectorHandler(DetectorHandler):

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict, continues_msg: bool, cli_cmd, cmd_call):
        pass

import typing
from rclpy.node import Node
from raya.handlers.cv.detectors.detector_handler import DetectorHandler


class TagsDetectorHandler(DetectorHandler):

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict, continues_msg: bool, cli_cmd, cmd_call):
        pass

    async def find_tags(self,
                        tags: dict,
                        callback: typing.Callable = None,
                        callback_async: typing.Callable = None,
                        wait: bool = False,
                        timeout: float = 0.0,
                        as_dict: bool = False):
        return

    def cancel_find_tags(self):
        pass

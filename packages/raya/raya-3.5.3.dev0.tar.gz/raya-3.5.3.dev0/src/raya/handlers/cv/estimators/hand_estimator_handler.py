from rclpy.node import Node
from raya.handlers.cv.estimators.estimator_handler import EstimatorHandler


class HandEstimatorHandler(EstimatorHandler):

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict, continues_msg: bool, cli_cmd, cmd_call):
        pass

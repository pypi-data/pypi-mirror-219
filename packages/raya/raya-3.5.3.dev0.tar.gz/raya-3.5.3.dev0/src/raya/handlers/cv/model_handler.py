from rclpy.node import Node


class ModelHandler():

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict):
        self.model_id = model_id

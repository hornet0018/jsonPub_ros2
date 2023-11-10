import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, UInt8, String, Float64
import json

class DataToJsonNode(Node):
    def __init__(self):
        super().__init__('data_to_json_node')
        self.json_topic_name = '/switchbot/data'

        # Subscribe to the necessary topics with their message types
        self.create_subscription(Int32, '/co2ppm', self.co2ppm_callback, 10)
        self.create_subscription(UInt8, '/switchbot/battery', self.switchbot_battery_callback, 10)
        self.create_subscription(UInt8, '/switchbot/humidity', self.switchbot_humidity_callback, 10)
        self.create_subscription(Float64, '/switchbot/temperature', self.switchbot_temperature_callback, 10)
        # Subscribe to the m5stack_button_state topic
        self.create_subscription(UInt8, '/m5stack_button_state', self.m5stack_button_state_callback, 10)

        # Initialize the publisher to send out the JSON string
        self.publisher_json = self.create_publisher(String, self.json_topic_name, 10)

        # Data dictionary to store the received values
        self.sensor_data = {}

    def publish_json(self):
        # Convert the dictionary to a JSON string and publish it
        json_str = json.dumps(self.sensor_data)
        self.publisher_json.publish(String(data=json_str))
        self.get_logger().info(f'Published JSON data: {json_str}')

    # Callback functions for each topic
    def co2ppm_callback(self, msg):
        self.sensor_data['co2ppm'] = msg.data
        self.publish_json()

    def switchbot_battery_callback(self, msg):
        self.sensor_data['battery'] = msg.data
        self.publish_json()

    def switchbot_humidity_callback(self, msg):
        self.sensor_data['humidity'] = msg.data
        self.publish_json()

    def switchbot_temperature_callback(self, msg):
        self.sensor_data['temperature'] = msg.data
        self.publish_json()

    # Callback for the m5stack_button_state topic
    def m5stack_button_state_callback(self, msg):
        self.sensor_data['button_state'] = msg.data
        self.publish_json()

def main(args=None):
    rclpy.init(args=args)
    node = DataToJsonNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

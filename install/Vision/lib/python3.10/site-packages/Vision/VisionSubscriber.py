import rclpy
from rclpy.node import Node
from sensor_msgs import msg
from cv_bridge import CvBridge
import cv2
from PIL import Image, ImageTk
import threading
from .UserInterface import *


class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('Vision')
        self.subscription = self.create_subscription(
            msg.Image,
            '/rgb',  # Change topic based on your setup
            self.image_callback,
            10)
        self.subscription  # Prevent unused variable warning
        self.bridge = CvBridge()
        self.turretApp= MainTurretApp()


    def image_callback(self, msg):
        try:
            # Convert ROS2 Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            wx.CallAfter(self.turretApp.setCameraFrameFeed, cv_image)
            
        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()

    ros_thread = threading.Thread(target=rclpy.spin, args=(node,))
    ros_thread.start()

    try:
        node.turretApp.MainLoop()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()
    ros_thread.join()

if __name__ == '__main__':
    main()

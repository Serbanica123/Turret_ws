import rclpy
from rclpy.node import Node
from sensor_msgs import msg
from cv_bridge import CvBridge
import cv2
from PIL import Image, ImageTk
import threading
import tkinter as tk

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
        
        self.root= tk.Tk()
        self.root.title("Turret GUI")
        self.canvas = tk.Canvas(self.root, width=2560, height=1440)
        self.canvas.pack()

        # Create a placeholder image object
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW)

        self.update_gui()

    def on_canvas_click(self, event, img):
        """ Handles mouse click events on the canvas. """
        x, y = event.x, event.y
        print(f"Mouse clicked at: {x}, {y}")

        """# Draw circles on the image
        cv2.circle(img, (x, y), 1, (0, 0, 255), 1)
        cv2.circle(img, (x, y), 10, (0, 0, 255), 2)

        # Update the displayed image
        image = Image.fromarray(img)
        photo = ImageTk.PhotoImage(image)

        self.canvas.itemconfig(self.image_id, image=photo)
        self.canvas.image = photo  # Prevent garbage collection"""

    def image_callback(self, msg):
        try:
            # Convert ROS2 Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(cv_image)
            self.photo = ImageTk.PhotoImage(image)

            self.canvas.itemconfig(self.image_id, image=self.photo)
            self.canvas.image = self.photo  # Prevent garbage collection
            self.canvas.bind("<Button-1>", lambda event: self.on_canvas_click(event, cv_image))

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def update_gui(self):
        self.root.update()
        self.root.after(10, self.update_gui)

def ros_spin_thread(node):
    rclpy.spin(node)  # Runs in the background

def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()

    # Start ROS2 in a background thread
    ros_thread = threading.Thread(target=ros_spin_thread, args=(node,))
    ros_thread.start()

    # Run the Tkinter GUI in the main thread
    try:
        node.root.mainloop()
    except KeyboardInterrupt:
        pass

    # Clean up on exit
    node.destroy_node()
    rclpy.shutdown()
    ros_thread.join()

if __name__ == '__main__':
    main()

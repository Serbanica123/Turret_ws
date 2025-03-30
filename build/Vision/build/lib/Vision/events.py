import cv2
from PIL import Image, ImageTk
def on_canvas_click(event, img, canvas, image_id):
    """ Handles mouse click events on the canvas. """
    x, y = event.x, event.y
    print(f"Mouse clicked at: {x}, {y}")

    # Draw circles on the image
    cv2.circle(img, (x, y), 1, (0, 0, 255), 1)
    cv2.circle(img, (x, y), 10, (0, 0, 255), 2)

    # Update the displayed image
    image = Image.fromarray(image)
    photo = ImageTk.PhotoImage(image)

    canvas.itemconfig(image_id, image=photo)
    canvas.image = photo  # Prevent garbage collection
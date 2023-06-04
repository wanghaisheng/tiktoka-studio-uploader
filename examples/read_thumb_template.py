import tkinter as tk
from tkinter import filedialog
import cv2
import os

# Global variables
drawing = False
ix, iy = -1, -1
image_path = ""
annotations = []


def draw_rectangle(event, x, y, flags, param):
    global drawing, ix, iy, image, annotations

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(image, (ix, iy), (x, y), (0, 255, 0), 2)
        annotations.append((ix, iy, x, y))
        cv2.imshow("Image", image)


def select_image():
    root = tk.Tk()
    root.withdraw()
    image_file = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    return image_file


def annotate_image():
    global image_path, image, annotations

    image_path = select_image()
    if not image_path:
        print("No image selected.")
        return

    image = cv2.imread(image_path)
    annotations = []

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_rectangle)

    while True:
        cv2.imshow("Image", image)
        key = cv2.waitKey(1) & 0xFF

        # Press 's' to save annotations
        if key == ord("s"):
            save_annotations()
            break

        # Press 'r' to reset annotations
        if key == ord("r"):
            annotations = []
            image = cv2.imread(image_path)
            cv2.imshow("Image", image)

        # Break the loop when the window is closed
        if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()


def save_annotations():
    global image_path, annotations

    filename = os.path.splitext(os.path.basename(image_path))[0]
    save_path = f"{filename}.txt"

    with open(save_path, "w") as f:
        for annotation in annotations:
            f.write(
                f"{annotation[0]} {annotation[1]} {annotation[2]} {annotation[3]}\n"
            )

    print("Annotations saved successfully.")


if __name__ == "__main__":
    annotate_image()

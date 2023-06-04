import cv2
from flet import App, FileChooser

# Global variables
image = None
bounding_boxes = []
current_box = None
is_drawing = False
font_size = 12


def draw_bounding_boxes():
    global image, bounding_boxes
    img_copy = image.copy()
    for box in bounding_boxes:
        cv2.rectangle(img_copy, box[0], box[1], (0, 255, 0), 2)
    cv2.imshow("Image", img_copy)


def mouse_callback(event, x, y, flags, param):
    global current_box, is_drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        current_box = [(x, y)]
        is_drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        current_box.append((x, y))
        bounding_boxes.append(tuple(current_box))
        is_drawing = False
        calculate_text_font_size(current_box[0], current_box[1])
        draw_bounding_boxes()


def calculate_text_font_size(top_left, bottom_right):
    global font_size
    box_width = abs(bottom_right[0] - top_left[0])
    box_height = abs(bottom_right[1] - top_left[1])
    # Calculate font size based on box dimensions (modify this as per your requirements)
    font_size = min(box_width, box_height) // 10


def select_image():
    app = App()
    file_chooser = FileChooser()
    app.add(file_chooser)
    app.run()

    file_path = file_chooser.get_path()
    return file_path


def main():
    global image, bounding_boxes, is_drawing, font_size
    image_path = select_image()
    if not image_path:
        print("No image selected.")
        return

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image:", image_path)
        return

    # Create a window and display the image
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)
    draw_bounding_boxes()

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("r"):
            bounding_boxes = []
            draw_bounding_boxes()

    # Save bounding box coordinates to a file
    with open("bounding_boxes.txt", "w") as f:
        for box in bounding_boxes:
            f.write(f"{box[0][0]},{box[0][1]},{box[1][0]},{box[1][1]}\n")

    cv2.destroyAllWindows()

    # Print calculated font size for each bounding box
    print("Font Sizes:")
    for i, box in enumerate(bounding_boxes):
        print(f"Box {i+1}: {font_size}pt")


if __name__ == "__main__":
    main()

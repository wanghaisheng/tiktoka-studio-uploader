import pandas as pd
import json
from PIL import Image, ImageDraw, ImageFont
import os, sys


def calculate_text_size(text, font):
    width, height = font.getsize(text)
    return width, height


def calculate_text_lines(text, font, max_width):
    lines = []
    words = text.split()
    current_line = words[0]
    for word in words[1:]:
        line_width, _ = calculate_text_size(current_line + " " + word, font)
        if line_width <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines


def convert_canvas_coord_to_corner(canvas_coord, zone_width, zone_height):
    zone_number = canvas_coord - 1
    zone_column = zone_number % 4
    zone_row = zone_number // 4
    corner_x = zone_column * zone_width
    corner_y = zone_row * zone_height
    return corner_x, corner_y


def draw_multiline_text(draw, text, start_coord, font, max_width, line_spacing):
    lines = calculate_text_lines(text, font, max_width)
    x, y = start_coord
    for line in lines:
        draw.text((x, y), line, font=font)
        x, y = start_coord[0], y + line_spacing


def clean_column_name(column_name):
    return column_name.replace(" ", "_")


def get_default_font(language):
    if sys.platform == "win32":
        if language == "en":
            return "arial.ttf"  # Use Arial as default font on Windows for English text
        elif language == "es":
            return "arial.ttf"  # Use Arial as default font on Windows for Spanish text
        elif language == "zh":
            return (
                "simhei.ttf"  # Use SimHei as default font on Windows for Chinese text
            )
    elif sys.platform == "darwin":
        if language == "en":
            return "/Library/Fonts/Arial.ttf"  # Use Arial as default font on macOS for English text
        elif language == "es":
            return "/Library/Fonts/Arial.ttf"  # Use Arial as default font on macOS for Spanish text
        elif language == "zh":
            return "/Library/Fonts/SimHei.ttf"  # Use SimHei as default font on macOS for Chinese text
    else:
        if language == "en":
            return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Use DejaVu Sans as default font on Unix-based systems for English text
        elif language == "es":
            return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Use DejaVu Sans as default font on Unix-based systems for Spanish text
        elif language == "zh":
            return "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"  # Use WQY Microhei as default font on Unix-based systems for Chinese text


def draw_text_on_image(row, output_folder):
    result_image_size = row["result_image_size"].split("x")
    result_image_width, result_image_height = map(int, result_image_size)

    # Load and resize the background image
    background_image_path = row["background_image"]
    background_image = Image.open(background_image_path).resize(
        (result_image_width, result_image_height)
    )

    # Create a new image with the resized background image
    result_image = Image.new("RGB", (result_image_width, result_image_height))
    result_image.paste(background_image)

    # Create a drawing object
    draw = ImageDraw.Draw(result_image)
    # Load font files or fallback to default system fonts for different languages
    try:
        title_font_path = row["title_font"]
        title_font = ImageFont.truetype(
            title_font_path, size=int(row["title_font_size"])
        )
    except (OSError, FileNotFoundError):
        title_font = ImageFont.truetype(
            get_default_font(row["title_language"]), size=int(row["title_font_size"])
        )

    try:
        subtitle_font_path = row["subtitle_font"]
        subtitle_font = ImageFont.truetype(
            subtitle_font_path, size=int(row["subtitle_font_size"])
        )
    except (OSError, FileNotFoundError):
        subtitle_font = ImageFont.truetype(
            get_default_font(row["subtitle_language"]),
            size=int(row["subtitle_font_size"]),
        )

    try:
        extra_text_font_path = row["extra_text_font"]
        extra_text_font = ImageFont.truetype(
            extra_text_font_path, size=int(row["extra_text_font_size"])
        )
    except (OSError, FileNotFoundError):
        extra_text_font = ImageFont.truetype(
            get_default_font(row["extra_text_language"]),
            size=int(row["extra_text_font_size"]),
        )

    # Split the result image into 16 zones
    zones_horizontal = 4
    zones_vertical = 4

    # Calculate the zone width and height
    zone_width = result_image_width // zones_horizontal
    zone_height = result_image_height // zones_vertical

    # Get the corner coordinates for each area
    title_area = int(row["title_area_number"])
    title_corner_coord = convert_canvas_coord_to_corner(
        title_area, zone_width, zone_height
    )

    subtitle_area = int(row["subtitle_area_number"])
    subtitle_corner_coord = convert_canvas_coord_to_corner(
        subtitle_area, zone_width, zone_height
    )

    extra_text_area = int(row["extra_text_area_number"])
    extra_text_corner_coord = convert_canvas_coord_to_corner(
        extra_text_area, zone_width, zone_height
    )

    # Draw title text
    title_text = row["title"]
    draw_multiline_text(
        draw,
        title_text,
        title_corner_coord,
        title_font,
        zone_width,
        int(row["title_font_size"]),
    )

    # Draw subtitle text
    subtitle_text = row["subtitle"]
    draw_multiline_text(
        draw,
        subtitle_text,
        subtitle_corner_coord,
        subtitle_font,
        zone_width,
        int(row["subtitle_font_size"]),
    )

    # Draw extra text
    extra_text = row["extra_text"]
    draw_multiline_text(
        draw,
        extra_text,
        extra_text_corner_coord,
        extra_text_font,
        zone_width,
        int(row["extra_text_font_size"]),
    )
    # Save the result image with the video_id as the filename
    video_id = row["video_id"]
    # Save the result image with the video_id as the filename
    result_image.save(os.path.join(output_folder, f"{video_id}.jpg"))

    # Overlay gridlines
    for x in range(zone_width, result_image_width, zone_width):
        draw.line([(x, 0), (x, result_image_height)], fill="red", width=1)
    for y in range(zone_height, result_image_height, zone_height):
        draw.line([(0, y), (result_image_width, y)], fill="red", width=1)

    new_filename = f"{video_id}-grid.jpg"
    result_image.save(os.path.join(output_folder, new_filename))


def process_file(file_path, output_folder):
    _, file_extension = os.path.splitext(file_path)
    if file_extension == ".xlsx":
        df = pd.read_excel(file_path, engine="openpyxl")
    elif file_extension == ".csv":
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    elif file_extension == ".json":
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    else:
        raise ValueError(
            "Invalid file format. Only Excel, CSV, and JSON files are supported."
        )

    df.columns = [clean_column_name(col) for col in df.columns]
    for _, row in df.iterrows():
        draw_text_on_image(row, output_folder)


def main():
    file_path = "data.json"  # Replace with your file path
    output_folder = "output"  # Replace with your desired output folder path
    os.makedirs(output_folder, exist_ok=True)
    process_file(file_path, output_folder)


if __name__ == "__main__":
    main()

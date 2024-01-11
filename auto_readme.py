import argparse, math, os
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", dest="name", help="Name", type=str, default="")
parser.add_argument("-s", "--style", dest="style", help="Style", type=str, default="")
parser.add_argument("-d", "--directory", dest="directory", help="Directory", type=str, default="")
args = parser.parse_args()

names = {
    "bw": "Black & White",
    "diiivoy": "DIIIVOY",
    "diiivoycolor": "DIIIVOY Color"
}


if args.name:
    name = args.name
elif args.style:
    name = names[args.style] if args.style in names else args.style.capitalize()
else:
    name = "Original"

if args.directory:
    directory = args.directory
elif args.style:
    directory = args.style
else:
    directory = "original"

repo = f"Plex Meta Manager People - {name}{f' ({args.style})' if args.style else ''}"

total_data = []
letters = [lt for lt in os.listdir(directory) if lt not in [".git", ".github", ".idea", "README.md"]]
letters.sort()
total = 0
for letter in letters:
    letter_folder = os.path.join(directory, letter)
    images_folder = os.path.join(letter_folder, "Images")
    if not os.path.exists(images_folder):
        print(f"Images Folder: {images_folder} does not exist")
        continue
    base_letter_url = f"https://raw.githubusercontent.com/meisnate12/Plex-Meta-Manager-People{f'-{args.style}' if args.style else ''}/master/{letter}/Images/"
    files = os.listdir(images_folder)
    files.sort()
    data = [f"\n* [{os.path.splitext(f)[0]}]({base_letter_url}{quote(str(f))})" for f in files]
    if files:
        total_data.append(f'\n<details><summary><a href="{letter}">{letter} ({len(files)} Images)</a></summary>')
        total_data.append("\n")
        total_data.extend(data)
        total_data.append("\n</details>")
        total += len(files)

        num_columns = int(math.sqrt(len(files)))
        text_color = (255, 255, 255)
        thumb_size = (200, 200)
        show_text = True
        num_rows = len(files) // num_columns + (len(files) % num_columns > 0)
        grid_size = (num_columns * thumb_size[0], num_rows * (thumb_size[1] + 20) + 20)
        grid_image = Image.new('RGB', grid_size, (0, 0, 0))
        draw = ImageDraw.Draw(grid_image)
        font = ImageFont.truetype('arial.ttf', size=12)

        for i, file in enumerate(files):
            image_path = os.path.join(images_folder, file)
            image = Image.open(image_path)
            image.thumbnail(thumb_size, Image.LANCZOS)

            col_index = i % num_columns
            row_index = i // num_columns
            x = col_index * thumb_size[0]
            y = row_index * (thumb_size[1] + 20) + 20
            x_offset = (thumb_size[0] - image.size[0]) // 2
            y_offset = (thumb_size[1] - image.size[1]) // 2
            filename = os.path.splitext(file)[0]
            text_bbox = font.getbbox(filename)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = x + (thumb_size[0] - text_width - 20) // 2 + 10
            text_y = y + thumb_size[1] + 5
            box_width = thumb_size[0] - 20
            box_height = text_height

            grid_image.paste(image, (x + x_offset, y + y_offset))
            draw.rectangle((x + 10, text_y - 2, x + 10 + box_width, text_y + box_height + 2), fill=(0, 0, 0))
            draw.text((text_x, text_y), filename, font=font, fill=text_color)

        for i in range(num_columns + 1):
            x = i * thumb_size[0]
            draw.line((x, 0, x, grid_size[1]), fill=(0, 0, 0))

        for i in range(num_rows + 1):
            y = i * (thumb_size[1] + 20) + 20
            draw.line((0, y, grid_size[0], y), fill=(0, 0, 0))

        grid_image.save(os.path.join(letter_folder, "grid.jpg"))

    with open(os.path.join(directory, letter, "README.md"), "w", encoding="utf-8") as f:
        f.writelines([f"# {repo} - {letter} ({len(files)} Images)", "\n", "![Grid](grid.jpg)", "\n"] + data)

with open(os.path.join(directory, "README.md"), "w", encoding="utf-8") as f:
    f.writelines([f"# {repo} ({total} Images)", "\n"] + total_data)

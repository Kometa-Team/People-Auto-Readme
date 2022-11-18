import argparse, os
from urllib.parse import quote

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", dest="name", help="Name", type=str)
parser.add_argument("-s", "--style", dest="style", help="Style", type=str)
parser.add_argument("-d", "--directory", dest="directory", help="Directory", type=str, default="imagerepo")
args = parser.parse_args()

repo = f"Plex Meta Manager People - {args.name} ({args.style})"

total_data = []
letters = [l for l in os.listdir(args.directory) if l not in [".git", ".github", ".idea", "README.md"]]
letters.sort()
total = 0
for letter in letters:
    images_folder = os.path.join(args.directory, letter, "Images")
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
    with open(os.path.join(args.directory, letter, "README.md"), "w", encoding="utf-8") as f:
        f.writelines([f"# {repo} - {letter} ({len(files)} Images)", "\n"] + data)

with open(os.path.join(args.directory, "README.md"), "w", encoding="utf-8") as f:
    f.writelines([f"# {repo} ({total} Images)", "\n"] + total_data)

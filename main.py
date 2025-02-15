import os
import sys
import time
import shutil
import argparse
import re

def format_size(size):
    if size < 1024:
        return f"{size: >7.2f} B"
    elif size < 1024 * 1024:
        return f"{size / 1024: >7.2f} KiB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024): >7.2f} MiB"
    elif size < 1024 * 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024 * 1024): >7.2f} GiB"
    else:
        return f"{size / (1024 * 1024 * 1024 * 1024): >7.2f} TiB"

def format_score(score):
    if score == 0:
        return "0.00"
    magnitude = 0
    while abs(score) >= 10:
        magnitude += 1
        score /= 10
    return f"{score:.2f}e"+f"{magnitude * 1}".zfill(2)

def list_files_and_folders(path, min_score=0, reverse=False, delete=False, exclude=None, min_age=0):
    entries = []
    total_size = 0
    last_modified = 0

    # List all items directly in the path
    items = os.listdir(path)

    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and not os.path.islink(item_path) and os.stat(file_path).st_nlink <= 1:
            # If it's a file, add its details to the entries list
            file_size = os.path.getsize(item_path)
            file_modified = os.path.getmtime(item_path)
            entries.append((item, file_size, file_modified, file_size))
            #total_size += file_size
            last_modified = max(last_modified, file_modified)
        elif os.path.isdir(item_path) and not os.path.islink(item_path):
            # If it's a directory, iterate over its files
            folder_size = 0
            folder_modified = 0
            for root, dirs, filenames in os.walk(item_path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if not os.path.islink(file_path) and os.stat(file_path).st_nlink <= 1:
                        file_size = os.path.getsize(file_path)
                        file_modified = os.path.getmtime(file_path)
                        folder_size += file_size
                        folder_modified = max(folder_modified, file_modified)
            entries.append((item, folder_size, folder_modified, folder_size))
            #total_size += folder_size
            last_modified = max(last_modified, folder_modified)

    # Filter entries by min_score
    entries = [entry for entry in entries if (time.time() - entry[2]) * entry[1] >= min_score and (time.time() - entry[2]) / (60*60*24) >= min_age]
    newentries = []
    if exclude is not None:
        for entry in entries:
            x = re.search(exclude, entry[0])
            if not x:
                newentries.append(entry)
        entries = newentries
    total_size = sum([entry[3] for entry in entries])

    # Sort entries by score
    entries.sort(key=lambda x: (time.time() - x[2]) * x[1], reverse=reverse)

    # Print entries
    print("Score      Date                   Size     Name")
    for entry in entries:
        score = (time.time() - entry[2]) * entry[1]
        print(f"{format_score(score)}  {time.strftime('%d.%m.%Y %H:%M', time.localtime(entry[2]))}  {format_size(entry[1])} \t{entry[0]}")

    print("\nTotal Size:", format_size(total_size))
    print("Last Modified:", time.strftime('%d.%m.%Y %H:%M', time.localtime(last_modified)))

    # Ask for delete option
    if delete:
        if input("Do you want to delete the listed entries? (yes/no): ").lower() == "yes":
            for entry in entries:
                entry_path = os.path.join(path, entry[0])
                if os.path.isdir(entry_path):
                    print("Delete folder "+entry_path)
                    shutil.rmtree(entry_path)
                elif os.path.isfile(entry_path):
                    print("Delete file "+entry_path)
                    os.remove(entry_path)
            print("Entries deleted successfully.")
        else:
            print("Entries not deleted.")
    else:
        print("use --delete to delete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List files and folders with scores.")
    parser.add_argument("path", help="The path to the folder")
    parser.add_argument("--min_score", type=float, default=1, help="Minimum score to filter entries")
    parser.add_argument("--min_age", type=int, default=0, help="Minimum age in days to filter entries")
    parser.add_argument("--exclude", type=str, default=None, help="Regex of files to ignore")
    parser.add_argument("--reverse", action="store_true", help="Reverse sorting order")
    parser.add_argument("--delete", action="store_true", help="Enable delete option")
    args = parser.parse_args()

    list_files_and_folders(args.path, min_score=args.min_score, reverse=args.reverse, delete=args.delete, exclude=args.exclude, min_age=args.min_age)

# File and Folder Scoring Script

This script lists files and folders in a specified directory, calculates a score based on their size and last modified time, and optionally deletes them based on user input. Note that the script ignores files that are linked (soft or hardlink).

## Usage

```bash
python main.py <path> [--min_score MIN_SCORE] [--min_age MIN_AGE] [--exclude EXCLUDE] [--reverse] [--delete]
```

### Arguments

- `path`: The path to the folder to be scanned.
- `--min_score`: Minimum score to filter entries (default: 1).
- `--min_age`: Minimum age in days to filter entries (default: 0).
- `--exclude`: Regex pattern to exclude files or folders.
- `--reverse`: Reverse the sorting order.
- `--delete`: Enable delete option.

### Example

```bash
python3 main.py /path/to/folder --min_score 10 --min_age 30 --exclude ".*\.log" --reverse --delete
```

This command will list files and folders in `/path/to/folder` with a minimum score of 10, minimum age of 30 days, excluding files with `.log` extension, in reverse order, and prompt for deletion.

## License

This project is licensed under the MIT License.

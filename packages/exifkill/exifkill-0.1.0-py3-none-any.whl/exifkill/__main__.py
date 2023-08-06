from sys import argv, exit as sys_exit, stderr
from exifkill import drop_exif
from os import EX_USAGE

if __name__ == "__main__":
    if len(argv) < 3:
        print(f"usage: exifkill <input_path> <output_path>", file=stderr)
        sys_exit(EX_USAGE)
    drop_exif(argv[1], argv[2])

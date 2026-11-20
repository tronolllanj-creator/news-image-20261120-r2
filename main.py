import os
import sys
import shutil


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        head = f.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        raise ValueError("copied file is not a valid PNG")
    size = os.path.getsize(dst)
    print(dst)
    print(size)
    return 0


if __name__ == "__main__":
    sys.exit(main())

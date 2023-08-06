from __future__ import annotations

import argparse

from tally_token import merge_bytes_into, split_bytes_into


def split_main(*, source_path: str, dest_paths: str) -> None:
    with open(source_path, "rb") as f:
        source = f.read()
    tokens = split_bytes_into(source, len(dest_paths))
    for token, dest_path in zip(tokens, dest_paths):
        with open(dest_path, "wb") as f:
            f.write(token)


def merge_main(*, dest_path: str, source_paths: str) -> None:
    tokens = []
    for source_path in source_paths:
        with open(source_path, "rb") as f:
            tokens.append(f.read())
    with open(dest_path, "wb") as f:
        f.write(merge_bytes_into(tokens))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        required=True,
        dest="command",
        help=(
            "Commands:\n"
            "split: split a file into multiple files\n"
            "merge: merge multiple files into a file"
            "Example:\n"
            "tally-token split example.bin example.bin.1 example.bin.2 example.bin.3\n"
            "tally-token merge example-merged.bin example.bin.1 example.bin.2 example.bin.3"
        ),
    )
    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("src", help="The source file to be split.")
    split_parser.add_argument("dst", nargs="+", help="The destination files.")

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("dst", help="The destination file.")
    merge_parser.add_argument("src", nargs="+", help="The source files.")

    args = parser.parse_args()
    if args.command == "split":
        split_main(source_path=args.src, dest_paths=args.dst)
    elif args.command == "merge":
        merge_main(dest_path=args.dst, source_paths=args.src)


if __name__ == "__main__":
    main()

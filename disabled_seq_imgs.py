#!/usr/bin/env python3
"""
A simple module to get the paths of the disabled images in a Siril sequence.

Siril is an astronomical image processing tool: https://siril.org

This module uses the generated conversion (e.g. light_conversion.txt) and sequence (e.g.
r_pp_light_.seq) files to get the file paths of the disabled images of the sequence.
"""
import re


def parse_seq_map(seq_file_path: str):
    """
    Returns a dict representing the Siril sequence. Where the key is the img ID and the value
    is a boolean indicating whether the img has been disabled.

    For ex, file:
    ```
    I 1 0
    I 2 1
    I 3 1
    ```

    will return `{'1': False, '2': True, '3': True}`

    Arguments:
    seq_file_path -- the path to the seq file Siril
    """

    seq_map: dict[str, bool] = {}

    with open(seq_file_path, encoding="utf-8") as file:
        for line in file:
            cols = line.split(" ")

            if len(cols) == 3 and cols[0] == "I":
                img_id = cols[1]
                is_enabled = bool(int(cols[2]))

                seq_map[img_id] = is_enabled

    return seq_map


def parse_conversion_map(conversion_file_path: str):
    """
    Returns a dict representing the mapping between the Siril img IDs and the original input files.

    For ex, file:
    ```
    '/path/to/IMG_3214.CR2' -> '../process/light_00001.fit'
    '/path/to/IMG_3215.CR2' -> '../process/light_00002.fit'
    '/path/to/IMG_3216.CR2' -> '../process/light_00003.fit'
    ```

    will return
    `{'1': '/path/to/IMG_3214.CR2', '2': '/path/to/IMG_3214.CR2', '3': '/path/to/IMG_3214.CR2'}`

    Arguments:
    conversion_file_path -- the path to the Siril img conversion file
    """

    conversion_map: dict[str, str] = {}

    with open(conversion_file_path, encoding="utf-8") as file:
        for line in file:
            cols = line.split("->")

            if len(cols) == 2:
                original_input_file_path = cols[0].strip().strip("'")
                converted_file_path = cols[1].strip().strip("'")

                img_id_match = re.search(r"_(\d+)\.fit$", converted_file_path)

                if img_id_match:
                    img_id = img_id_match.group(1).lstrip("0")
                    conversion_map[img_id] = original_input_file_path

    return conversion_map


def get_disabled_seq_imgs(seq_file_path: str, conversion_file_path: str):
    """
    Returns a list of file paths, representing the input imgs that are disabled in the provided
    Siril sequence.

    Arguments:
    seq_file_path -- the path to the seq file Siril
    conversion_file_path -- the path to the Siril img conversion file
    """

    disabled_imgs: list[str] = []

    seq_map = parse_seq_map(seq_file_path)
    conversion_map = parse_conversion_map(conversion_file_path)

    disabled_img_ids = list(
        filter(lambda img_key: not seq_map[img_key], seq_map.keys())
    )
    for img_id in disabled_img_ids:
        disabled_imgs.append(conversion_map[img_id])

    return disabled_imgs


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="""
        A simple tool to get the file paths of the disabled imgs in a Siril sequence.
        """
    )
    parser.add_argument(
        "-s",
        "--seq-file-path",
        dest="input_seq_file_path",
        help="the path to the Siril seq file",
        metavar="",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--conversion-file-path",
        dest="input_conversion_file_path",
        help="the path to the Siril conversion file",
        metavar="",
        required=True,
    )

    args = parser.parse_args()
    imgs = get_disabled_seq_imgs(args.input_seq_file_path, args.input_conversion_file_path)
    for img in imgs:
        print(img)

# Bad Pixels

Bad Pixels is a Python script that converts an image to greyscale and identifies pixel islands. An island is defined as a group of contiguous pixels with values less than 1. The script outputs an image with the islands highlighted in red and a detailed spreadsheet containing the coordinates including perimeter pixels of each island.

## Features

- Supports multiple image formats: BMP, TIFF, PNG, JPEG, and more.
- Outputs an image with highlighted pixel islands.
- Generates an Excel spreadsheet with detailed information about each island.

## Requirements

- Python 3.x
- Pillow library
- Pandas library

## Usage

Run the script with the path to your input image file:

```python bad_pixels.py path_to_your_image```

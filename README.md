# Table Recognition

This repository contains a Python script that can transform an image of a game board into a matrix of 81 equal squares.
## How it works

The script applies several image processing techniques to extract the numbers from the game board image and divide it into squares. Here's a summary of the steps:

1. Add a gray border to the original image to ensure that the contours are not lost at the edges.
2. Apply a GaussianBlur filter to smooth the image and reduce noise.
3. Find the contours in the image and select the largest one, which corresponds to the game board.
4. Divide the game board contour into a grid of 81 squares and extract the numbers from each square.
5. Concatenate the numbers into a single string and output it.

## Usage

To use the script, simply run the following command:

```
python table_recognition.py <path_to_image>
```

Replace `<path_to_image>` with the path to the image you want to process. The script will output the string of numbers extracted from the image.

## Limitations

The script works best with images that have a clear and consistent layout, such as Sudoku puzzles. It may not work well with images that have complex backgrounds or irregular shapes. In addition, the script assumes that the game board has exactly 81 squares arranged in a 9x9 grid. If the board has a different size or shape, the script may produce incorrect results.

## Credits

This script was created by Robert-Lucian Suto and is released under the MIT License.

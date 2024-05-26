import argparse
import os
import pandas as pd
from PIL import Image

def find_islands(image):
    """
    Identifies pixel islands in a grayscale image.
    
    Steps:
    1. Initialize an empty set `visited` to keep track of visited pixels.
    2. Initialize an empty list `islands` to store the information of identified islands.
    3. Iterate through each pixel in the image.
    4. For each pixel that hasn't been visited and has a value less than 1:
       a. Initialize an empty list `island` to store the coordinates of the island's pixels.
       b. Initialize an empty list `perimeter` to store the coordinates of the island's perimeter pixels.
       c. Call `dfs` to perform depth-first search starting from this pixel to find the entire island.
       d. Append the island's information (pixels and perimeter) to the `islands` list.
    5. Return the `islands` list.
    """
    def dfs(x, y, visited, image, island, perimeter):
        """
        Performs depth-first search to identify all connected pixels in an island.
        
        Steps:
        1. Initialize a stack with the starting pixel (x, y).
        2. Get the value of the starting pixel.
        3. Define the directions for moving up, down, left, and right.
        4. While the stack is not empty:
           a. Pop the top pixel (cx, cy) from the stack.
           b. If this pixel has not been visited:
              i. Mark it as visited.
              ii. Add it to the `island` list.
              iii. Initialize a flag `is_perimeter` to determine if the pixel is a perimeter pixel.
              iv. For each direction (dx, dy):
                  A. Calculate the new coordinates (nx, ny).
                  B. Check if the new coordinates are within the image bounds.
                  C. If the pixel (nx, ny) has not been visited:
                     - If the pixel value is different or greater than or equal to 1, mark `is_perimeter` as True.
                     - If the pixel value is the same, add it to the stack for further exploration.
                  D. If the new coordinates are out of bounds, mark `is_perimeter` as True.
              v. If `is_perimeter` is True, add the pixel to the `perimeter` list.
        """
        stack = [(x, y)]
        pixel_value = image[x][y]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) not in visited:
                visited.add((cx, cy))
                island.append((cx, cy))

                is_perimeter = False
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < len(image) and 0 <= ny < len(image[0]):
                        if (nx, ny) not in visited:
                            if image[nx][ny] != pixel_value or image[nx][ny] >= 1:
                                is_perimeter = True
                            elif image[nx][ny] == pixel_value:
                                stack.append((nx, ny))
                    else:
                        is_perimeter = True

                if is_perimeter:
                    perimeter.append((cx, cy))

    visited = set()
    islands = []

    for i in range(len(image)):
        for j in range(len(image[0])):
            if (i, j) not in visited and image[i][j] < 1:
                island = []
                perimeter = []
                dfs(i, j, visited, image, island, perimeter)
                if island:
                    islands.append({'pixels': island, 'perimeter': perimeter})

    return islands

def load_image(file_path):
    """
    Loads an image file and converts it to grayscale.
    
    Steps:
    1. Open the image file using PIL's Image.open.
    2. Convert the image to grayscale using convert('L').
    3. Get the pixel data as a flat list using getdata().
    4. Get the width and height of the image.
    5. Reshape the flat list of pixels into a 2D list (height x width).
    6. Return the grayscale image (PIL image object) and the 2D list of pixel values.
    """
    img = Image.open(file_path)
    img = img.convert('L')  # Convert image to grayscale
    pixels = list(img.getdata())
    width, height = img.size
    image = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return img, image

def save_image_with_islands(image, islands, output_path):
    """
    Saves an image with identified islands highlighted in red.
    
    Steps:
    1. Convert the grayscale image to RGB to modify colors.
    2. Load the pixel data for the image.
    3. For each island in the list of islands:
       a. For each pixel in the island:
          i. Change the pixel's color to red (255, 0, 0).
    4. Save the modified image to the specified output path.
    """
    image = image.convert('RGB')
    pixels = image.load()

    for island in islands:
        for y, x in island['pixels']:  # Note: coordinates are (y, x) in the island
            pixels[x, y] = (255, 0, 0)  # Set pixel to red

    image.save(output_path)

def save_islands_to_spreadsheet(islands, output_path):
    """
    Saves the details of identified islands to an Excel spreadsheet.
    
    Steps:
    1. Initialize an empty list `data` to store the information for each island.
    2. For each island in the list of islands:
       a. Get the number of pixels in the island.
       b. Format the coordinates of the pixels and the perimeter pixels as strings.
       c. Append the island's information (number, pixel coordinates, perimeter coordinates) to the `data` list.
    3. Create a DataFrame from the `data` list with appropriate column names.
    4. Save the DataFrame to an Excel file at the specified output path.
    """
    data = []
    for idx, island in enumerate(islands):
        num_pixels = len(island['pixels'])
        pixel_coords = '; '.join([f"({x}, {y})" for x, y in island['pixels']])
        perimeter_coords = '; '.join([f"({x}, {y})" for x, y in island['perimeter']])
        data.append([idx + 1, num_pixels, pixel_coords, perimeter_coords])

    df = pd.DataFrame(data, columns=['Island Number', 'Number of Pixels', 'Pixel Coordinates', 'Perimeter Coordinates'])
    df.to_excel(output_path, index=False)

def generate_output_paths(input_path):
    """
    Generates output file paths based on the input file name.
    
    Steps:
    1. Extract the base name of the input file (without extension).
    2. Append '_islands.png' to the base name for the output image path.
    3. Append '_islands.xlsx' to the base name for the output Excel path.
    4. Return the generated output image path and output Excel path.
    """
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_image_path = f"{base_name}_islands.png"
    output_excel_path = f"{base_name}_islands.xlsx"
    return output_image_path, output_excel_path

def main():
    """
    Main function to process the input image file, identify pixel islands,
    and save the results to an output image and an Excel spreadsheet.
    
    Steps:
    1. Parse the command line arguments to get the input file path.
    2. Generate output file paths for the image and Excel file.
    3. Check if output files already exist and prompt for overwrite confirmation if they do.
    4. Load the image and convert it to a grayscale 2D list.
    5. Identify pixel islands in the image.
    6. Save the image with islands highlighted to the output image path.
    7. Save the island details to an Excel spreadsheet at the output Excel path.
    8. Print the number of islands found and the paths of the output files.
    """
    parser = argparse.ArgumentParser(description="Find pixel islands in an image file (supports multiple formats).")
    parser.add_argument('file_path', type=str, help="Path to the image file (e.g., BMP, TIFF, PNG, JPEG).")
    args = parser.parse_args()

    output_image_path, output_excel_path = generate_output_paths(args.file_path)

    # Check if output files already exist and prompt for overwrite
    for path in [output_image_path, output_excel_path]:
        if os.path.exists(path):
            overwrite = input(f"{path} already exists. Do you want to overwrite it? (y/n): ")
            if overwrite.lower() != 'y':
                print("Operation cancelled.")
                return

    img, image = load_image(args.file_path)
    islands = find_islands(image)

    # Save image with islands highlighted
    save_image_with_islands(img, islands, output_image_path)
    
    # Save islands to spreadsheet
    save_islands_to_spreadsheet(islands, output_excel_path)
    
    # Print final message
    print(f"Found {len(islands)} islands :)")
    print(f"Output image saved to {output_image_path}")
    print(f"Output spreadsheet saved to {output_excel_path}")

if __name__ == "__main__":
    main()

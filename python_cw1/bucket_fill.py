""" Coursework 1: Bucket Fill
"""

def load_image(filename):
    """ Load image from file made of 0 (unfilled pixels) and 1 (boundary pixels) and 2 (filled pixel)

    Example of content of filename:

0 0 0 0 1 1 0 0 0 0
0 0 1 1 0 0 1 1 0 0
0 1 1 0 0 1 0 1 1 0
1 1 0 0 1 0 1 0 1 1
1 0 0 1 0 0 1 0 0 1
1 0 0 1 0 0 1 0 0 1
1 1 0 1 0 0 1 0 1 1
0 1 1 0 1 1 0 1 1 0
0 0 1 1 0 0 1 1 0 0
0 0 0 0 1 1 0 0 0 0

    Args:
        filename (str) : path to file containing the image representation

    Returns:
        list : a 2D representation of the filled image, where
               0 represents an unfilled pixel,
               1 represents a boundary pixel
               2 represents a filled pixel
    """

    image = []
    with open(filename) as imagefile:
        for line in imagefile:
            if line.strip():
                row = list(map(int, line.strip().split()))
                image.append(row)
    return image


def stringify_image(image):
    """ Convert image representation into a human-friendly string representation

    Args:
        image (list) : list of lists of 0 (unfilled pixel), 1 (boundary pixel) and 2 (filled pixel)

    Returns:
        str : a human-friendly string representation of the image
    """

    if image is None:
        return ""

    # The variable "mapping" defines how to display each type of pixel.
    mapping = {
        0: " ",
        1: "*",
        2: "0"
    }

    image_str = ""
    if image:
        image_str += "+ " + "- " * len(image[0]) + "+\n"
    for row in image:
        image_str += "| "
        for pixel in row:
            image_str += mapping.get(pixel, "?") + " "
        image_str += "|"
        image_str += "\n"
    if image:
        image_str += "+ " + "- " * len(image[0]) + "+\n"

    return image_str


def show_image(image):
    """ Show image in terminal

    Args:
        image (list) : list of lists of 0 (unfilled pixel), 1 (boundary pixel) and 2 (filled pixel)
    """
    print(stringify_image(image))



def fill(image, seed_point):
    """ Fill the image from seed point to boundary

    the image should remain unchanged if:
    - the seed_point has a non-integer coordinate
    - the seed_point is on a boundary pixel
    - the seed_point is outside of the image

    Args:
        image (list) : a 2D nested list representation of an image, where
                       0 represents an unfilled pixel, and
                       1 represents a boundary pixel
        seed_point (tuple) : a 2-element tuple representing the (row, col)
                       coordinates of the seed point to start filling

    Returns:
        list : a 2D representation of the filled image, where
               0 represents an unfilled pixel,
               1 represents a boundary pixel, and
               2 represents a filled pixel
    """
    # Check if the image is empty.
    if(not image):
        return image

    # Create variables for image width and height.
    image_width = len(image[0])
    image_height = len(image)
    # Create row and column variables.
    row = seed_point[0]
    col = seed_point[1]

    # Check that both coordinates of seed_point are integer.
    if(not(isinstance(row, int) and isinstance(col,int))):
        return image

    # Check if the seed_point lies within the bounds of the image.
    if(row >= image_height or row < 0 or col >= image_width or col < 0):
        return image

    # Check if the seed point lies on a boundary (i.e equal to 1).
    if(image[row][col] == 1):
        return image

    # Check that the current point is a zero to avoid infinite loop.
    if(image[row][col] == 0):
        image[row][col] = 2 # Fill point.

        image = fill(image, (row-1,col)) # Repeat for point to the left.

        image = fill(image, (row+1,col)) # Repeat for point to the right.

        image = fill(image, (row,col+1)) # Repeat for the point above.

        image = fill(image, (row,col-1)) # Repeat for the point below.

    return image



def example_fill():
    image = load_image("data/bar.txt")

    print("Before filling:")
    show_image(image)

    image = fill(image=image, seed_point=(1,1))

    print("-" * 25)
    print("After filling:")
    show_image(image)


if __name__ == '__main__':
    example_fill()

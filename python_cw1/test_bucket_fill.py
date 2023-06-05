from bucket_fill import fill
from bucket_fill import load_image
from bucket_fill import show_image

def test_pattern():
    test_image_1 = load_image("test_image_1.txt")
    test_image_1_result = load_image("test_image_1_result.txt")
    test_image_2 = load_image("test_image_2.txt")
    test_image_2_result = load_image("test_image_2_result.txt")
    test_image_3 = load_image("test_image_3.txt")
    test_image_3_result = load_image("test_image_3_result.txt")
    test_image_4 = load_image("test_image_4.txt")

    print("Testing on test image 1:")
    show_image(test_image_1)

    # First test case, normal fill example 25x25.
    print("Test 1: Normal fill example 25x25 image.")
    test_1_filled = fill(test_image_1, (10, 1))
    assert test_1_filled == test_image_1_result, "Test failed. Image filled incorrectly."
    print("Test 1: Passed.")

    # Second test cse, attempt to fill with see_pont out of bounds.
    print("Test 2: Attempt to fill with seed_point out of bounds.")
    test_2_filled = fill(test_image_1, (-1, -5))
    assert test_2_filled == test_image_1, "Test failed, original image not returned."
    print("Test 2: Passed.")

    # Third test case, non-integer seed_point
    print("Test 3: Attempt to fill with non-integer seed_point.")
    test_3_filled = fill(test_image_1, (0.1,1))
    assert test_3_filled == test_image_1, "Test failed, original image not returned."
    print("Test 3: Passed.")

    # Fourth test case, seed_point on edge.
    print("Test 4: Attempt to fill with seed_point on an edge.")
    test_4_filled = fill(test_image_1, (2, 3))
    assert test_4_filled == test_image_1, "Test failed, original image not returned."
    print("Test 4: Passed.")

    # Fifth test case, rectangular image test.
    print("Testing on image 2:")
    show_image(test_image_2)

    print("Test 5: Attempt to fill a rectangular image (3x11).")
    test_5_filled = fill(test_image_2, (1, 7))
    assert test_5_filled == test_image_2_result, "Test failed, Image filled incorrectly."
    print("Test 5: Passed.")

    # Sixth test case, test to ensure function fills hard to reach areas (spiral test).
    print("Testing on image 3:")
    show_image(test_image_3)

    print("Test 6: Attempt to fill a spiral image with \"hard to reach\" areas.")
    test_6_filled = fill(test_image_3, (2, 12))
    assert test_6_filled == test_image_3_result, "Test failed, Image filled incorrectly."
    print("Test 6: Passed.")

    # Seventh test case, test to ensure an fill function handeles empty image
    # correctly.
    print("Testing on image 4 (i.e empty image):")
    show_image(test_image_4)

    print("Test 7: Attempt to fill an empty image.")
    test_7_filled = fill(test_image_4, (0,0))
    assert test_7_filled == test_image_4, "Test failed, Unable to fill empty image."
    print("Test 7: Passed.")




if __name__ == '__main__':
    test_pattern()

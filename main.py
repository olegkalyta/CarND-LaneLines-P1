import os

from utils import *

files = os.listdir("test_images/")

# for file in files:
# img = mpimg.imread("test_images/" + file)
img = mpimg.imread("test_images/solidWhiteCurve.jpg")
gray = grayscale(img)
gray = gaussian_blur(gray, 3)
edges = canny(gray, 50, 180)

imshape = img.shape
vertices = np.array([[(.51 * imshape[1], imshape[0] * .58), (.49 * imshape[1], imshape[0] * .58), (0, imshape[0]),
                      (imshape[1], imshape[0])]], dtype=np.int32)
target = region_of_interest(edges, vertices)

lines = hough_lines(target, 1, np.pi / 180, 35, 5, 2)
result = weighted_img(lines, img, 0.9, 1)
r, g, b = cv2.split(result)
result = cv2.merge((b, g, r))

# cv2.imwrite("output_images/" + file, result)
cv2.imwrite("output_images/solidWhiteCurve.jpg", result)

    # plt.imshow(result, cmap='gray')

    # plt.colorbar()
    # plt.show()

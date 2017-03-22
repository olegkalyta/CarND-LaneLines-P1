import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2


def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def util_draw_line(img, lines, color):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, 2)


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    # print(len(lines))
    leftlines = []
    rightlines = []
    lc = []
    lm = []
    rc = []
    rm = []

    height, width, channels = img.shape
    print(height/2)

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            center = [(x1 + x2) / 2, (y1 + y2) / 2]

            if slope < 0 and slope > -2:
                lc.append(center)
                lm.append(slope)
                leftlines.append(line)
            else:
                if slope > 0 and slope < 2:
                    rightlines.append(line)
                    rc.append(center)
                    rm.append(slope)

    # util_draw_line(img, leftlines, [255, 0, 0])
    # util_draw_line(img, rightlines, [255, 255, 0])

    r_slope = np.sum(rm) / len(rm)
    l_slope = np.sum(lm) / len(lm)

    l_center = np.divide(np.sum(lc, axis=0), len(lc))
    r_center = np.divide(np.sum(rc, axis=0), len(rc))

    leftX, leftY = l_center
    rightX, rightY = r_center

    lefty1 = - (l_slope*(leftX - 480) - leftY)
    lefty2 = - (l_slope*(leftX - 150) - leftY)

    int_lefty1 = int(round(lefty1))
    int_lefty2 = int(round(lefty2))


    righty1 = - (r_slope*(rightX - 480) - rightY)
    righty2 = - (r_slope*(rightX - 900) - rightY)

    int_righty1 = int(round(righty1))
    int_righty2 = int(round(righty2))

    # arr = np.array([[(540, lefty1), (250, lefty2)]], dtype=np.int32)

    # print((540, lefty1), (250, lefty2))
    cv2.line(img, (480, int_lefty1), (150, int_lefty2), [255, 0, 255], 15)
    cv2.line(img, (480, int_righty1), (900, int_righty2), [255, 0, 255], 15)

    # print((480, int_righty1), (900, int_righty2))


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img


# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)

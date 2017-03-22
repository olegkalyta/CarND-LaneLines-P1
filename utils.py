import cv2


def makeblurgray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel_size = 5
    return cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

def canny(image):
    low_threshold = 50
    high_threshold = 250
    return cv2.Canny(image, low_threshold, high_threshold)


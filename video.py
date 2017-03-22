# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML

from utils import *


def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)

    gray = grayscale(image)
    gray = gaussian_blur(gray, 3)
    edges = canny(gray, 50, 180)

    imshape = image.shape
    vertices = np.array([[(.51 * imshape[1], imshape[0] * .58), (.49 * imshape[1], imshape[0] * .58), (0, imshape[0]),
                          (imshape[1], imshape[0])]], dtype=np.int32)
    target = region_of_interest(edges, vertices)

    lines = hough_lines(target, 1, np.pi / 180, 35, 5, 2)
    result = weighted_img(lines, image, 0.9, 1)

    return result

white_output = 'test_videos_output/solidWhiteRight.mp4'
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
white_clip.write_videofile(white_output, audio=False)

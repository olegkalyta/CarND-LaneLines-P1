#**Finding Lane Lines on the Road** 

##Writeup Template

###You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ../CarND-LaneLines-P1_loaded/examples/grayscale.jpg "Grayscale"

---

### Reflection

###1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. 
- I converted the images to grayscale, 
- I used gaussian blur to prepare image for Canny algorithm
- Used Canny algorithm to array of edges
- Then I cut image to get region of interest only
- I used Hough lines algorithm with own draw_lines function to get extrapolated lane lines

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...
I went through video `Self-Driving Car Project Q&A | Finding Lane Lines`.
So i divided lines into 2 arryas: left & right lane lines.
Then i calculated average center & slope of each group and used it in calculationg y1,y2:
`y-y1=M(x-x1)`. I found y1 as `y1 = - (M(x-x1) + y)`, where M is slope, x,y - center of line, y1 - left/right edge of road.

###2. Identify potential shortcomings with your current pipeline

One potential shortcoming would be what would happen when car drives on sharp turn road, my algorithm work not very good on challenge.mpg 

###3. Suggest possible improvements to your pipeline

A possible improvement would be to optimize speed of overall pipeline. Not sure it's fast enough to work with high-res video in real-time

Another potential improvement could be to calculate more smartly height of image, that i use in `draw_line()` function
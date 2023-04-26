
## The Car

![alt text](https://github.com/kunwarsingh55/Self-Driving-Car/blob/main/Images/Car.JPG?raw=true)

# Autonomous Driving

**Engineering** and **conceptualize** basics of a self driving car

# Method for Lane Detection

We are going to use **pixel summation** for finding the lane **curve**. To find curve of the path summation of pixels is done.

![Untitled](https://github.com/kunwarsingh55/Self-Driving-Car/blob/main/Images/Untitled.png?raw=true)

Idea is that we are summing up  pixels in each column

> **Black** → 0
> 

> **White** → 255
> 

<aside>
💡 Because we are using 8-bit unsigned integers that is $2^6$ which is 256 values for each pixel [0-255]

</aside>

Image will be binary - black and white

So, 0 will be black and 255 will be white and in between we will have shades of Gray.

Now by summing up each column we will be able to tell the curve

Example here, we have more white pixels on left hand side so our curve will be on the left.

# Libraries

```jsx
import cv2 //opencv-python
import numpy //numpy
```

**OpenCV** (Open Source Computer Vision Library) is an open source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in the commercial products

**NumPy** is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays

Since we are creating a **module** and we want to run it as a **standalone script** as well we will add the if statement to check the file name. 

If this is the main module that was run then we will grab frame from our video and call the main function. In this case we will call the main function `getLaneCurve` since that is what we are interested in.

# Finding Lane

There will be 5 steps to find the lane curve

Thresholding

Warping

Summation of pixels

Averring

Display

## Step 1 - Thresholding

Now the idea here is to get the path using either **`Color`** or Edge Detection. In our case we are using regular A4 White paper as path, therefore we can simply use the **`color`** detection to find the path. We will write the Thresholding function in the `Utilitis` file.

![Untitled](https://github.com/kunwarsingh55/Self-Driving-Car/blob/main/Images/Untitled.png?raw=true)

Image that we are using is **black** and **white** 

Wherever we have the **lane** is white and what ever is the **background** is black.

We will perform **thresholding** based on colour. Because we know our **path is white pixels**.

<aside>
💡 For advanced lane detection we can use edge detectors like canny edge detector

</aside>

> For now we have controlled environment, so we will keep it simple and use colour.
> 

### Converting image to HSV colour model

```jsx
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

**HSV colour space** is consists of 3 matrices, **'hue'**, **'saturation'** and **'value'**. 

In OpenCV, value range for 'hue', 'saturation' and 'value' are respectively 0-179, 0-255 and 0-255. 

'**Hue**' represents the colour,

'**Saturation**' represents the amount to which that respective colour is mixed with white 

'**Value**' represents the amount to which that respective colour is mixed with black.

<aside>
💡 HSV is suitable colour space for colour based image segmentation

</aside>

## Creating Mask

```python
#define color bounds
lowerWhite = np.array([0,0,0])
upperWhite = np.array([179, 255, 255])

#create mask from above values
maskWhite = cv2.inRange(imgHSV, lowerWhite, upperWhite)
```

After calling cv2.inRange, a binary mask is returned, where white pixels (255) represent pixels that fall into

It is very difficult to change mask values each time and then sun script to see the change, to find the optimal values for **upper** and **lower** bound we **have to try values in real-time** to quickly see the the results this can be done using **trackbars** 

**Trackbars** change values in **real-time** we can see results right away.

![Untitled](https://github.com/kunwarsingh55/Self-Driving-Car/blob/main/Images/Untitled 1.png?raw=true)

## STEP 2 - Warping

This helps to change an image from angled perspective to a birds eye view

![Untitled](https://github.com/kunwarsingh55/Self-Driving-Car/blob/main/Images/Untitled 2.png?raw=true)

Why do we need it ?

If we look at road from tilted angle it is difficult to determine how much the curve is, if you are looking from the top it will be much easier to tell.

To do the we are going to use warm image function in OpenCV

```python
def warpImg(img, points, w, h):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    return imgWarp
```

# . . . .

pts1 pts2 

**`pts1`** are the original points (on the left) 

**`pts2`** are the points we want them to be by warping them image (on the right)

To relate these two points we create a **transformation matrix**

Transformation matrix is **a matrix that transforms one vector into another by process of matrix multiplication**

Can be done using function `**getPrespectiveTransform()**`

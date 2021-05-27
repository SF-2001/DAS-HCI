import matplotlib.pyplot as plt
import cv2
import numpy as np

image = cv2.imread('pic1.jpg')
image = cv2.resize(image,(800,600))
image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

height = image.shape[0]
width = image.shape[1]

region_of_interest_vertices = [
    (0,height),
    (width/2, height/2),
    (width,height)
]

def region_of_interest(img,vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img,mask)
    return masked_image

def draw_lines(img,lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0],img.shape[1], 3),dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blank_image,(x1,y1),(x2,y2),(255,0,0),thickness=3)

    merged_img = cv2.addWeighted(img, 0.8,blank_image,1,0.0)
    return merged_img


gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
canny_image = cv2.Canny(gray_image,100,200)
masked_img = region_of_interest(canny_image,
                                np.array([region_of_interest_vertices],np.int32))
lines = cv2.HoughLinesP(masked_img,rho=6,theta=np.pi/60,threshold=160,lines=np.array([]),minLineLength=40,maxLineGap=25)

image_with_lines = draw_lines(image,lines)

plt.imshow(image_with_lines)
plt.show()



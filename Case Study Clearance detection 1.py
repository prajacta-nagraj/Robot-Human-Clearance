#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2


# Loading the given Imagefile.

# In[2]:


env1 = np.loadtxt('human_corridor_0.txt')


# In[3]:


env1


# In[4]:


img=env1


# In[5]:


import matplotlib.pyplot as plt


# In[6]:


plt.imshow(img)


# Applying erosion, dilation to clean the image.

# In[7]:


kernel = np.ones((5,5),np.float32)/25
plt.rcParams['image.cmap'] = 'jet' 
mask=cv2.inRange(img,0, 255)
erosion =cv2.erode(img, kernel, iterations=1)
dil =cv2.dilate(erosion, kernel, iterations=1)
plt.imshow(dil)


# Thresholding the image to get a clear view of human.

# In[8]:


ret1, thresh1 = cv2.threshold(dil, 5, 10, 0)
plt.imshow(thresh1)


# Applying canny edge detection.

# In[9]:


Copy = np.uint8(thresh1)
canny = cv2.Canny(Copy,3,5)
plt.imshow(canny),plt.title('Canny')


# Seperating human contour from base.

# In[10]:


canny=cv2.dilate(canny, kernel, iterations=2)
canny=cv2.erode(canny, kernel, iterations=2)
plt.imshow(canny)


# Crop required area ( Assumption- same lobby corridor.)

# In[11]:


cropped = np.zeros((canny.shape[0], canny.shape[1]), dtype=np.uint8)
cropped[30:110,65:115]=canny[30:110,65:115]
ret,thresh = cv2.threshold(cropped,127,255,cv2.THRESH_BINARY)


# In[12]:


plt.imshow(thresh)


# Applying contour detection and filtering contours using hierarchy.
# Bounding box for final contour.

# In[13]:


im2, contours, hierarchy = cv2.findContours(cropped,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
max_area=0
human=0
hierarchy = hierarchy[0] 

for component in zip(contours, hierarchy):
    Contour = component[0]
    Hierarchy = component[1]
    
    if Hierarchy[2] < 0:
        a=component
        area=cv2.contourArea(a[0]) 
        print(area)
        if (area>max_area):
            max_area=area
            human=a[0]
x, y, w, h = cv2.boundingRect(human)
kk=cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
print (x, y),(x+w, y+h)            
plt.imshow(kk)


# In[14]:


x-3,y,w,h


# Using the co-ordinates of bounding box calculating clearance for the robot.( +- 3 for feet clearance)

# In[15]:


left = x-60-3
right = 120-(x+w+3)
if (left >right):
    print("left",left*1.5/60)
else: 
    print("right",right*1.5/60)


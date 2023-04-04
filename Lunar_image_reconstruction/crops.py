import cv2
image = cv2.imread("moon.png")
print(image.shape)

y=2
x=2
h=300
w=510
crop_image = image[x:w, y:h]
print(crop_image.shape)
cv2.imshow("Cropped", crop_image)
cv2.waitKey(0)
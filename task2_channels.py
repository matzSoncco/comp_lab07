import cv2
import numpy as np

img1 = cv2.imread('output/resized1_person.jpg')
img2 = cv2.imread('output/resized2_dog.jpg')
img3 = cv2.imread('output/resized3_cat.jpg')

# OpenCV stores channels as BGR
b1, g1, r1 = cv2.split(img1)
b2, g2, r2 = cv2.split(img2)
b3, g3, r3 = cv2.split(img3)

# New image: R from img1 (person), G from img2 (dog), B from img3 (cat)
combined = cv2.merge([b3, g2, r1])

cv2.imwrite('output/combined_channels.jpg', combined)
print("Saved -> output/combined_channels.jpg")
print(f"  R channel: person image")
print(f"  G channel: dog image")
print(f"  B channel: cat image")

# Show source and result
zeros = np.zeros_like(r1)
only_r = cv2.merge([zeros, zeros, r1])
only_g = cv2.merge([zeros, g2,    zeros])
only_b = cv2.merge([b3,    zeros, zeros])

top = np.hstack([img1, img2, img3])
bot = np.hstack([only_r, only_g, only_b])

cv2.imshow('Sources: person | dog | cat', top)
cv2.imshow('Channels used: R(person) | G(dog) | B(cat)', bot)
cv2.imshow('Combined result', combined)
cv2.waitKey(0)
cv2.destroyAllWindows()

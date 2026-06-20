import cv2
import numpy as np

# Step 1 – load combined channels image and invert every pixel value
combined = cv2.imread('output/combined_channels.jpg')

negative = 255 - combined

cv2.imwrite('output/negative.png', negative)
print("Saved -> output/negative.png  (color negative)")

# Step 2 – open the negative in grayscale and save
gray = cv2.imread('output/negative.png', cv2.IMREAD_GRAYSCALE)

cv2.imwrite('output/grayscale.png', gray)
print("Saved -> output/grayscale.png  (grayscale)")

# Display
cv2.imshow('Original combined', combined)
cv2.imshow('Negative (inverted)', negative)
cv2.imshow('Grayscale of negative', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

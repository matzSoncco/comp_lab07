import cv2

img1 = cv2.imread('images/person.jpg')
img2 = cv2.imread('images/dog.jpg')
img3 = cv2.imread('images/cat.jpg')

h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]
h3, w3 = img3.shape[:2]

print(f"Original sizes -> person: {w1}x{h1}  dog: {w2}x{h2}  cat: {w3}x{h3}")

max_w = max(w1, w2, w3)
max_h = max(h1, h2, h3)
print(f"Target size (largest): {max_w}x{max_h}")

resized1 = cv2.resize(img1, (max_w, max_h), interpolation=cv2.INTER_LINEAR)
resized2 = cv2.resize(img2, (max_w, max_h), interpolation=cv2.INTER_LINEAR)
resized3 = cv2.resize(img3, (max_w, max_h), interpolation=cv2.INTER_LINEAR)

cv2.imwrite('output/resized1_person.jpg', resized1)
cv2.imwrite('output/resized2_dog.jpg', resized2)
cv2.imwrite('output/resized3_cat.jpg', resized3)
print("Saved -> output/resized1_person.jpg, resized2_dog.jpg, resized3_cat.jpg")

# Display all three side by side
import numpy as np
row = np.hstack([resized1, resized2, resized3])
cv2.imshow('Resized images (same size)', row)
cv2.waitKey(0)
cv2.destroyAllWindows()

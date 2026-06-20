import cv2
import numpy as np

img_color = cv2.imread('images/person.jpg')
img_gray  = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# Binary threshold: pixels >= 127 become 255 (white), the rest become 0 (black)
threshold_value = 127
_, binary = cv2.threshold(img_gray, threshold_value, 255, cv2.THRESH_BINARY)

cv2.imwrite('output/binary_threshold.png', binary)
print(f"Saved -> output/binary_threshold.png  (threshold={threshold_value})")

# Also save the grayscale source for comparison
cv2.imwrite('output/gray_source.png', img_gray)

# Interactive: slider lets you explore different threshold values
def nothing(x):
    pass

cv2.namedWindow('Threshold Explorer')
cv2.createTrackbar('Threshold', 'Threshold Explorer', threshold_value, 255, nothing)

while True:
    t = cv2.getTrackbarPos('Threshold', 'Threshold Explorer')
    _, thresh = cv2.threshold(img_gray, t, 255, cv2.THRESH_BINARY)

    side = np.hstack([img_gray, thresh])
    cv2.imshow('Threshold Explorer', side)

    key = cv2.waitKey(30) & 0xFF
    if key in (ord('q'), 27):
        break
    if key == ord('s'):
        cv2.imwrite('output/binary_threshold.png', thresh)
        print(f"Saved current threshold ({t}) -> output/binary_threshold.png")

cv2.destroyAllWindows()

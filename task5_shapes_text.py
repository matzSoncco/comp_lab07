import cv2
import numpy as np

img = cv2.imread('images/person.jpg')
output = img.copy()

# The synthetic person's face is centered at approximately (200, 150)
# with axes ~75x90 px – a radius of 95 covers it comfortably
face_center = (200, 150)
face_radius = 95

# Draw green circle around the face
cv2.circle(output, face_center, face_radius, (0, 220, 0), 3)

# Add label above the circle
label = 'Person'
font = cv2.FONT_HERSHEY_SIMPLEX
text_x = face_center[0] - 40
text_y = face_center[1] - face_radius - 12
cv2.putText(output, label, (text_x, text_y), font, 1.0, (0, 0, 0), 4)   # black shadow
cv2.putText(output, label, (text_x, text_y), font, 1.0, (0, 220, 0), 2) # green text

cv2.imwrite('output/labeled_person.jpg', output)
print("Saved -> output/labeled_person.jpg")

cv2.imshow('Original', img)
cv2.imshow('Labeled with circle', output)
cv2.waitKey(0)
cv2.destroyAllWindows()

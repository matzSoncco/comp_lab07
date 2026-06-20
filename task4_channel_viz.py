import cv2
import numpy as np

img = cv2.imread('output/combined_channels.jpg')
b_ch, g_ch, r_ch = cv2.split(img)

show_r = True
show_g = True
show_b = True

WINDOW = 'Channel Visualizer  |  R=toggle red  G=toggle green  B=toggle blue  Q=quit'
cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)

while True:
    zeros = np.zeros_like(r_ch)

    r_out = r_ch if show_r else zeros
    g_out = g_ch if show_g else zeros
    b_out = b_ch if show_b else zeros

    frame = cv2.merge([b_out, g_out, r_out])

    # Burn a small status bar at the bottom
    status = np.zeros((30, frame.shape[1], 3), dtype=np.uint8)
    label = (f"[R] {'ON ' if show_r else 'OFF'}   "
             f"[G] {'ON ' if show_g else 'OFF'}   "
             f"[B] {'ON ' if show_b else 'OFF'}")
    cv2.putText(status, label, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 255), 1)
    display = np.vstack([frame, status])

    cv2.imshow(WINDOW, display)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('r'):
        show_r = not show_r
        print(f"Red channel: {'ON' if show_r else 'OFF'}")
    elif key == ord('g'):
        show_g = not show_g
        print(f"Green channel: {'ON' if show_g else 'OFF'}")
    elif key == ord('b'):
        show_b = not show_b
        print(f"Blue channel: {'ON' if show_b else 'OFF'}")
    elif key in (ord('q'), 27):
        break

cv2.destroyAllWindows()

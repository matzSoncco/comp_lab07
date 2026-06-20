import cv2
import numpy as np

# ── Canvas & state ────────────────────────────────────────────────────────────
CANVAS_W, CANVAS_H = 800, 600
canvas   = np.full((CANVAS_H, CANVAS_W, 3), 255, dtype=np.uint8)
history  = []          # undo stack (list of canvas copies)
shape    = 'rectangle' # current shape: rectangle | circle | line | freehand
color    = (0, 0, 0)   # BGR
thickness = 2

drawing  = False
start_x  = start_y = -1
preview  = canvas.copy()  # temporary layer shown while dragging

COLORS = {
    ord('1'): ((0,   0,   0),   'Black'),
    ord('2'): ((0,   0, 255),   'Red'),
    ord('3'): ((0, 255,   0),   'Green'),
    ord('4'): ((255, 0,   0),   'Blue'),
    ord('5'): ((0, 200, 255),   'Yellow'),
    ord('6'): ((255, 0, 255),   'Magenta'),
}

def draw_shape(img, s, x1, y1, x2, y2, col, thick):
    if s == 'rectangle':
        cv2.rectangle(img, (x1, y1), (x2, y2), col, thick)
    elif s == 'circle':
        r = int(np.hypot(x2 - x1, y2 - y1))
        cv2.circle(img, (x1, y1), r, col, thick)
    elif s == 'line':
        cv2.line(img, (x1, y1), (x2, y2), col, thick)

def status_bar(img, shape, color, thickness):
    bar = np.full((36, img.shape[1], 3), 40, dtype=np.uint8)
    shape_map = {'r': 'rectangle', 'c': 'circle', 'l': 'line', 'f': 'freehand'}
    keys_hint = ('[R]rect [C]circ [L]line [F]free | '
                 '[1-6]color | [+/-]thick | [Z]undo | [S]save | [ESC]quit')
    cv2.putText(bar, f'Shape:{shape}  Thick:{thickness}  {keys_hint}',
                (6, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 200, 200), 1)
    swatch = np.full((20, 20, 3), color, dtype=np.uint8)
    bar[8:28, img.shape[1] - 30: img.shape[1] - 10] = swatch
    return np.vstack([img, bar])

# ── Mouse callback ─────────────────────────────────────────────────────────────
def on_mouse(event, x, y, flags, param):
    global drawing, start_x, start_y, canvas, preview

    if event == cv2.EVENT_LBUTTONDOWN:
        history.append(canvas.copy())
        drawing = True
        start_x, start_y = x, y
        preview = canvas.copy()

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        if shape == 'freehand':
            cv2.line(canvas, (start_x, start_y), (x, y), color, thickness)
            start_x, start_y = x, y
        else:
            preview_frame = canvas.copy()
            draw_shape(preview_frame, shape, start_x, start_y, x, y, color, thickness)
            cv2.imshow(WINDOW, status_bar(preview_frame, shape, color, thickness))

    elif event == cv2.EVENT_LBUTTONUP and drawing:
        drawing = False
        if shape != 'freehand':
            draw_shape(canvas, shape, start_x, start_y, x, y, color, thickness)

WINDOW = 'Drawing Program'
cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(WINDOW, on_mouse)

print("Controls:")
print("  R/C/L/F  – select shape (rectangle / circle / line / freehand)")
print("  1-6      – change color")
print("  + / -    – increase / decrease line thickness")
print("  Z        – undo last action")
print("  S        – save drawing to output/drawing.png")
print("  ESC      – quit")

while True:
    cv2.imshow(WINDOW, status_bar(canvas, shape, color, thickness))
    key = cv2.waitKey(20) & 0xFF

    if   key == ord('r'): shape = 'rectangle'; print('Shape: rectangle')
    elif key == ord('c'): shape = 'circle';    print('Shape: circle')
    elif key == ord('l'): shape = 'line';      print('Shape: line')
    elif key == ord('f'): shape = 'freehand';  print('Shape: freehand')
    elif key in COLORS:
        color, name = COLORS[key]
        print(f'Color: {name}')
    elif key == ord('+') or key == ord('='):
        thickness = min(thickness + 1, 30)
        print(f'Thickness: {thickness}')
    elif key == ord('-'):
        thickness = max(thickness - 1, 1)
        print(f'Thickness: {thickness}')
    elif key == ord('z'):
        if history:
            canvas = history.pop()
            print('Undo')
        else:
            print('Nothing to undo')
    elif key == ord('s'):
        import os; os.makedirs('output', exist_ok=True)
        cv2.imwrite('output/drawing.png', canvas)
        print('Saved -> output/drawing.png')
    elif key == 27:  # ESC
        break

cv2.destroyAllWindows()

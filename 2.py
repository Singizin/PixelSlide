import cv2
import numpy as np

img = cv2.imread(r'G:\PyProject\PixelSlide\img\1.JPG')
mask = np.zeros(img.shape, np.uint8)
koef = 4
img_res = cv2.resize(img, (img.shape[1] // koef, img.shape[0] // koef))
mask_res = cv2.resize(mask, (img.shape[1] // koef, img.shape[0] // koef))

drawing = False  # true if mouse is pressed
mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1
pressed = False

h, w = img.shape[0] // koef, img.shape[1] // koef
k, b = 0, 0
last = ((0, 0), (h, w))
print(h, w)

class Frame:
    def __init__(self, h, w):
        self.top = 0, 0, w, 0
        self.bot = 0, h, w, h
        self.left = 0, 0, 0, h
        self.right = w, 0, w, h


F = Frame(w,h)


# mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, k, b

    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        if mode == True:
            cv2.line(mask_res, (ix, iy), (x, y), (255, 255, 255), 2)
            print((ix, iy), ' ', (x, y))
            k, b = equation((ix, iy), (x, y))


def equation(xy1, xy2):
    x1 = xy1[0]
    y1 = xy1[1]
    x2 = xy2[0]
    y2 = xy2[1]
    k = (y1 - y2) / (x1 - x2)
    b = y2 - k * x2
    print(k, b)
    return k, b


def endpoint(start, k, b):
    x0, y0 = start
    x_end = w
    for i in range(0, x_end - x0):
        y_end = i * k
        return i, y_end


def crossing(p1, p2,
             line_frame):
    x1_1, y1_1 = p1
    x1_2, y1_2 = p2
    x2_1, y2_1, x2_2, y2_2 = line_frame
    print(p1, p2)
    print(line_frame)
    # составляем формулы двух прямых
    A1 = y1_1 - y1_2
    B1 = x1_2 - x1_1
    C1 = x1_1 * y1_2 - x1_2 * y1_1
    A2 = y2_1 - y2_2
    B2 = x2_2 - x2_1
    C2 = x2_1 * y2_2 - x2_2 * y2_1
    # решаем систему двух уравнений
    if B1 * A2 - B2 * A1 != 0:
        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C1 - B1 * y) / A1
        # проверяем, находится ли решение системы (точка пересечения) на первом отрезке, min/max - потому
        # что координаты точки могут быть заданы не по порядку возрастания
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2) and \
                min(y1_1, y1_2) <= y <= max(y1_1, y1_2):
            print('Точка пересечения отрезков есть, координаты: ({0:f}, {1:f}).'.
                  format(x, y))
        else:
            print('Точки пересечения отрезков нет.')
    # случай деления на ноль, то есть параллельность
    if B1 * A2 - B2 * A1 == 0: print('Точки пересечения отрезков нет, отрезки ||.')


def doit(mask_res, img_res):
    for i in range(h):
        for j in range(w):
            if mask_res[i][j][0] == 255:
                img_res = cv2.line(img_res, (j, i), endpoint((j, i), k, b),
                                   img_res[i][j].tolist(), 1)
                crossing((j, i), endpoint((j, i), k, b), F.right)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while 1:
    cv2.imshow('image', img_res)
    cv2.imshow('mask', mask_res)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        doit(mask_res, img_res)
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()

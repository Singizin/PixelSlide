import numpy as np
import cv2


img = cv2.imread(r'G:\PyProject\PixelSlide\img\1.JPG')
mask = cv2.imread(r'G:\PyProject\PixelSlide\img\1_mask.png')

h, w, channels = img.shape
m_h, m_w, m_channels = mask.shape
print(h, w, channels)
print(m_h, m_w, m_channels)

resized = cv2.resize(img, (w, h))
resized_mask = cv2.resize(mask, (w, h))
'''
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ",", y)

        mask = np.zeros((h, w, 1), np.uint8)
        mask[:] = 0
        cv2.rectangle(mask, (x, y), (x + 10, y + 10), 255, -1)

for i in range(h):
    for j in range(w):
        if resized_mask[i][j][0] != 255:
            resized = cv2.line(resized, (j, i), (j+100, i+100), resized[i][j].tolist(), 1)

'''
def on_mouse(event, x, y, flags, params):
    if event == cv2.CV_EVENT_LBUTTONDOWN:
        print('Start Mouse Position: '+str(x)+', '+str(y))
        sbox = [x, y]
        boxes.append(sbox)
    elif event == cv2.CV_EVENT_LBUTTONUP:
        print('End Mouse Position: '+str(x)+', '+str(y))
        ebox = [x, y]
        boxes.append(ebox)

count = 0
while(1):
    count += 1
    img = cv2.blur(img, (3,3))

    cv2.namedWindow('real image')
    cv2.SetMouseCallback('real image', on_mouse, 0)
    cv2.imshow('real image', img)

    if count < 50:
        if cv2.waitKey(33) == 27:
            cv2.destroyAllWindows()
            break
    elif count >= 50:
        if cv2.waitKey(0) == 27:
            cv2.destroyAllWindows()
            break
        count = 0








cv2.imshow('dst', cv2.resize(resized, (w//4, h//4)))
cv2.waitKey(0)
cv2.destroyAllWindows()

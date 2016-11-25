import cv2
import numpy as np

colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0),
          (255, 255, 255), (255, 255, 0), (255, 102, 0)]
names = ['b', 'r', 'g', 'w', 'y', 'o']
avg_colors = []
name_dict = {}
color_dict = {}
for a, c1 in zip(names, colors):
    for b, c2 in zip(names, colors):
        for c, c3 in zip(names, colors):
            for d, c4 in zip(names, colors):
                avg_color = [0, 0, 0]
                for i in xrange(3):
                    x = c1[i] + c2[i] + c3[i] + c4[i]
                    avg_color[i] = x / 4
                avg_colors.append(tuple(reversed(avg_color)))
                name_dict[tuple(reversed(avg_color))] = a + b + c + d
                color_dict[tuple(reversed(avg_color))] = (c1, c2, c3, c4)


img = np.zeros((36, 36, 3), dtype=np.uint8)
for i, c in enumerate(avg_colors):
    img[i % 36, i/36] = c

cv2.imwrite('img.png', img)

def color_diff(c1, c2):
    diff = 0
    for (x, y) in zip(c1, c2):
        diff += (x - y) * (x - y)
    return diff

def nearest_color(c, many=True):
    min_diff = float('inf')
    min_c = None
    cs = avg_colors if many else colors
    for x in cs:
        diff = color_diff(x, c)
        if diff < min_diff:
            min_diff = diff
            min_c = x
    return min_c

number_of_pixels = 0

img = cv2.imread('cherry_blossums_2.png', flags=cv2.CV_LOAD_IMAGE_COLOR)
w = img.shape[0]
h = img.shape[1]
img1 = img.copy()
img2 = img.copy()
img3 = np.zeros((w * 2, h * 2, 3), dtype=np.uint8)
with open('colors.txt', 'w') as f:
    for i in xrange(w):
        f.write('\n')
        for j in xrange(h):
            c1 = nearest_color(img[i, j])
            c2 = nearest_color(img[i, j], many=False)
            if c1 != (255, 255, 255):
                number_of_pixels += 1
            f.write(str(name_dict[c1]) + ' ')
            img1[i, j] = c1
            img2[i, j] = c2
            img3[i * 2 + 0, j * 2 + 0] = tuple(reversed(color_dict[c1][0]))
            img3[i * 2 + 1, j * 2 + 0] = tuple(reversed(color_dict[c1][1]))
            img3[i * 2 + 0, j * 2 + 1] = tuple(reversed(color_dict[c1][2]))
            img3[i * 2 + 1, j * 2 + 1] = tuple(reversed(color_dict[c1][3]))
    print number_of_pixels, number_of_pixels * (2.0 / 3.0)**2, number_of_pixels / 9
    print w * (2.0/3.0), h * (2.0 / 3.0), w * (2.0/3.0) * h * (2.0 / 3.0)
    print w * (1.0/3.0), h * (1.0 / 3.0), w * (1.0/3.0) * h * (1.0 / 3.0)
    cv2.imwrite('new_img.png', img1)
    cv2.imwrite('new_img_2.png', img2)
    cv2.imwrite('new_img_3.png', img3)

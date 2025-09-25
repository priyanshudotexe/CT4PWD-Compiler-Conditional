import cv2
import numpy as np

def identify_color(b, g, r):
    if r > 150 and g < 100 and b < 100:
        return 'red'
    elif g > 150 and r < 100 and b < 100:
        return 'green'
    elif b > 150 and r < 100 and g < 100:
        return 'blue'
    else:
        return None

def extract_colors_after_qr(img, qr_x=None):
    height, width, _ = img.shape
    strip_width = 10
    
    # If no QR is found, start from the beginning of the image
    if qr_x is None:
        x = 0
    else:
        x = qr_x + 5  # Start after the QR code

    color_sequence = []
    prev_color = None

    while x < width:
        strip = img[0:height, x:x+strip_width]
        avg_color = strip.mean(axis=0).mean(axis=0)  # BGR
        b, g, r = avg_color
        color = identify_color(b, g, r)

        if color and color != prev_color:
            color_sequence.append(color)
            prev_color = color

        x += strip_width

    return color_sequence

import subprocess
import cv2
from copy import deepcopy
import numpy as np
from scripts.general_purpose import get_secret

TESS_DATA_DIR = get_secret("TESS_DATA_DIR")


DEFAULT_IMAGE_PATH = "/home/denny_k/Documents/work/puller_blueprints_ocr/needed_tables/5.png"


def remove_lines(img_path):
    """
    Removes all lines on image and save it as separate image

    :param img_path: path ro image
    :type img_path: str
    """
    img = cv2.imread(img_path)
    img_height = img.shape[0]
    img_width = img.shape[1]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 10)

    gray = cv2.erode(gray, (3, 3), iterations=1)
    bw = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(bw, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

    horizontal = bw
    vertical = bw

    horizontal_scale = 10
    vertical_scale = 10
    if img_width/img_height > 3.5:
        vertical_scale = 3

    horizontalsize = int(horizontal.shape[1] / horizontal_scale)

    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))

    horizontal = cv2.erode(horizontal, horizontal_structure, (-1, -1))
    horizontal = cv2.dilate(horizontal, horizontal_structure, (-1, -1))

    vertical_size = int(vertical.shape[0] / vertical_scale)

    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))

    vertical = cv2.erode(vertical, vertical_structure, (-1, -1))
    vertical = cv2.dilate(vertical, vertical_structure, (-1, -1))

    img_without_lines = img

    mask = horizontal + vertical

    whiteImg = np.zeros(img_without_lines.shape, img_without_lines.dtype)
    whiteImg[:, :] = (255, 255, 255)
    whiteMask = cv2.bitwise_and(whiteImg, whiteImg, mask=mask)

    kernel = np.ones((5, 5), np.uint8)
    whiteMask = cv2.dilate(whiteMask, kernel, iterations=1)

    cv2.addWeighted(whiteMask, 1, img_without_lines, 1, 0, img_without_lines)

    cv2.imwrite(img_path.split(".")[0] + "_no_lines.png", img_without_lines)

def table_cells_cropper(img_path=DEFAULT_IMAGE_PATH, cropped_img_dir="/home/denny_k/Documents/work/puller_blueprints_ocr/needed_tables/cropped/"):
    """
    Find table cells on given image, crop them into separate images and save them. Also, calculate some params for each image

    :param img_path:
    :param cropped_img_dir:
    :return: cropped_img_list - list of cropped img params
    :rtype: list
    """

    # Image preparation
    img = cv2.imread(img_path)
    img_height = img.shape[0]
    img_width = img.shape[1]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 10)

    gray = cv2.erode(gray, (3, 3), iterations=1)
    bw = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(bw, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    circle_result = deepcopy(img)

    # Finding all vertical and horizontal lines
    horizontal = bw
    vertical = bw

    horizontal_scale = 10
    vertical_scale = 10

    horizontalsize = int(horizontal.shape[1] / horizontal_scale)

    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))

    horizontal = cv2.erode(horizontal, horizontal_structure, (-1, -1))
    horizontal = cv2.dilate(horizontal, horizontal_structure, (-1, -1))

    vertical_size = int(vertical.shape[0] / vertical_scale)

    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))

    vertical = cv2.erode(vertical, vertical_structure, (-1, -1))
    vertical = cv2.dilate(vertical, vertical_structure, (-1, -1))

    img_without_lines = img

    mask = horizontal + vertical

    # Using mask to remove all lines from image
    whiteImg = np.zeros(img_without_lines.shape, img_without_lines.dtype)
    whiteImg[:, :] = (255, 255, 255)
    whiteMask = cv2.bitwise_and(whiteImg, whiteImg, mask=mask)

    kernel = np.ones((5, 5), np.uint8)
    whiteMask = cv2.dilate(whiteMask, kernel, iterations=1)

    cv2.addWeighted(whiteMask, 1, img_without_lines, 1, 0, img_without_lines)

    corners = cv2.bitwise_and(horizontal, vertical)

    points = list()
    point = dict()
    lines = list()

    # Filters points in line intersections and save them as dict's using horizontal axis
    for y in range(img_height):
        for x in range(img_width):
            point['x'] = int()
            point['y'] = int()
            if corners[y][x]:
                point_control = True
                point['x'] = x
                point['y'] = y
                if points:
                    for comp_point in points:
                        if point['x'] - 25 < comp_point['x'] < point['x'] + 25 and \
                                point['y'] - 25 < comp_point['y'] < point['y'] + 25:
                            point_control = False
                    if point_control:
                        points.append(deepcopy(point))
                else:
                    points.append(deepcopy(point))

    if points:
        # Same filter as previous, but using other vertical axis
        points.sort(key=lambda x: x['y'])
        lines = list()
        current_line = dict()
        current_line['points'] = list()
        current_point = points[0]
        for point_counter in range(len(points)):
            if points[point_counter]['y'] <= current_point['y'] + 15:
                current_line['points'].append(points[point_counter])
            else:
                if current_line['points']:
                    lines.append(current_line)
                current_point = points[point_counter]
                current_line = dict()
                current_line['points'] = list()
                current_line['points'].append(points[point_counter])

        if current_line:
            lines.append(current_line)

    cropped_img_list = list()

    # Removing emply lines and calculate horizontal line width
    if lines:
        for line in lines:
            if len(line['points']) <= 1:
                lines.remove(line)
                continue
            line['points'].sort(key=lambda x: x['x'])

            line['line_length'] = 0
            start_point = line['points'][0]
            end_point = line['points'][0]
            for point_counter in range(len(line['points'])):
                if point_counter == len(line['points']) - 1:
                    end_point = line['points'][point_counter]
                    line['line_length'] = int(end_point['x'] - start_point['x'])
                cv2.circle(circle_result, (line['points'][point_counter]['x'], line['points'][point_counter]['y']), 25, (0, 255, 0), thickness=5)

        # Page segmentation using points
        img_num = 1
        if len(lines) > 1:
            row = 1
            for line_counter in range(len(lines) - 1):

                if abs(lines[line_counter]['line_length'] - lines[line_counter + 1]['line_length']) \
                        < 0.5 * lines[line_counter]['line_length']:
                    for point_counter1 in range(len(lines[line_counter]['points']) - 1):

                        point_a = lines[line_counter]['points'][point_counter1]
                        point_b = dict()
                        point_c = dict()
                        point_d = dict()
                        for point_counter2 in range(len(lines[line_counter + 1]['points']) - 1):
                            if lines[line_counter + 1]['points'][point_counter2]['x'] - 15 < point_a['x'] <  \
                                    lines[line_counter + 1]['points'][point_counter2]['x'] + 15:
                                point_d = lines[line_counter + 1]['points'][point_counter2]
                        point_b = lines[line_counter]['points'][point_counter1 + 1]
                        for point_counter2 in range(len(lines[line_counter + 1]['points'])):
                            if lines[line_counter + 1]['points'][point_counter2]['x'] - 15 < point_b['x'] <  \
                                    lines[line_counter + 1]['points'][point_counter2]['x'] + 15:
                                point_c = lines[line_counter + 1]['points'][point_counter2]

                        if point_a and point_b and point_d and not point_c:
                            for point_counter2 in range(len(lines[line_counter + 1]['points']) - 1):
                                if point_d == lines[line_counter + 1]['points'][point_counter2]:
                                    point_c = lines[line_counter + 1]['points'][point_counter2 + 1]

                            for point_counter2 in range(len(lines[line_counter]['points'])):
                                if lines[line_counter]['points'][point_counter2]['x'] - 15 < point_c['x'] < \
                                        lines[line_counter]['points'][point_counter2]['x'] + 15:
                                    point_b = lines[line_counter]['points'][point_counter2]
                        if point_a and point_b and point_c and point_d:
                            is_subline = False
                            cropped_img_params = dict()
                            crop_img = img[point_a['y']: point_d['y'],
                                       point_a['x']: point_b['x']]

                            full_path = cropped_img_dir + "img_%s.png" % (img_num)
                            cv2.imwrite(full_path, crop_img)

                            subprocess.call(
                                'convert -density 300x300 -units PixelsPerInch "%(file)s" "%(file)s"' % (
                                {"file": full_path}),
                                shell=True, executable='/bin/bash')

                            cropped_img_params['img_path'] = full_path
                            cropped_img_params['x_topleft'] = point_a['x']
                            cropped_img_params['y_topleft'] = point_a['y']
                            cropped_img_params['width'] = point_b['x'] - point_a['x']
                            cropped_img_params['height'] = point_d['y'] - point_a['y']
                            cropped_img_params['row_num'] = row

                            if lines[line_counter]['line_length'] < 0.6 * lines[line_counter + 1]['line_length']:
                                is_subline = True
                            cropped_img_params['is_subline'] = is_subline

                            cropped_img_list.append(cropped_img_params)

                            img_num += 1


                else:
                    for point_counter1 in range(len(lines[line_counter]['points']) - 1):
                        point_a = lines[line_counter]['points'][point_counter1]
                        point_b = dict()
                        point_c = dict()
                        point_d = dict()
                        for point_counter2 in range(len(lines[line_counter + 1]['points']) - 1):
                            if lines[line_counter + 1]['points'][point_counter2]['x'] - 15 < point_a['x'] <  \
                                    lines[line_counter + 1]['points'][point_counter2]['x'] + 15:
                                point_d = lines[line_counter + 1]['points'][point_counter2]

                        if not point_d:
                            for point_counter2 in range(len(lines[line_counter + 2]['points']) - 1):
                                if lines[line_counter + 2]['points'][point_counter2]['x'] - 15 < point_a['x'] < \
                                        lines[line_counter + 2]['points'][point_counter2]['x'] + 15:
                                    point_d = lines[line_counter + 2]['points'][point_counter2]

                        point_b = lines[line_counter]['points'][point_counter1 + 1]

                        for point_counter2 in range(len(lines[line_counter + 1]['points'])):
                            if lines[line_counter + 1]['points'][point_counter2]['x'] - 15 < point_b['x'] < \
                                    lines[line_counter + 1]['points'][point_counter2]['x'] + 15:
                                point_c = lines[line_counter + 1]['points'][point_counter2]

                        if not point_c:
                            for point_counter2 in range(len(lines[line_counter + 2]['points'])):
                                if lines[line_counter + 2]['points'][point_counter2]['x'] - 15 < point_b['x'] < \
                                        lines[line_counter + 2]['points'][point_counter2]['x'] + 15:
                                    point_c = lines[line_counter + 2]['points'][point_counter2]

                        if point_a and point_b and point_c and point_d:
                            cropped_img_params = dict()
                            is_subline = False
                            crop_img = img_without_lines[point_a['y']: point_d['y'],
                                       point_a['x']: point_b['x']]

                            full_path = cropped_img_dir + "img_%s.png" % (img_num)
                            cv2.imwrite(full_path, crop_img)

                            subprocess.call(
                                'convert -density 300x300 -units PixelsPerInch "%(file)s" "%(file)s"' % (
                                {"file": full_path}),
                                shell=True, executable='/bin/bash')

                            cropped_img_params['img_path'] = full_path
                            cropped_img_params['x_topleft'] = point_a['x']
                            cropped_img_params['y_topleft'] = point_a['y']
                            cropped_img_params['width'] = point_b['x'] - point_a['x']
                            cropped_img_params['height'] = point_d['y'] - point_a['y']
                            cropped_img_params['row_num'] = row


                            if lines[line_counter]['line_length'] < 0.6 * lines[line_counter + 1]['line_length']:
                                is_subline = True
                            cropped_img_params['is_subline'] = is_subline

                            cropped_img_list.append(cropped_img_params)
                            img_num += 1
                row += 1

    return cropped_img_list
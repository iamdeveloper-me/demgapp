import cv2
from scripts.general_purpose import create_dir


def intersection(a,b, threshold=0):
    """
    Gets intersection result of 2 rectangles
    :param a: rectangle type tuple
    :type a: tuple
    :param b: rectangle type tuple
    :type b: tuple
    :param threshold: intersection threshold value
    :type threshold: int
    :return:  intersection rectangle
    :rtype: tuple
    """
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<threshold or h<threshold:
        return () # or (0,0,0,0) ?rota
    return (x, y, w, h)


def crop_roi_from_page(img_path, roi_path):
    """
    Finds all table-like ROI's and crops them to roi_path


    Uses following functions:

    * :func: 'scripts.general_purpose.create_dir'

    :param img_path: path to image
    :type img_path: str
    :param roi_path: path to cropped rois
    :type roi_path: str
    :return:
    """
    create_dir(roi_path)

    # Image preparatioin
    img = cv2.imread(img_path)
    img_height = img.shape[0]
    img_width = img.shape[1]
    img_area = img_height * img_width
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw = cv2.bitwise_not(gray)

    # Find all contours and select all approximate to rectangle smaller then 96% of image to avoid including whole
    # image contour
    contours = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    rects = [cv2.boundingRect(cnt) for cnt in contours if cv2.contourArea(cnt) < 0.64 * img_area]

    # Delete intersected rectangles (table cells for example) inside bigger one (tables)
    inner_rects = list()
    if len(rects) > 2:
        for i in range(len(rects) - 1):
            for k in range(i + 1, len(rects)):
                if intersection(rects[i], rects[k]):
                    # print(i, k)
                    min_rect = rects[i]
                    if (rects[k][2] * rects[k][3]) < (min_rect[2] * min_rect[3]):
                        min_rect = rects[k]
                    # print(min_rect)
                    inner_rects.append(min_rect)

    inner_rects = list(set(inner_rects))

    temp = list()
    # Filters outer rectangles
    for rect in rects:
        if rect not in inner_rects:
            temp.append(list(rect))


    table_rects = temp

    # Crops every outer rectangle and save them to roi_path as .png
    roi_iterator = 1
    for rect in table_rects:
        x, y, w, h = rect
        crop_img = img[y - 15: y + h + 15, x - 15: x + w + 15]
        filename = img_path.split("/")[-1].split(".")[0] + "_" + str(roi_iterator) + ".png"
        cropped_roi_path = roi_path + filename
        cv2.imwrite(cropped_roi_path, crop_img)
        roi_iterator += 1
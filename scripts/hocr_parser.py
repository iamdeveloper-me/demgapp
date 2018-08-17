
import binascii
import subprocess
from copy import deepcopy
from scripts.general_purpose import get_secret


TESS_DATA_DIR = get_secret("TESS_DATA_DIR")

def get_table_name(soup):
    """
    Gets table name from Tesseract output

    Uses following functions:
    * :func: 'utils.hocr_parser.form_lines'
    * :func: 'utils.hocr_parser.parse_words'

    :param soup: tesseract output
    :type soup: bs4.BeautifulSoup
    :return: table_name
    :rtype: str
    """
    lines = soup.find_all('span', 'ocr_line')
    words_hip = list()
    for line in lines:
        words = {'words': list()}
        if "textangle" not in line['title']:
            angle = line['title'].split(';')[1].lstrip().split(' ')[1]
            words['tesser_line_id'] = line['id']
            words['angle'] = angle
            words['words'].extend(line.find_all('span', 'ocrx_word'))
            words_hip.append(words)
    lines_list = list()
    table_name = str()
    if words_hip:
        words_list = parse_words(words_hip)
        if words_list:
            words_list = sorted(words_list, key=lambda x: x['word_base_line'])
            lines_list = form_lines(words_list)
            if lines_list:
                for word in lines_list[0]:
                    table_name += word['value'].strip() + " "
    else:
        print("Failed to get table name in scripts.hocr_parser.get_table_name")

    # print("--------------------------        ", table_name, '            --------------------------')
    # print(words_list, "\n -----------------------------------------------------------------------------------------------")


    return table_name


def form_lines(words_list):
    """
    Form lines based on "base_line" param of words

    :param words_list: list of words
    :type words_list: list
    :return: lines_list - list of words groupped by line
    :rtype: list
    """
    current_word = words_list[0]
    lines_list = list()
    line = list()
    for word in words_list:
        if word['base_line'] - 15 < current_word['base_line'] < word['base_line'] + 15:
            line.append(word)
        else:
            if line:
                line = sorted(line, key=lambda x: x['base_col'])
                lines_list.append(line)
            current_word = word
            line = list()
            line.append(word)
    if line:
        line = sorted(line, key=lambda x: x['base_col'])
        lines_list.append(line)

    return lines_list


def get_text_angle(soup):
    """
    Gets text angle from Tesseract output

    :param soup: tesseract output
    :type soup: bs4.BeautifulSoup
    :return: most_common_angle - angle
    :rtype: float
    """
    lines = soup.find_all('span', 'ocr_line')
    text_angles = list()
    number_without_angle = 0
    most_common_angle = 0
    for line in lines:
        if "textangle" in line['title']:
            text_angle = int(line['title'].split(";")[1].strip().split(" ")[1])
            text_angles.append(text_angle)
        else:
            number_without_angle += 1

    if len(text_angles) >  0.5 * len(lines):
        most_common_angle = max(set(text_angles), key=text_angles.count)
    return most_common_angle


def get_average_accuracy(soup):
    """
    Gets average of all words from tesseract output

    Uses following functions:

    * :func: 'utils.hocr_parser.parse_words'

    :param soup: tesseract output
    :type soup: bs4.BeautifulSoup
    :return: avg_accuracy - average accuracy
    :rtype: int
    """
    lines = soup.find_all('span', 'ocr_line')
    words_hip = list()
    for line in lines:
        words = {'words': list()}
        words['tesser_line_id'] = line['id']
        words['words'].extend(line.find_all('span', 'ocrx_word'))
        words_hip.append(words)


    words_list = parse_words(words_hip)
    words_list = sorted(words_list, key=lambda x: x['word_base_line'])
    print(words_list)
    sum_accuracy = 0
    for word in words_list:
        sum_accuracy += int(word['accuracy'])

    if len(words_list) > 0:
        avg_accuracy = sum_accuracy / len(words_list)
    else:
        avg_accuracy = 0
    return avg_accuracy



def parse_words(words_hip):
    """
    Gets words values and adding the following parameters to words:

    * ``accuracy``
    * ``angle``
    * ``tesser_line_id``
    * ``x_left``
    * ``x_right``
    * ``y_top``
    * ``y_bottom``
    * ``word_length``
    * ``word_height``
    * ``word_base_line``
    * ``base_line``
    * ``base_col``
    * ``y_top_low``
    * ``y_bottom_high``
    * ``value``

    :param words_hip: ``ocrx_word`` blocks from `hocr-file`
    :type words_hip: list
    :return: words_list - list of dicts with words values and their attributes
    :rtype: list
    """
    words_list = list()
    for words in words_hip:
        for word in words['words']:
            if word.text not in [" ", "", "'", ".", ",", "!", ";", "|",
                                 ">", "<", "&gt;", "&lt;", 'ËË"', '/',
                                 '\\', '{', '}', '__', 'i', 'Î4Ê', '__|']:
                word_title = word["title"].split(';')
                word_coordinates = word_title[0]
                word_coordinates = word_coordinates.split(' ')
                word_params = dict()
                word_params['x_left'] = int(word_coordinates[1])
                word_params['y_top'] = int(word_coordinates[2])
                if not word_params['y_top'] and not word_params['x_left']:
                    continue
                word_params['tesser_line_id'] = words['tesser_line_id']
                word_params['x_right'] = int(word_coordinates[3])
                word_params['y_bottom'] = int(word_coordinates[4])
                word_params['word_base_line'] = (word_params['y_top'] +
                                                 word_params['y_bottom']) / 2
                word_params['base_line'] = (word_params['y_top'] + word_params[
                    'y_bottom']) / 2
                word_params['base_col'] = (word_params['x_left'] + word_params[
                    'x_right']) / 2
                word_params['word_height'] = word_params['y_bottom'] - word_params['y_top']
                word_params['value'] = word.text
                word_params['accuracy'] = int(word_title[1].split(' ')[2])
                words_list.append(word_params)
    return words_list

def shingle_word_compare(phrase, correct_phrase):
    """ Finding % of similarity between 2 texts (or overlapping for 2 texts)

    For each parameter divide string by shingles (per symbol),
    convert to crc32 hash and then return % of similar hashes.

    | If operation_type == 'comparing' - compares 2 words/phrases
    | If operation_type == 'overlapping' - check 2 words/phrases on overlapping


    Uses the following functions:

    * :func:`utils.parsers_utils.canonize`
    * :func:`utils.parsers_utils.genshingle`
    * :func:`utils.parsers_utils.compare`

    :param phrase: phrase to check
    :param correct_phrase: phrase to compare with
    :param operation_type: operation type for using this function
    :type phrase: basestring
    :type correct_phrase: basestring
    :return: result - % of similarity between phrase and correct_phrase
    :rtype: float
    """
    result = ''
    if len(phrase) == 1 or len(correct_phrase) == 1:
        result = compare(phrase, correct_phrase)
    else:
        cmp1 = genshingle(canonize(phrase))
        cmp2 = genshingle(canonize(correct_phrase))
        result = compare(cmp1, cmp2)

    return result


def genshingle(word):
    """ Splitting text into shingles

    Returns list CRC32 hashes for current word

    :param word: word
    :type word: str
    :return: list of checksums of current word
    :rtype: list
    """
    shingle_len = 2
    out = []
    for i in range(len(word) - (shingle_len - 1)):
        out.append(binascii.crc32(''.join([x for x in word[i:i + shingle_len]]).encode('utf-8')))
    return out


def compare(source1, source2):
    """ Compare 2 sets of checksums of 2 texts

    | Finds percentage of their similarity.
    | Returns percentage of similarity of two texts.

    :param source1: checksums set 1
    :param source2: checksums set 2
    :type source1: list or str
    :type source2: list or str
    :return: percentage of similarity of two texts
    :rtype: float
    """
    same = 0
    if len(source1) <= len(source2):
        for i in range(len(source1)):
            if source1[i] in source2:
                same = same + 1
    else:
        for i in range(len(source2)):
            if source2[i] in source1:
                same = same + 1
    return same * 2 / float(len(source1) + len(source2)) * 100


def canonize(word):
    """ Text canonization

    Clears the text of the stop-symbols,
    brings all the characters of the string to the lower case and
    returns a word in lower case without stop-symbols and spaces.

    :param word: word
    :type word: str
    :return: word after clearing
    :rtype: str
    """
    stop_symbols = '.,!?;:()/'
    for symbol in stop_symbols:
        word = ''.join(word.split(symbol))
    return word.lower().rstrip().lstrip()


def cropped_img_processor(cropped_img_list):
    """
    Process segmented table cells and form new lists/dirs structure with recognized text and some params

    :param cropped_img_list:
    :type cropped_img_list: list
    :return: new_tb_rows - list with cropped cells params and text from OCR
    :rtype: list
    """
    new_tb_rows = list()
    new_tb_row = list()
    i = 0
    for cropped_img in cropped_img_list:
        tess_call_1 = "tesseract %(path)s %(path)s --tessdata-dir %(tessdata_dir)s -l %(lang)s tsv" % {
            "path": cropped_img['img_path'], "lang": "eng",
            "tessdata_dir": TESS_DATA_DIR}

        tess_call_2 = "tesseract %(path)s %(path)s --tessdata-dir %(tessdata_dir)s -l %(lang)s --psm 6" % {
            "path": cropped_img['img_path'], "lang": "eng",
            "tessdata_dir": TESS_DATA_DIR}

        subprocess.call("%s" % tess_call_1, shell=True)

        with open(cropped_img["img_path"] + ".tsv") as f:
            rows = f.readlines()  # [line.split('\t') for line in f]
            rows = [line.split('\t') for line in rows]

        f.close()
        csv_headers = rows[0]
        tmp_list = list()
        for row in rows[1:]:
            tmp_dict = dict()
            k = 0  # i --> k
            for c in row:
                # print('eeeee', c)
                if csv_headers[k].strip() == 'text' and len(rows) == 2 and not len(c.strip()):
                    subprocess.call("%s " % tess_call_2, shell=True)
                    # print('PEW_PEW_PEW', c, len(c.strip()))
                    with open(cropped_img["img_path"] + ".txt") as txt:
                        c = txt.readline().strip()
                        # print('CCCCC', c)
                    txt.close()
                tmp_dict[csv_headers[k].strip()] = c.strip() if c else ''  # i --> k
                k += 1  # i --> k
            # if 'text' in tmp_dict.keys() and tmp_dict['text'] and\
            #         50 <= int(tmp_dict['top']) <= 50 + chunk['height'] and\
            #         30 <= int(tmp_dict['left']) <= 30 + chunk['width']:
            if 'text' in tmp_dict.keys() and tmp_dict['text']:  # and tmp_dict['text'].lower() != "куки":
                tmp_list.append(deepcopy(tmp_dict))
        text_var = str()
        avg_accuracy = 0
        for text in tmp_list:
            text_var += text['text'] + " "
            avg_accuracy += int(text['conf'])
        text_var = text_var[:-1]
        # print(text_var)
        cropped_img["text"] = text_var if text_var else ""
        if tmp_list:
            cropped_img["accuracy"] = avg_accuracy / len(tmp_list)
            # ---------------------------------------------- if recognized word has low accuracy ---------------------------------------------
            if 0 < cropped_img["accuracy"] <= 50:
                subprocess.call("%s" % tess_call_2, shell=True)
                with open(cropped_img["img_path"] + ".txt") as t:
                    c = ''
                    for l in t.readlines():
                        if l:
                            c += l.strip() + ' '
                t.close()
                cropped_img["accuracy"] = -5
                cropped_img["text"] = c.strip()
            # --------------------------------------------------------------------------------------------------------------------------------
        else:
            cropped_img["accuracy"] = 0

        if new_tb_row:
            # print(new_tb_row)
            if new_tb_row[-1]['row_num'] == cropped_img['row_num']:
                new_tb_row.append(cropped_img)
            else:
                new_tb_rows.append(deepcopy(new_tb_row))
                new_tb_row = list()
                new_tb_row.append(cropped_img)
        else:
            new_tb_row.append(cropped_img)
        if i == len(cropped_img_list) - 1:
            # print('111')
            # print(new_tb_row)
            new_tb_rows.append(deepcopy(new_tb_row))
        # print('i:', i)
        i += 1
    return new_tb_rows


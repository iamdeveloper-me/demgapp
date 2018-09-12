# from django.views.decorators.csrf import csrf_exempt
# from werkzeug.utils import secure_filename
# from config.settings import UPLOAD_FOLDER
# from django.http import HttpResponse
# import os
# import subprocess
# from bs4 import BeautifulSoup
# from scripts import file_processing, roi_finder, hocr_parser, json_builder
# from scripts.table_cells_cropper import table_cells_cropper, remove_lines, form_lines, prepare_img_to_roi_search, remove_unwanted_objects
# from scripts.general_purpose import file_name_extension_splitter, create_dir, get_secret
# import time
# import json


# '''
# List of current problems:
# 1. High CPU load due to lots of subprocess calls
# 2. Queue issue. There is not queue
# 3. Very simplistic api. Client sent POST and wait for response. Will require script on client side
# 4. Multi sublines fails to split headers.
# 5. Extremely long time extracting big PDFs
# 6. No rotation
# 7. .xml remove might fix
# 8. Triangles on some images

# '''


# TESS_DATA_DIR = get_secret("TESS_DATA_DIR")

# ALLOWED_EXTENSIONS = set(['pdf'])
# ALLOWED_TABLE_NAMES = ["LUMINAIRE SCHEDULE", "LIGHT FIXTURE SCHEDULE", "LIGHTING FIXTURE SCHEDULE",
#                        "UNITS LIGHTING FUXTURE SCHEDULE", "COMMON SPACES LIGHTING FIXTURE SCHEDULE",
#                        "EXTERIOR LIGHT FIXTURE SCHEDULE", "LUMINAIRE SCHEDULE"]
# FORBIDDEN_TABLE_NAMES = ["PLUMBING FIXTURE SCHEDULE"]

# def allowed_file(filename) -> bool:
#     """
#     Checks if file meets requirements.
#     :param filename: path to file
#     :type filename: str
#     :return: control - boolean value if file is allowed
#     :rtype: bool
#     """
#     control = False
#     if str(filename).rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
#         control = True
#     return control


# @csrf_exempt
# def upload(request):
#     """
#     Main function that execute chain

#     :param request: http request object
#     :type request: request_object
#     :return: httpresponse - html page with string
#     :rtype: httpresponseobject
#     """
#     start_time = time.time()
#     json_results = list()
#     if request.method == 'POST':
#         # print("--------------------POST---------------")
#         file = request.FILES['file']
#         if file == '':
#             print("No file")
#             return "No file"
#         if file and allowed_file(file):
#             file_params = file_name_extension_splitter(file)
#             new_name_header = str(int(time.time())) + "_tt_"
#             file_params['new_name'] = new_name_header + secure_filename(file_params['name_without_extension']).replace(
#                 ".", "") + "." + file_params["extension"]
#             upload_path = UPLOAD_FOLDER + new_name_header + file_params['name_without_extension'] + "/"
#             upload_path = upload_path.replace(" ", "_").replace(".", "").replace("(", "").replace(")", "")
#             file_params["upload_path"] = upload_path
#             print("-------FILE PARAMS--------", file_params)
#             try:
#                 create_dir(upload_path)
#             except Exception as e:
#                 print("Can't create upload directory")
#                 return "Can`t create upload directory"
#             try:
#                 with open(upload_path + file_params['new_name'], 'wb+') as destination:
#                     for chunk in file.chunks():
#                         destination.write(chunk)
#                 destination.close()
#             except Exception as e:
#                 print("Can`t save uploaded file")
#                 return "Can`t save uploaded file"
#             try:
#                 file_params = file_processing.pre_process(file_params)
#             except Exception as e:
#                 print("Cant preprocess file")
#                 return "Cant preprocess file"

#             pdf_path = file_params["upload_path"] + file_params["new_name"]
#             output_path = pdf_path.split(".")[0] + ".xml"
#             page_amount = file_processing.get_pdf_page_amount(pdf_path)

#             files = list()
#             page_number_order_of_magnitude = len(str(page_amount))
#             page_counter = 1
#             if page_amount <= 5:
#                 files = sorted(os.listdir(file_params["dispatch_path"]))
#             elif 5 < page_amount < 50:
#                 # if pdf is empty check all files aka files = sorted(os.listdir(file_params["dispatch_path"]))
#                 subprocess.call("pdftohtml '%s' -xml -q -i '%s'" % (pdf_path, output_path),
#                                 shell=True)  # , executable='/bin/bash')

#                 with open(output_path, "r") as f:
#                     data = f.read()
#                 xml_data = BeautifulSoup(data, 'lxml-xml')
#                 pages = xml_data.find_all("page")
#                 have_xml_data = True
#                 for page in pages:
#                     texts = page.find_all("text")
#                     if not texts:
#                         have_xml_data = False
#                         break
#                     for text in texts:
#                         applicant = text.text
#                         for allowed_name in ALLOWED_TABLE_NAMES:
#                             if allowed_name.lower() in applicant.lower():
#                                 print("Lighting table might be on page ", page_counter)
#                                 file_ending_number = str(page_counter)
#                                 while len(file_ending_number) < page_number_order_of_magnitude:
#                                     file_ending_number = "0" + file_ending_number
#                                 file_ending = "-" + file_ending_number + ".png"
#                                 files.append(file_params['name_without_extension'] + file_ending)
#                     page_counter += 1
#                 if not have_xml_data:
#                     files = sorted(os.listdir(file_params["dispatch_path"]))
#             else:
#                 # if xml is empty pass this kind of documents files = list()
#                 subprocess.call("pdftohtml '%s' -xml -q -i '%s'" % (pdf_path, output_path),
#                                 shell=True)  # , executable='/bin/bash')
#                 with open(output_path, "r") as f:
#                     data = f.read()
#                 xml_data = BeautifulSoup(data, 'lxml-xml')
#                 pages = xml_data.find_all("page")
#                 have_xml_data = True
#                 for page in pages:
#                     texts = page.find_all("text")
#                     for text in texts:
#                         applicant = text.text
#                         if not texts:
#                             have_xml_data = False
#                             break
#                         for allowed_name in ALLOWED_TABLE_NAMES:
#                             if allowed_name.lower() in applicant.lower():
#                                 print("Lighting table might be on page ", page_counter)
#                                 file_ending_number = str(page_counter)
#                                 while len(file_ending_number) < page_number_order_of_magnitude:
#                                     file_ending_number = "0" + file_ending_number
#                                 file_ending = "-" + file_ending_number + ".png"
#                                 files.append(file_params['name_without_extension'] + file_ending)
#                     page_counter += 1
#                 if not have_xml_data:
#                     files = sorted(os.listdir(file_params["dispatch_path"]))

#             if not files:
#                 files = sorted(os.listdir(file_params["dispatch_path"]))
#             files = sorted(list(set(files)))
#             print("-------CHAIN PARAMS--------\nFile params: ", file_params, "\nFiles: ", files, "\n -------------------------")

#             last_page = False
#             for file in files:
#                 if file.endswith(".png"):
#                     have_lighting_table = False
#                     file_path = file_params["dispatch_path"] + file
#                     print("\n--------------- Processing IMAGE ", file_path)
#                     rois_path = file_params["dispatch_path"] + 'roi_' + file.split(".")[0] + "/"
#                     create_dir(rois_path)
#                     img_area = roi_finder.crop_roi_from_page(file_path, rois_path)
#                     print("@ROI cropping executed")
#                     rois = sorted(os.listdir(rois_path))
#                     for roi in rois:
#                         stop_trigger = False
#                         is_light_table = False
#                         roi_path = rois_path + roi
#                         if os.stat(roi_path).st_size > 0:
#                             print("Processing ROI: ", roi_path)
#                             img_without_lines, corners = remove_lines(roi_path, roi_process=True, return_corners=True)
#                             print("@Line removal executed")
#                             lines = form_lines(corners, img_without_lines.shape[0], img_without_lines.shape[1])
#                             print("@Forming lines executed")
#                             point_counter = 0
#                             for line in lines:
#                                 if len(line['points']) > 25:
#                                     stop_trigger = True
#                                 point_counter += len(line['points'])
#                             if stop_trigger:
#                                 print("!!!Stop trigger worked")
#                                 continue
#                             if point_counter < 22 or img_without_lines.shape[0] * img_without_lines.shape[
#                                 1] > 0.75 * img_area:
#                                 print("     @@@@@@@@@    FILTER WORKED")
#                                 continue
#                             roi_nolines_path = roi_path.split(".")[0] + "_no_lines.png"
#                             prepare_img_to_roi_search(img_without_lines, lines, roi_nolines_path)
#                             print("@Image preparation for roi search executed")
#                             roi_without_extension = roi_path.split(".")[0]

#                             # dpi_convert_call = 'convert -density 300x300 -units PixelsPerInch "%(file)s" "%(file)s"' % (
#                             # {"file": roi_nolines_path})
#                             tess_call_1 = "tesseract %(input)s %(output)s --tessdata-dir %(tessdata_dir)s -l %(lang)s hocr" % {
#                                 "input": roi_nolines_path, "output": roi_without_extension, "lang": "eng",
#                                 "tessdata_dir": get_secret("TESS_DATA_DIR")}
#                             tess_call_2 = "tesseract %(input)s %(output)s --tessdata-dir %(tessdata_dir)s -l %(lang)s --psm 6" % {
#                                 "input": roi_nolines_path, "output": roi_without_extension, "lang": "eng",
#                                 "tessdata_dir": get_secret("TESS_DATA_DIR")}

#                             # subprocess.call(dpi_convert_call, shell=True, executable='/bin/bash')
#                             subprocess.call("%s" % tess_call_1, shell=True)
#                             subprocess.call("%s" % tess_call_2, shell=True)
#                             print("@Tesseract calls executed")
#                             hocr_path = roi_without_extension + ".hocr"
#                             hocr_file = open(hocr_path)
#                             soup = BeautifulSoup(hocr_file, "lxml")
#                             hocr_file.close()

#                             table_name = hocr_parser.get_table_name(soup)
#                             print("@Table name finder executed")
#                             if not table_name:
#                                 with open(roi_without_extension + ".txt", "r") as f:
#                                     lines = f.readlines()
#                                     for line in lines:
#                                         # print(line)
#                                         if len(line) > 5:
#                                             allowed_name = "LIGHTING FIXTURE SCHEDULE".strip().lower()
#                                             line = line.strip().lower()
#                                             if hocr_parser.shingle_word_compare(allowed_name, line) > 75:
#                                                 is_light_table = True
#                                             break
#                             print("@Table name shingles executed")
#                             for forbidden_name in FORBIDDEN_TABLE_NAMES:
#                                 forbidden_name = forbidden_name.strip().lower()
#                                 table_name = table_name.strip().lower()
#                                 if hocr_parser.shingle_word_compare(forbidden_name, table_name) < 95:
#                                     for allowed_name in ALLOWED_TABLE_NAMES:
#                                         allowed_name = allowed_name.strip().lower()
#                                         table_name = table_name.strip().lower()
#                                         if hocr_parser.shingle_word_compare(allowed_name, table_name) > 75:
#                                             is_light_table = True
#                             print("@Forbiden name check executed")
#                             if is_light_table:
#                                 have_lighting_table = True
#                                 print("PROCESSING LIGHT TABLE")
#                                 cropped_img_location = roi_without_extension + "/"
#                                 create_dir(cropped_img_location)
#                                 print("TABLE SEGMENTATION")
#                                 cropped_img_list = table_cells_cropper(roi_path, cropped_img_location)
#                                 print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", cropped_img_list)
#                                 print("PROCESSING SEGMENTATED IMAGES")
#                                 table = hocr_parser.cropped_img_processor(cropped_img_list)
#                                 print("!!!!!!", table)
#                                 print("REMOVING UNWANTED OBJECTS (TRIANGLES)")
#                                 table = remove_unwanted_objects(table)
#                                 print("SUBLINE PROCESSING")
#                                 table = json_builder.subline_processor(table)
#                                 print("BUILDING JSON")
#                                 json_result = json_builder.json_builder(table)
#                                 json_results.append(json_result)
#                         else:
#                             continue

#                     if last_page:
#                         break

#                     if have_lighting_table:
#                         last_page = True
#                         have_lighting_table = False



#             with open(upload_path + 'data.json', 'w') as outfile:
#                 json.dump(json_results, outfile)
#             outfile.close()
#             # json_results = json.dumps(json_results)
#             print("\n\n----------------- CHAIN PROCESS TIME ", time.time() - start_time,
#                   " seconds ------------------------\n")
#     return HttpResponse(json_results)

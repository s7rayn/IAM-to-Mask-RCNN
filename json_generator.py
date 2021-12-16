import json

import matplotlib.pyplot as plotly
from bs4 import BeautifulSoup as bs

DATASET = 'train'

# Load xml
with open(DATASET + ".xml", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")

image_description = {}
### load word jednotlive slova v txt
with open(DATASET + '_words.txt', "r") as description:
    for line in description:
        if (line != "\n"):
            array = line.split(" ")

            print(line)
            description_name = array[0]
            description_x = int(array[3])/6.90529248
            description_y = int(array[4])/6.91796875
            description_width = int(array[5])/6.90529248
            description_height = int(array[6])/6.91796875
            description_dict = {description_name: {"x": description_x, "y": description_y, "width": description_width,
                                                   "height": description_height}}
            image_description.update(description_dict)

resultForm = bs_content.find_all("form")
result = bs_content.find_all("word")
# result = list(result[1].children)

dataFinal = {}
images = []
categories = []
annotations = []
category_id = 1
img_id = 0
unique_id = 0
unique_id_ann = 0
for i in result:
    id_image = i["id"]
    for j in resultForm:
        if i["id"].__contains__(j["id"]):
            id_imageForm = j["id"]
            name = j["id"]
            heightForm = j["height"]
            widthForm = j["width"]

    children = list(i.children)
    xList = []
    yList = []
    if not any(d['name'] == "word" for d in categories):
        categories.append({"id": category_id, "name": "word", "supercategory": "words"})
        category_id += 1
    actual_category_id = 0
    for d in categories:
        if (d["name"] == "word"):
            actual_category_id = d["id"]

    if not any(img["file_name"] == id_imageForm + ".png" for img in images):
        images.append({"id": img_id, "license": 1, "file_name": id_imageForm + ".png", "height": 359,
                       "width": 512, "date_captured": "2021-11-22T16:00:30+00:00"})
        img_id += 1
    area = int(image_description[id_image]["height"]) * int(image_description[id_image]["width"])
    seg = []
    # LH
    seg.append(int(image_description[id_image]["x"]))
    seg.append(int(image_description[id_image]["y"]))
    # PH
    seg.append(int(image_description[id_image]["x"]) + int(image_description[id_image]["width"]))
    seg.append(int(image_description[id_image]["y"]))
    # PD
    seg.append(int(image_description[id_image]["x"]) + int(image_description[id_image]["width"]))
    seg.append(int(image_description[id_image]["y"]) + int(image_description[id_image]["height"]))
    # LD
    seg.append(int(image_description[id_image]["x"]))
    seg.append(int(image_description[id_image]["y"]) + int(image_description[id_image]["height"]))
    annotation = {"id": unique_id, "image_id": img_id - 1, "category_id": actual_category_id,
                  "bbox": [int(image_description[id_image]["x"]), int(image_description[id_image]["y"]),
                           int(image_description[id_image]["width"]), int(image_description[id_image]["height"])],
                  "area": area, "segmentation": [seg],
                  "iscrowd": 0}
    annotations.append(annotation)
    for j in children:
        if (j != "\n"):
            xList.append(int(j["x"]))
            yList.append(int(j["y"]))

            data = {"info":
                {
                    "description": "COCO 2021 Dataset",
                    "url": "https://kalendar-kril.herokuapp.com/school",
                    "version": "1.0",
                    "year": 2021,
                    "contributor": "FEI STU Team Project",
                    "date_created": "2021/11/22"
                },
                "licenses": [{
                    "id": 1,
                    "url": "https://kalendar-kril.herokuapp.com/school",
                    "name": "Team project"
                }],
                "categories": [],
                "images": [],
                "annotations": [],
            }

    dataFinal.update(data)
    unique_id += 1
dataFinal["categories"] = categories
dataFinal["images"] = images
dataFinal["annotations"] = annotations

with open(DATASET + '.json', 'w') as fp:
    json.dump(dataFinal, fp)








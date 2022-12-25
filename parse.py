# importing the libraries
from bs4 import BeautifulSoup
import requests
import unidecode
import json

#   ___ _        _   _
#  | __| |___ __| |_(_)_ _____ ___
#  | _|| / -_) _|  _| \ V / -_|_-<
#  |___|_\___\__|\__|_|\_/\___/__/

cs_courses = {}
cs_elective_courses = {}
cs_electives_raw = {
    "team_project_requirement": "417, 427, 428, 429, 437, 465, 467, 493, 494, 497",
    "software_foundations": "407, 409, 422, 426, 427, 428, 429, 474, 476, 477, 492, 493, 494, 521, 522, 524, 526, 527, 528, 576",
    "algorithms": "407, 413, 473, 475, 476, 477, 481, 482, 571, 572, 573, 574, 575, 576, 579, 580, 581, 583, 584, 586",
    "intelligence_big_data": "410, 411, 412, 414, 416, 440, 441, 442, 444, 445, 446, 447, 448, 464, 466, 467, 469, 470, 510, 511, 512, 514, 540, 542, 544, 545, 546, 548, 562, 567, 576, 582",
    "human_social_impact": "409, 416, 417, 441, 442, 460, 461, 463, 464, 465, 467, 468, 469, 470, 500, 514, 562, 563, 565, 566, 567",
    "media": "409, 414, 416, 417, 418, 419, 445, 448, 465, 467, 468, 469, 519, 545, 565, 567",
    "scientific_parallel": "419, 435, 450, 457, 466, 482, 483, 484, 519, 554, 555, 556, 558",
    "distributed_system": "407, 423, 424, 425, 431, 435, 436, 437, 438, 439, 460, 461, 463, 483, 484, 523, 524, 525, 537, 538, 562, 563",
    "machines": "423, 424, 426, 431, 433, 437, 484, 523, 526, 533, 534, 536, 541, 584, 588"
}

for c in cs_electives_raw.keys():
    prev = cs_electives_raw[c].replace(" ", "").split(",")
    cs_electives_raw[c] = prev

#   ___    _      _    _            __      __   _       _ _
#  | __|__| |_ __| |_ (_)_ _  __ _  \ \    / /__| |__ __(_) |_ ___
#  | _/ -_)  _/ _| ' \| | ' \/ _` |  \ \/\/ / -_) '_ (_-< |  _/ -_)
#  |_|\___|\__\__|_||_|_|_||_\__, |   \_/\_/\___|_.__/__/_|\__\___|
#                            |___/

url = "http://catalog.illinois.edu/courses-of-instruction/cs/"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")

courseblocks = soup.find_all("div", attrs={"class": "courseblock"})

for c in courseblocks:
    extracted_course_title = unidecode.unidecode(c.find(
        "a", attrs={"class": "schedlink"}).text)
    extracted_course_title_list = extracted_course_title.split("   ")
    extracted_descrption = unidecode.unidecode(c.find(
        "p", attrs={"class": "courseblockdesc"}).text.strip("\n"))

    course_code = extracted_course_title_list[0].replace("CS ", "")
    course_name = extracted_course_title_list[1]
    course_hour = extracted_course_title_list[2].strip("credit: ").strip(".")
    course_description = ""
    course_prerequisites = ""
    prerequisites = []

    if "Prerequisite:" in extracted_descrption:
        course_description = extracted_descrption.split("Prerequisite:")[0]
        course_prerequisites = extracted_descrption.split("Prerequisite:")[1]

        if ";" in course_prerequisites.strip():
            p = course_prerequisites.split(";")
            # print("multiple courses required.", course_prerequisites.strip())
            for _ in p:
                _ = _.strip()
                # if "ONE OF " in _.upper():
                #     print(_)
                prerequisites.append(_)
    else:
        course_description = extracted_descrption.split("Prerequisite:")[0]

    cs_courses[course_code] = {
        "course_code": course_code, "course_name": course_name,
        "course_hour": course_hour,
        "course_description": course_description,
        "course_prerequisites": {
            "raw_text": course_prerequisites.strip(),
            "prerequisites": prerequisites
        }
    }

parsed = json.dumps(cs_courses, indent=4)
# print(parsed)

for c in cs_electives_raw.keys():
    cs_elective_courses[c] = []
    for course in cs_electives_raw[c]:
        try:
            # print(course)
            cs_elective_courses[c].append(cs_courses[course])
        except BaseException as e:
            print(e)

# print(cs_elective_courses)
parsed_electives = json.dumps(cs_elective_courses, indent=4)

with open("cs_courses.json", "w") as outfile:
    outfile.write(parsed)

with open("cs_electives.json", "w") as outfile:
    outfile.write(parsed_electives)

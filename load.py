import json

electives_dict = {}
electives = {}
csv = ["course_code,course_name,course_hour,team_project_requirement,software_foundations,algorithms,intelligence_big_data,human_social_impact,media,scientific_parallel,distributed_system,machines\n"]

with open('cs_electives.json') as json_file:
    electives_dict = json.load(json_file)

for key in electives_dict.keys():
    for course in electives_dict[key]:
        if electives.get(course["course_code"]) == None:
            electives[course["course_code"]] = {
                "team_project_requirement": False,
                "software_foundations": False,
                "algorithms": False,
                "intelligence_big_data": False,
                "human_social_impact": False,
                "media": False,
                "scientific_parallel": False,
                "distributed_system": False,
                "machines": False,
                "course_name": course["course_name"].replace(",", " "),
                "course_hour": course["course_hour"]
            }
        electives[course["course_code"]][key] = True

# print(json.dumps(electives, indent=4))
for key in sorted(electives):
    # print(key)
    csv.append(key + "," + electives[key]["course_name"] +
               "," + electives[key]["course_hour"] + "," +
               ("" if (electives[key]["team_project_requirement"] == False) else "Y") + "," +
               ("" if (electives[key]["software_foundations"] == False) else "Y") + "," +
               ("" if (electives[key]["algorithms"] == False) else "Y") + "," +
               ("" if (electives[key]["intelligence_big_data"] == False) else "Y") + "," +
               ("" if (electives[key]["human_social_impact"] == False) else "Y") + "," +
               ("" if (electives[key]["media"] == False) else "Y") + "," +
               ("" if (electives[key]["scientific_parallel"] == False) else "Y") + "," +
               ("" if (electives[key]["distributed_system"] == False) else "Y") + "," +
               ("" if (electives[key]["machines"] == False) else "Y") + "\n")

for c in csv:
    print(c)

f = open("electives.csv", "w")
f.writelines(csv)
f.close()

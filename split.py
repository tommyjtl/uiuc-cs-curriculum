import json

def split_json_into_tiers(json_data):
    # Create dictionaries for each tier
    tier_100 = {}
    tier_200 = {}
    tier_300 = {}
    tier_400 = {}
    tier_500 = {}

    # Iterate through the courses and add them to the appropriate tier dictionary
    for course_code, course_info in json_data.items():
        first_digit = course_code[3]  # Get the first digit of the course code
        if first_digit == '1':
            tier_100[course_code] = course_info
        elif first_digit == '2':
            tier_200[course_code] = course_info
        elif first_digit == '3':
            tier_300[course_code] = course_info
        elif first_digit == '4':
            tier_400[course_code] = course_info
        elif first_digit == '5':
            tier_500[course_code] = course_info

    # Save each tier dictionary as a separate JSON file
    with open('tier_100.json', 'w') as file:
        json.dump(tier_100, file, indent=4)
    with open('tier_200.json', 'w') as file:
        json.dump(tier_200, file, indent=4)
    with open('tier_300.json', 'w') as file:
        json.dump(tier_300, file, indent=4)
    with open('tier_400.json', 'w') as file:
        json.dump(tier_400, file, indent=4)
    with open('tier_500.json', 'w') as file:
        json.dump(tier_500, file, indent=4)

# Load JSON data from a file
def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# Load the JSON data from the file
json_data = load_json_file('cs_courses.json')

# Split the JSON data into five different JSON files for each tier
split_json_into_tiers(json_data)

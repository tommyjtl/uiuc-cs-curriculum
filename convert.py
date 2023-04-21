import json

def convert_to_graph_format(course_json):
    nodes = []
    links = []
    node_ids = set()

    for course_code, course_info in course_json.items():
        # Add the course as a node
        nodes.append({'id': course_code, 'name': course_info['course_name']})
        node_ids.add(course_code)

        # Add the prerequisites as links (edges)
        prerequisites = course_info['course_prerequisites']['prerequisites']
        for group in prerequisites:
            for prereq in group:
                links.append({'source': prereq, 'target': course_code})
                if prereq not in node_ids:
                    # Add prerequisite course as a node if not already present
                    nodes.append({'id': prereq, 'name': prereq})
                    node_ids.add(prereq)

    return {'nodes': nodes, 'links': links}

# Load JSON data from a file
def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# Load the course JSON data from the file
course_json = load_json_file('cs_courses.json')

# Convert the course JSON data into the graph format
graph_data = convert_to_graph_format(course_json)

# Save the graph data as a JSON file
with open('graph_data.json', 'w') as outfile:
    json.dump(graph_data, outfile, indent=4)

print('Graph data has been successfully generated and saved as graph_data.json')

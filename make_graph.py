import graphviz
import json

def create_graphviz(json_data):
    # Create a directed graph using the Graphviz library
    dot = graphviz.Digraph('Courses', format='png')
    
    # Create subgraphs for each tier with rank=same
    tiers = {'1': [], '2': [], '3': [], '4': [], '5': []}
    for course_code, course_info in json_data.items():
        first_digit = course_code[3]  # Get the first digit of the course code
        tiers[first_digit].append(course_code)

    for tier, courses in tiers.items():
        with dot.subgraph(name=f'cluster_{tier}00') as subgraph:
            subgraph.attr(rank='same')
            for course_code in courses:
                course_info = json_data[course_code]
                subgraph.node(course_code, "CS " + course_info['course_code'])
    
    # Create edges based on the prerequisites
    for course_code, course_info in json_data.items():
        prerequisites = course_info['course_prerequisites']['prerequisites']
        for group in prerequisites:
            for prereq in group:
                # Create an edge from each prerequisite to the course
                dot.edge(prereq, course_code)
    
    # Save the graph as a PNG file
    dot.render('courses_graph', view=True)
    
def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

json_data = load_json_file('cs_courses.json')

# Create the Graphviz file based on the JSON data
create_graphviz(json_data)
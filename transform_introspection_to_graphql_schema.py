import json
import argparse

# Load the introspection JSON file
def load_introspection_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to print a GraphQL type from introspection
def print_graphql_type(type_info):
    kind = type_info['kind']
    name = type_info['name']
    
    if kind == "OBJECT":
        print(f"type {name} {{")
        for field in type_info['fields']:
            field_type = get_type_name(field['type'])
            print(f"  {field['name']}: {field_type}")
        print("}")
    
    elif kind == "SCALAR":
        print(f"scalar {name}")
    
    elif kind == "ENUM":
        print(f"enum {name} {{")
        for enum_value in type_info['enumValues']:
            print(f"  {enum_value['name']}")
        print("}")
    
    elif kind == "INTERFACE":
        print(f"interface {name} {{")
        for field in type_info['fields']:
            field_type = get_type_name(field['type'])
            print(f"  {field['name']}: {field_type}")
        print("}")
    
    elif kind == "UNION":
        possible_types = " | ".join([pt['name'] for pt in type_info['possibleTypes']])
        print(f"union {name} = {possible_types}")
    
    elif kind == "INPUT_OBJECT":
        print(f"input {name} {{")
        for input_field in type_info['inputFields']:
            field_type = get_type_name(input_field['type'])
            print(f"  {input_field['name']}: {field_type}")
        print("}")

# Helper function to recursively get the name of a type
def get_type_name(type_info):
    if type_info['kind'] == "NON_NULL":
        return f"{get_type_name(type_info['ofType'])}!"
    elif type_info['kind'] == "LIST":
        return f"[{get_type_name(type_info['ofType'])}]"
    return type_info['name']

# Main function to generate the schema
def generate_graphql_schema(introspection_json):
    for type_info in introspection_json['data']['__schema']['types']:
        if not type_info['name'].startswith("__"):  # Skip introspection types
            print_graphql_type(type_info)

# Load introspection JSON file and generate schema
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert introspection JSON to GraphQL schema.")
    parser.add_argument('file', type=str, help="Path to the introspection JSON file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load and process introspection JSON file
    introspection_json = load_introspection_file(args.file)
    generate_graphql_schema(introspection_json)

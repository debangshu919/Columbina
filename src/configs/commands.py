import yaml

# Define the path to your YAML file
yaml_file_path = "commands.yaml"

try:
    with open(yaml_file_path, "r") as file:
        data = yaml.safe_load(file)
except FileNotFoundError:
    print(f"Error: The file '{yaml_file_path}' was not found.")
except yaml.YAMLError as e:
    print(f"Error parsing YAML file: {e}")

COMMANDS = data

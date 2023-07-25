import re

CBOX = ""

def Getdata(valuename):
    # Check if the CBOX has the .cps extension
    if not CBOX.endswith('.cps'):
        raise ValueError("Invalid file type. Only .cps files are allowed.")

    with open(CBOX, 'r') as file:
        lines = file.readlines()

    multiline_string = False
    current_name = None
    current_value = None

    for line in lines:
        line = line.strip()
        if line.startswith("**") and line.endswith("**"):
            # Skip comments
            continue
        elif line.startswith("[>"):
            current_name = line[line.find("[>") + 2:-1].strip()
            multiline_string = line.startswith("[> ~\"")
            if multiline_string:
                current_value = ""
            else:
                current_value = None
        elif line == "]":
            multiline_string = False
        elif current_name is not None:
            if multiline_string:
                if line != "~\"":
                    current_value += line + "\n"
            else:
                current_value = line

        if current_name == valuename:
            return current_value

    return None

def printc(format_string):
    # Find all occurrences of $VALUE_NAME in the format_string using regular expressions
    placeholders = re.findall(r'\$([A-Za-z_]+)', format_string)

    # Initialize a dictionary to store the values for each placeholder
    values_dict = {}

    # Fetch the values for each placeholder using Getdata and store them in the values_dict
    for placeholder in placeholders:
        value = Getdata(placeholder)
        values_dict[placeholder] = value

    # Replace each placeholder with its corresponding value in the format_string
    for key, value in values_dict.items():
        format_string = format_string.replace(f"${key}", str(value))

    # Print the formatted string
    print(format_string)
from savey import end
def modify_line_in_file(file_path, line_number, new_content):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Modify the specific line
    if 1 <= line_number <= len(lines):
        lines[line_number - 1] = new_content + '\n'

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)
    file.close()

def new_value(value):
    modify_line_in_file('TTT\savey.py', 1, 'base='+ str(end))

    modify_line_in_file('TTT\savey.py', 2, 'base.append( '+ str(value)+')')

def reset():
    modify_line_in_file('TTT\savey.py', 1, 'base=[]')
    modify_line_in_file('TTT\savey.py', 2, '')
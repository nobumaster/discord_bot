
def read_text_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warning: {file_name} 無いよ.")
        return None

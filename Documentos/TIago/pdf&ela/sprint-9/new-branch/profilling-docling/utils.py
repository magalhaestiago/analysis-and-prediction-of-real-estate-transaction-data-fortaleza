import json
def filter_lines(lines, keywords):
    filtered_lines = [
        line for line in lines
        if any(keyword in line for keyword in keywords)
    ]
    
    return filtered_lines


def get_first_word(line):
    
    stripped = line.lstrip()
    
    parts = stripped.split(' ', 1)
    return parts[0] if parts else ''

def creating_dictionary(words, numbers):
    dictionary = {}
    for i in range(len(words)):
        dictionary[words[i]] = numbers[i]
    return dictionary


def get_time(result):
    numbers = []
    for i in range(len(result)): 
        numbers.append(get_first_word(result[i]))
        numbers[i] = float(numbers[i])
    return numbers


def remove_chars_of_dir(text):
    if '/' in text:
        return text.split('/', 1)[1]
    return text



def remove_word_pdf_or_txt(text):
    char_map = {
        ".pdf": "",
        ".txt": ""
    }
    for old_char, new_char in char_map.items():
        text = text.replace(old_char, new_char)
    return text



def remove_unnecessary_characters(text):
    char_map = {
        "|": " ",
        "`": " ",
        "-": " ",
    }
    for old_char, new_char in char_map.items():
        text = text.replace(old_char, new_char)
    return text


def convert_dict_to_json(dictionary, json_name):
    
    json_string = json.dumps(dictionary, indent=4)
    
    
    with open(json_name, "w") as json_file:
        json_file.write(json_string)


    

from utils import filter_lines, creating_dictionary, get_time, convert_dict_to_json, remove_chars_of_dir, remove_word_pdf_or_txt
import os


to_seek_dir = "txts"

for file in os.listdir(to_seek_dir):
    file_path = remove_word_pdf_or_txt(file)
    file_path = os.sep.join([to_seek_dir, file])
    
    
    
    with open(file_path, "r") as f:
        lines = f.readlines()

        docling_words = ["_build_document", "TableStructureModel.__call__", "LayoutModel.__call__", "EasyOcrModel.__call__", "PagePreprocessingModel.__call__", "StandardPdfPipeline._assemble_document"]

        result = filter_lines(lines, docling_words)
        numbers = get_time(result)

        
        if numbers[1] == numbers[2]:
            numbers[1] = 0
            numbers[2] = numbers[2] - numbers[3]
        else:
            numbers[1] = numbers[1] - numbers[2]
            numbers[2] = numbers[2] - numbers[3]

        dictionary = creating_dictionary(docling_words, numbers)
        file_path = os.sep.join([to_seek_dir, file])
        file_path = remove_chars_of_dir(file_path)
        file_path = remove_word_pdf_or_txt(file)
        
        

        if not os.path.exists("jsons"):
            os.makedirs("jsons")
        convert_dict_to_json(dictionary, "jsons/" + file_path + ".json")



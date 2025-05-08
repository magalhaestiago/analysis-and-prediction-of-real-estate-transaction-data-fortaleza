import sys

from pathlib import Path
import os
from src.document_relayout.core.backend.process_file import DoclingProcessor
from src.document_relayout.core.backend.process_file import process_file

from pyinstrument import Profiler
from utils import remove_chars_of_dir, remove_word_pdf_or_txt, remove_unnecessary_characters
profiler = Profiler()

to_seek_dir = sys.argv[1]

for file in os.listdir(to_seek_dir):
    profiler.start()

    file_path = os.sep.join([to_seek_dir, file])
    print(f"Processing {file_path}")

    result = process_file(file_path, DoclingProcessor(), "output")

    profiler.stop()

    

    text = profiler.output_text(unicode=False, color=False, show_all=True)
    text = remove_unnecessary_characters(text)
    file_path = remove_word_pdf_or_txt(file_path)
    file_path = remove_chars_of_dir(file_path)


    if not os.path.exists("txts"):
        os.makedirs("txts")
    with open("txts/" +file_path + ".txt", "w") as f:
        f.write(text)
    
    

    profiler.reset()


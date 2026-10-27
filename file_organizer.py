"""
File Organizer Script
Author: Kuban Turan

Description:
This script automatically organizes files in a specified directory into categorized subfolders based on their file extensions (e.g., images, videos, documents).

How to use:
1. By default, the script organizes the directory it is located in.
2. If you want to organize a specific folder (like your Downloads folder), simply change the 'TARGET_DIRECTORY' variable below to the correct path before running.
"""

import os 
import shutil

# Change this path if you want to organize a different folder. 
# Leave it as '.' to organize the current folder where the script is located.
TARGET_DIRECTORY = '.'

def downloads():
    return os.listdir(TARGET_DIRECTORY)

def order_dir(file=downloads()):
    path_dict={'.jpg':'images', '.png':'images', '.mp4':'videos', '.txt':'text_files', '.pdf':'documents', '.pptx':'presentations', '.zip':'archives', '.py':'python_files', '.docx':'word_docs'}
    for f in file:
        check=list(os.path.splitext(f))
        if os.path.isfile(f):
            for dir_type,path in path_dict.items():
                if check[1]==dir_type:
                    if not os.path.exists(path):
                        os.mkdir(path)
                    way = os.path.join(path,f)
                    while os.path.exists(way):
                        if check[0][-1].isdigit():
                            a=int(check[0][-1])+1
                            check[0] = check[0][:-1] + str(a)
                        else:
                            check[0]+='1'
                        way = os.path.join(path, ''.join(check))
                    shutil.move(f,way)
                    break
            else:
                if os.path.exists('Others'):
                    shutil.move(f,'Others')
                else:
                    os.mkdir('Others')
                    shutil.move(f,'Others')

order_dir()
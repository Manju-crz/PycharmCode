from mks.utility import MksFileSystem as fs
from mks.utility import MksThreads as t
from threading import *
import docx2txt


def get_files(folder):
    files = fs.get_all_files_folders(folder)
    import os
    file_list = []
    for file in files:
        os.path.isfile(folder + '\\' + file)
        file_list.append(file)
    return file_list


def return_files(folder1, folder2):
    t1 = t.MyThread(target=get_files, args=(folder1,))
    t2 = t.MyThread(target=get_files, args=(folder2,))
    t1.start()
    t2.start()
    return t1.join(), t2.join()


def compare_mismatched_files(old_folder, latest_folder, results_folder, mismatched_file, resulting_html_file):
    first_text = docx2txt.process(old_folder + "\\" + mismatched_file)
    second_text = docx2txt.process(latest_folder + "\\" + mismatched_file)

    first_text_readable_lines = []
    for txt in first_text.split("\n"):
        first_text_readable_lines.append(txt)

    seconds_text_readable_lines = []
    for txt in second_text.split("\n"):
        seconds_text_readable_lines.append(txt)

    curr_thread = current_thread().getName()
    file1 = curr_thread + "1.txt"
    file2 = curr_thread + "2.txt"
    fs.update_text_file(results_folder + file1, first_text_readable_lines)
    fs.update_text_file(results_folder + file2, seconds_text_readable_lines)
    fs.compare_two_files(results_folder + file1, results_folder + file2, results_folder + resulting_html_file)
    fs.delete_selected_files([results_folder + file1, results_folder + file2])

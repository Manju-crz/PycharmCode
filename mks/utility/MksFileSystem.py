import shutil
from pathlib import Path
import os
from filecmp import dircmp
import filecmp
import os
import glob


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent.parent


def get_all_files_folders(folder):
    return os.listdir(folder)


def is_file_same(main_file, sec_file):
    import filecmp
    return bool(filecmp.cmp(main_file, sec_file))


def clear_folder(folder_path):
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)


def create_new_text_file(filepath, file_text):
    file = open(filepath, "a+")
    file.write(file_text)
    file.close()


def update_text_file(filepath, list=[]):
    file = open(filepath, "a+")
    for txt in list:
        try:
            file.write(str(txt))
        except UnicodeEncodeError:
            pass
        file.write("\n")
    file.close()


def compare_two_files(file1, file2, html_result_file):
    import difflib
    difference = difflib.HtmlDiff().make_file(open(file1).readlines(), open(file2).readlines(), file1, file2)
    difference_report = open(html_result_file, "w")
    difference_report.write(difference)
    difference_report.close()


def delete_selected_files(files=[]):
    for fl in files:
        os.unlink(fl)

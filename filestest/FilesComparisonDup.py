from mks.utility import MksFileSystem as fs
from threading import *
from filestest import FilesThreadingUtil

folder = fs.get_project_root()
old_folder = str(folder) + "\\DocsFolder\\old"
latest_folder = str(folder) + "\\DocsFolder\\latest"
results_folder = str(folder) + "\\filetest_results\\"

old_files, latest_files = FilesThreadingUtil.return_files(old_folder, latest_folder)
common_files = list(set(old_files) & set(latest_files))
print("Common files are " + str(common_files))

fs.clear_folder(results_folder)
fs.create_new_text_file(results_folder + "results.txt", "Result\n======\n")
mismatched_list = []
for file in common_files:
    ans = fs.is_file_same(old_folder + "\\" + file, latest_folder + "\\" + file)
    if ans:
        fs.create_new_text_file(results_folder + "results.txt", str(file) + " : \tIdentical\n")
    else:
        fs.create_new_text_file(results_folder + "results.txt", str(file) + " : \tMismatched\n")
        mismatched_list.append(file)

print("Mismatched files ", mismatched_list)

import time

start_time = time.time()


class Compare:
    def compare_files(self, mismatched_file1, mismatched_file_html_report1):
        FilesThreadingUtil.compare_mismatched_files(old_folder, latest_folder, results_folder, mismatched_file1,
                                                    mismatched_file_html_report1)


threads = {}
for mismatched_file in mismatched_list:
    threads.update({mismatched_file: Thread})

for mismatched_file in mismatched_list:
    mismatched_file_html_report = mismatched_file + "__report.html"
    threads[mismatched_file] = Thread(target=Compare().compare_files, args=(mismatched_file, mismatched_file_html_report,))
    threads[mismatched_file].start()

for mismatched_file in mismatched_list:
    threads[mismatched_file].join()
    fs.create_new_text_file(results_folder + "error_result.txt", mismatched_file + " :\t" + results_folder +
                            mismatched_file + "__report.html" + "\n")
end_time = time.time()
print("Time difference is : ", end_time - start_time)

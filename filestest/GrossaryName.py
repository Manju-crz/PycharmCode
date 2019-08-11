from mks.utility import MksFileSystem as fs
from mks.utility import MksJsonReader
from mks.utility import MksHtmlGenerator

myfolder = str(fs.get_project_root()) + "\\DocsFolder\\GrossaryFiles\\"
results_folder = str(fs.get_project_root()) + "\\filetest_results\\"
fs.clear_folder(results_folder)
for myfile in fs.get_all_files_folders(myfolder):
    myfile, my_output_file = myfolder + myfile, results_folder + myfile + ".html"

    lines_list = MksJsonReader.read_file_in_txt(myfile)
    rep_txt = "Emergency Room Care"
    style_changer_start = """<u><font color="blue">"""
    style_changer_end = """</font></u>"""
    output_body_text = "<p>"
    for line in lines_list:
        if rep_txt and "name" in line:
            line = line.replace(rep_txt, style_changer_start + rep_txt + style_changer_end)
        output_body_text = output_body_text + "/<br>" + line
    output_body_text = output_body_text + "/<p>"
    MksHtmlGenerator.generate_html(my_output_file, output_body_text)

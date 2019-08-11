

def generate_html(output_file, bodytext):
    f = open(output_file, 'w')
    message = """<html>
    <head></head>
    <body>""" + bodytext + """</body>
    </html>"""
    f.write(message)
    f.close()


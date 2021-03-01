#!/usr/bin/env python3
import cgi, os
import cgitb

cgitb.enable()
form = cgi.FieldStorage()
fileitem = form['filename']
if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
else:
    fn = "Not found!"

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Проверка естественности текста</title>
        </head>
        <body>""")

print("<h1>Обработка данных форм!</h1>")
print("<p>Text from file: {}</p>".format(fn))

print("""</body>
        </html>""")
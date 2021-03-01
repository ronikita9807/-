#!/usr/bin/env python3
import cgi, os
import cgitb
import html
import main

cgitb.enable()
form = cgi.FieldStorage()
samples_len = form.getfirst("samples_len")
eps = form.getfirst("eps")
samples_len = html.escape(samples_len)
eps = html.escape(eps)
fileitem = form['filename']

if samples_len == "":
    samples_len = 50
if eps == "":
    eps = 0.1

samples_len = int(samples_len)
eps = float(eps)
text = ""
result = 0
if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    bytes = fileitem.file.read()
    text = bytes.decode("utf-8")

    result = main.text_naturalness(text, samples_len, eps)
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

print("<h1>Проверка естественности текста:</h1>")
print("<p>Имя файла: {}</p>".format(fn))
print("<p>Размер выборки: {}</p>".format(samples_len))
print("<p>Погрешность: {}</p>".format(eps))
print("<p>Естественность текста: {}%</p>".format(result * 100))

print("""</body>
        </html>""")

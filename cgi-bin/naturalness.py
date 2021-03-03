#!/usr/bin/env python3
import cgi, os
import cgitb
import main

cgitb.enable()
form = cgi.FieldStorage()
fileitem = form['filename']

text = ""
result = 0
tokens_len = 0
stopwords_len = 0
unique = 0
significant = 0
sickness = 0
if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    bytes = fileitem.file.read()
    text = bytes.decode("utf-8")

    result, tokens_len, stopwords_len, unique, significant, sickness = main.text_naturalness(text)
else:
    fn = "Not found!"

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Проверка естественности текста</title>
            <link rel="shortcut icon" href="../favicon.ico" type="image/x-icon">
        </head>
        <body style=\"background-color: aqua;\">""")
print("<div style=\"border: 3px solid #000;\">")
print("<h1 align=\"center\">Проверка естественности текста:</h1>")
print("<p align=\"center\">Имя файла: {}</p>".format(fn))
print("<p align=\"center\">Всего слов: {}</p>".format(tokens_len))
print("<p align=\"center\">Стоп-слов: {}</p>".format(stopwords_len))
print("<p align=\"center\">Уникальных словоформ: {}</p>".format(unique))
print("<p align=\"center\">Водность текста: {}%</p>".format(round(((tokens_len - significant)/tokens_len) * 100, 3)))
print("<p align=\"center\">Классическа тошнота: {}</p>".format(sickness))
print("<p align=\"center\">Естественность текста: {}%</p>".format(round(result * 100, 3)))
print("</div>")
print("<div style=\"font-size:20px;\">")
print("<p><u>Водность текста</u> определяется как отношение незначимых слов к общему количеству слов. То есть чем больше в статье значимых слов, тем меньше в итоге «воды». <br>Конечно, невозможно написать текст совсем без воды, нормальный показатель — 55%-75%.</p><br>")
print("<p><u>Классическая тошнота</u> определяется по самому частотному слову — как квадратный корень из количества его вхождений. <br><b>Важно!</b> Максимально допустимое значение классической тошноты зависит от объема текста — для 20 000 знаков тошнота, равная 5, будет нормальной, а для 1000 знаков — слишком высокой.</p><br>")
print("<p><u>Естественность текста определяется по закону Ципфа</u>. <br>Он говорит, что если упорядочить все слова определенного текста по уменьшению частоты их использования, то частота n-го слова будет около обратно-пропорциональной его рангу (порядковому номеру n). К примеру второе слово используется в два раза реже, чем первое, третье – в три раза, и так далее.</p><br>")
print("</div>")

print("""</body>
        </html>""")

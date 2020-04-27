#!/usr/bin/python
import cgi, cgitb
import html
from os import environ
import http.cookies

total_cnt = 0
cur_cnt = 0
prev_cnt = 0
#cookie_cnt = 0

cookie = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE"))

ilovecookies = cookie.get("prev_cnt")
if ilovecookies is not None:
        prev_cnt = int(ilovecookies.value)

try:
        with open("count.txt", 'r') as handler:
                total_cnt = handler.read()
                if total_cnt == "":
                        total_cnt = 0
                else:
                        total_cnt = int(total_cnt)
except FileNotFoundError as e:
        print(e)

form = cgi.FieldStorage()

def get_value(question, answer, t_counter, c_counter):
        if type(question) is list:
                question = ', '.join(question)
        if question == answer:
                t_counter += 1
                c_counter += 1
                question = str(question)
                question += " (верно)"
        elif question is None:
                question = "-"
        else:
                question = str(question)
                question += " (неверно)"
        return t_counter, c_counter, question

css_abbr = form.getvalue("css_abbr")
margin = form.getvalue("margin")
padding = form.getvalue("padding")
vmax = form.getvalue("vmax")

total_cnt, cur_cnt, css_abbr = get_value(css_abbr, "2", total_cnt, cur_cnt)
total_cnt, cur_cnt, margin = get_value(margin, "2", total_cnt, cur_cnt)
total_cnt, cur_cnt, padding = get_value(padding, "2, 3, 4", total_cnt, cur_cnt)
total_cnt, cur_cnt, vmax = get_value(vmax, "3", total_cnt, cur_cnt)

with open("count.txt", "w") as handler:
        handler.write(str(total_cnt))

print(f"Set-Cookie:prev_cnt={cur_cnt}")
print("Content-type: text/html")
print("<!DOCTYPE HTML>")
print()
print("<html>")
print("<head>")
print('<meta charset="utf-8">')
print('<link rel="icon" href="data:;base64,iVBORw0KGgo=">')
print("<title>Результаты теста</title>")
print("</head>")
print("<body>")
print('<div style="margin-left: 32%; padding: 10% ">')
print("<h1>Результаты</h1>")
print(f"<p> 1) {css_abbr}</p>")
print(f"<p> 2) {margin}</p>")
print(f"<p> 3) {padding}</p>")
print(f"<p> 4) {vmax}</p>")
print(f"<p> Ваш текущий счет: {cur_cnt}</p>")
print(f"<p> Ваш предыдущий счет: {prev_cnt}</p>")
print(f"<p> Общий счёт: {total_cnt}</p>")
print("</div>")
print(f"ilovecookies: {ilovecookies}")
print("</body>")
print("</html")

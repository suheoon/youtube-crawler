import requests, zipfile, io
r = requests.get('https://d26jfubr2fa7sp.cloudfront.net/Musics.zip')
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("./")

tj_dic = {}

f = open("musicbook_TJ.txt", "rt")
while True:
    line = f.readline()
    if line == '' :
        break
    s = line.split(sep='^')
    if s :
        keyword = s[0] + " " + s[1]
        number = s[2]
        tj_dic[number] = keyword
f.close()

url_number = set()

f = open("youtube_Url.txt", "rt")
while True:
    line = f.readline()
    if line == '':
        break
    s = line.split(sep='^')
    if s:
        number = s[0]
        url_number.add(number)
f.close()

keyword = []

for number, title in tj_dic.items():
    if number not in url_number:
        keyword.append(number+"^"+title)

f = open("url_keyword.txt", 'w')
for k in keyword:
    f.write(k + "\n")
f.close()
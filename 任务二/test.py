import codecs

f = codecs.open("thisTurn.txt","r+",encoding="utf-8")
html = f.readlines()
f.close()

a_set = set()
html = [item.split(":") for item in html]
for item in html:
    if len(item) == 3:
        a_set.add(item[2].strip())

print (len(a_set))

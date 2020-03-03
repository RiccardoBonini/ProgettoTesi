import svgwrite
from xml.dom import minidom

from xml.dom import minidom

doc = minidom.parse("Test1.svg")  # parseString also exists
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]

#print(path_strings[0])
#doc.unlink()
path_stringsM = []
for i in range(len(path_strings)):
    path_stringsM.append(path_strings[i].replace('M', ''))
    #path_strings[i].replace('L', '')

print(path_stringsM)
path_stringsL = []
for i in range(len(path_strings)):
    path_stringsL.append(path_stringsM[i].replace('L', ''))

print(path_stringsL)
    #path_strings[i].replace('L', '')

for j in range(len(path_stringsL)):
    for i in path_stringsL[j]:
         a = float(i)
         print(a)

dwg = svgwrite.Drawing('test.svg', profile='tiny')
dwg.add(dwg.line((327.2, 154.6), (331.4, 218), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line((160, 149.2), (268.8,148.8), stroke = svgwrite.rgb(10, 10, 16, '%')))
dwg.save()

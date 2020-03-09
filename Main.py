import svgwrite
from xml.dom import minidom
from xml.dom import minidom

doc = minidom.parse("Trial sheet_p3_20200309.svg")  # parseString also exists
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]

class Element:
    def __init__(self, xcoordinates, ycoordinates, tag):
        self.xcoordinates = xcoordinates
        self.ycoordinates = ycoordinates
        self.tag = tag

#print(path_strings[0])
#doc.unlink()
path_stringsM = []
for i in range(len(path_strings)):
    path_stringsM.append(path_strings[i].replace('M', ''))
    #path_strings[i].replace('L', '')

#print(path_stringsM)
path_stringsL = []
for i in range(len(path_strings)):
    path_stringsL.append(path_stringsM[i].replace('L', ''))

#print(path_stringsL)
    #path_strings[i].replace('L', '')
Xcoordinates = []
Ycoordinates = []
coordinates = []
elements = []

for i in range(len(path_stringsL)):
    coordinates.append(path_stringsL[i].split())

for i in range(len(coordinates)):
    support = []
    for j in range(0,len(coordinates[i]),2):
        support.append(coordinates[i][j])
    Xcoordinates.append(support)

for i in range(len(coordinates)):
    support = []
    for j in range(1,len(coordinates[i]),2):
        support.append(coordinates[i][j])
    Ycoordinates.append(support)

print(coordinates)
print(Xcoordinates)
print(Ycoordinates)

for i in range(len(coordinates)):
    if abs(float(Xcoordinates[i][-1]) - float(Xcoordinates[i][0])) < abs(float(Ycoordinates[i][-1]) - float(Ycoordinates[i][0])):
        #print("elemento numero:", i, " : linea verticale")
        elements.append(Element(Xcoordinates[i],Ycoordinates[i], "linea verticale"))
    else:
        #print("elemento numero:", i, " : linea orizzontale")
        elements.append(Element(Xcoordinates[i], Ycoordinates[i], "linea orizzontale"))
for i in range(len(elements)):
    print(elements[i].tag)
dwg = svgwrite.Drawing('test.svg', profile='tiny')
dwg.add(dwg.line((Xcoordinates[0][0], Ycoordinates[0][0]), (Xcoordinates[0][-1], Ycoordinates[0][-1]), stroke = svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.line((Xcoordinates[1][0], Ycoordinates[1][0]), (Xcoordinates[1][-1], Ycoordinates[1][-1]), stroke = svgwrite.rgb(10, 10, 16, '%')))
dwg.save()

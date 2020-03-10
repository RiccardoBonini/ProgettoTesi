import svgwrite
from xml.dom import minidom
from xml.dom import minidom

doc = minidom.parse("N Toaster D_p20_20200310.svg")  # parseString also exists
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]

class Element:
    def __init__(self, xcoordinates, ycoordinates, tag):
        self.xcoordinates = xcoordinates
        self.ycoordinates = ycoordinates
        self.tag = tag
        self.x1 = self.x2 = self.y1 = self.y2 = 0

    def adjust(self):
        if self.tag == "linea verticale":
            self.x1 = self.x2 = (min(self.xcoordinates) + max(self.xcoordinates)) / 2
            self.y1 = min(self.ycoordinates)
            self.y2 = max(self.ycoordinates)
        else:
            self.y1 = self.y2 = (min(self.ycoordinates) + max(self.ycoordinates)) / 2
            self.x1 = min(self.xcoordinates)
            self.x2 = max(self.xcoordinates)

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
    for j in range(len(coordinates[i])):
        coordinates[i][j] = float(coordinates[i][j])

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
    if abs(Xcoordinates[i][-1] - Xcoordinates[i][0]) < abs(Ycoordinates[i][-1] - Ycoordinates[i][0]):
        #print("elemento numero:", i, " : linea verticale")
        elements.append(Element(Xcoordinates[i],Ycoordinates[i], "linea verticale"))
    else:
        #print("elemento numero:", i, " : linea orizzontale")
        elements.append(Element(Xcoordinates[i], Ycoordinates[i], "linea orizzontale"))
for i in range(len(elements)):
    print(elements[i].tag)
    elements[i].adjust()
    print(elements[i].x1,elements[i].x2, elements[i].y1, elements[i].y2)

dwg = svgwrite.Drawing('test.svg', profile='tiny')
for i in range(len(elements)):
    dwg.add(dwg.line((elements[i].x1, elements[i].y1), (elements[i].x2, elements[i].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.line((Xcoordinates[1][0], Ycoordinates[1][0]), (Xcoordinates[1][-1], Ycoordinates[1][-1]), stroke = svgwrite.rgb(10, 10, 16, '%')))
dwg.save()

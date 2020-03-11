import svgwrite
from xml.dom import minidom

class Element:
    def __init__(self, xcoordinates, ycoordinates, tag):
        self.xcoordinates = xcoordinates
        self.ycoordinates = ycoordinates
        self.tag = tag
        self.x1 = self.x2 = self.y1 = self.y2 = 0
        # if self.tag == "linea verticale":
        #     self.x1 = x1
        #     self.x2 = (min(self.xcoordinates) + max(self.xcoordinates)) / 2
        #     self.y1 = y1
        #     self.y2 = max(self.ycoordinates)
        # else:
        #     self.y1 = y1
        #     self.y2 = (min(self.ycoordinates) + max(self.ycoordinates)) / 2
        #     self.x1 = x1
        #     self.x2 = max(self.xcoordinates)
        #
    def adjust(self, xupperbound, xlowerbound, yupperbound, ylowerbound):
        if self.tag == "linea verticale":
            self.x1 = (min(self.xcoordinates) + max(self.xcoordinates)) / 2
            self.x2 = (min(self.xcoordinates) + max(self.xcoordinates)) / 2
            self.y1 = self.ycoordinates[0]
            self.y2 = self.ycoordinates[-1]#max(self.ycoordinates)
        if self.tag == "linea orizzontale":
            self.y1 = (min(self.ycoordinates) + max(self.ycoordinates)) / 2
            self.y2 = (min(self.ycoordinates) + max(self.ycoordinates)) / 2
            self.x1 = self.xcoordinates[0]
            self.x2 = self.xcoordinates[-1]#max(self.xcoordinates)
        if abs(self.x1 - xupperbound) < 20: self.x1 = xupperbound
        if abs(self.x1 - xlowerbound) < 20: self.x1 = xlowerbound
        if abs(self.x2 - xupperbound) < 20: self.x2 = xupperbound
        if abs(self.x2 - xlowerbound) < 20: self.x2 = xlowerbound
        if abs(self.y1 - yupperbound) < 20: self.y1 = yupperbound
        if abs(self.y1 - ylowerbound) < 20: self.y1 = ylowerbound
        if abs(self.y2 - yupperbound) < 20: self.y2 = yupperbound
        if abs(self.y2 - ylowerbound) < 20 : self.y2 = ylowerbound
doc = minidom.parse("N Toaster D_p16_20200311.svg")  # parseString also exists
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]

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

# print(coordinates)
# print(Xcoordinates)
# print(Ycoordinates)

Xupperbound = 0
Xlowerbound = 5000
Yupperbound = 0
Ylowerbound = 5000

for i in range (len(Xcoordinates)):
    maximum = max(Xcoordinates[i])
    if Xupperbound < maximum: Xupperbound = maximum

for i in range (len(Xcoordinates)):
    minimum = min(Xcoordinates[i])
    if Xlowerbound > minimum: Xlowerbound = minimum

for i in range (len(Ycoordinates)):
    maximum = max(Ycoordinates[i])
    if Yupperbound < maximum: Yupperbound = maximum

for i in range (len(Ycoordinates)):
    minimum = min(Ycoordinates[i])
    if Ylowerbound > minimum: Ylowerbound = minimum

print(Xlowerbound, Xupperbound, Ylowerbound, Yupperbound)
for i in range(len(coordinates)):
    if abs(Xcoordinates[i][-1] - Xcoordinates[i][0]) < abs(Ycoordinates[i][-1] - Ycoordinates[i][0]):
        #print("elemento numero:", i, " : linea verticale")
        elements.append(Element(Xcoordinates[i],Ycoordinates[i], "linea verticale"))
    else:
        #print("elemento numero:", i, " : linea orizzontale")
        elements.append(Element(Xcoordinates[i], Ycoordinates[i], "linea orizzontale"))



for i in range(len(elements)):
    #print(elements[i].tag)
    elements[i].adjust(Xupperbound, Xlowerbound, Yupperbound, Ylowerbound)

# print(min(Xcoordinates[3]), min(Ycoordinates[3]), max(Xcoordinates[3]), max(Ycoordinates[3]))
# print(elements[3].x1, elements[3].y1, elements[3].x2, elements[3].y2)


dwg = svgwrite.Drawing('test.svg', profile='tiny')
for i in range(len(elements)):
    dwg.add(dwg.line((elements[i].x1, elements[i].y1), (elements[i].x2, elements[i].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# for i in range(len(Xcoordinates)):
#     dwg.add(dwg.line((Xcoordinates[i][0], Ycoordinates[i][0]), (Xcoordinates[i][-1],Ycoordinates[i][-1]),stroke=svgwrite.rgb(10, 10, 16, '%')))

# dwg.add(dwg.line((elements[0].x1, elements[0].y1), (elements[0].x2, elements[0].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[1].x1, elements[1].y1), (elements[1].x2, elements[1].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[2].x1, elements[2].y1), (elements[2].x2, elements[2].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[3].x1, elements[3].y1), (elements[3].x2, elements[3].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[4].x1, elements[4].y1), (elements[4].x2, elements[4].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[5].x1, elements[5].y1), (elements[5].x2, elements[5].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[6].x1, elements[6].y1), (elements[6].x2, elements[6].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[7].x1, elements[7].y1), (elements[7].x2, elements[7].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.line((elements[8].x1, elements[8].y1), (elements[8].x2, elements[8].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[9].x1, elements[9].y1), (elements[9].x2, elements[9].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[10].x1, elements[10].y1), (elements[10].x2, elements[10].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[11].x1, elements[11].y1), (elements[11].x2, elements[11].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.line((elements[12].x1, elements[12].y1), (elements[12].x2, elements[12].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.line((elements[13].x1, elements[13].y1), (elements[13].x2, elements[13].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[5].x1, elements[5].y1), (elements[5].x2, elements[5].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[6].x1, elements[6].y1), (elements[6].x2, elements[6].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((elements[7].x1, elements[7].y1), (elements[7].x2, elements[7].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.line((elements[-4].x1, elements[-4].y1), (elements[-4].x2, elements[-4].y2), stroke = svgwrite.rgb(10, 10, 16, '%')))


#dwg.add(dwg.line((Xcoordinates[1][0], Ycoordinates[1][0]), (Xcoordinates[1][-1], Ycoordinates[1][-1]), stroke = svgwrite.rgb(10, 10, 16, '%')))
dwg.save()

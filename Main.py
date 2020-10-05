import svgwrite
from xml.dom import minidom
import math
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageDraw
import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def distanceBetweenPoints(x1, y1, x2, y2):
    distance = math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))
    return distance

class Element:
    def __init__(self, xcoordinates, ycoordinates, tag):
        self.xcoordinates = xcoordinates
        self.ycoordinates = ycoordinates
        self.tag = tag
        self.x1 = self.x2 = self.y1 = self.y2 = 0
        self.neighbour1 = None
        self.neighbour2 = None
        self.flag1 = None
        self.flag2 = None
        self.stroke_width = 2
        self.role = None
        self.red = 0
        self.green = 0
        self.blue = 0
        if self.tag == 'camera':
            self.red = 255
            self.green = 255
            self.role = 'camera'

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
        if self.tag == 'linea verticale':
            self.x1 = (min(self.xcoordinates) + max(self.xcoordinates)) / 2
            self.x2 = (min(self.xcoordinates) + max(self.xcoordinates)) / 2
            self.y1 = self.ycoordinates[0]
            self.y2 = self.ycoordinates[-1]#max(self.ycoordinates)
        if self.tag == 'linea orizzontale':
            self.y1 = (min(self.ycoordinates) + max(self.ycoordinates)) / 2
            self.y2 = (min(self.ycoordinates) + max(self.ycoordinates)) / 2
            self.x1 = self.xcoordinates[0]
            self.x2 = self.xcoordinates[-1]#max(self.xcoordinates)
        if self.tag == 'linea diagonale':
            self.y1 = self.ycoordinates[0]
            self.y2 = self.ycoordinates[-1]
            self.x1 = self.xcoordinates[0]
            self.x2 = self.xcoordinates[-1]
        if abs(self.x1 - xupperbound) < 50: self.x1 = xupperbound
        if abs(self.x1 - xlowerbound) < 50: self.x1 = xlowerbound
        if abs(self.x2 - xupperbound) < 50: self.x2 = xupperbound
        if abs(self.x2 - xlowerbound) < 50: self.x2 = xlowerbound
        if abs(self.y1 - yupperbound) < 50: self.y1 = yupperbound
        if abs(self.y1 - ylowerbound) < 50: self.y1 = ylowerbound
        if abs(self.y2 - yupperbound) < 50: self.y2 = yupperbound
        if abs(self.y2 - ylowerbound) < 50: self.y2 = ylowerbound
        if self.tag != 'linea diagonale':
            if self.y2 < self.y1:
                tmp = self.y1
                self.y1 = self.y2
                self.y2 = tmp
            if self.x2 < self.x1:
                tmp = self.x1
                self.x1 = self.x2
                self.x2 = tmp

    def fix(self):
        if self.tag == 'linea verticale':
            if self.flag1 == True: self.y1 = self.neighbour1.y1
            if self.flag2 == True: self.y2 = self.neighbour2.y1
        if self.tag == 'linea orizzontale':
            if self.flag1 == True: self.x1 = self.neighbour1.x1
            if self.flag2 == True: self.x2 = self.neighbour2.x1
        if self.tag == 'linea diagonale':
            if self.flag1 == True:
                distance1 = distanceBetweenPoints(self.x1, self.y1, self.neighbour1.x1, self.neighbour1.y1)
                distance2 = distanceBetweenPoints(self.x1, self.y1, self.neighbour1.x2, self.neighbour1.y2)
                if distance1 < distance2:
                    self.x1 = self.neighbour1.x1
                    self.y1 = self.neighbour1.y1
                else:
                    self.x1 = self.neighbour1.x2
                    self.y1 = self.neighbour1.y2
                distance1 = distanceBetweenPoints(self.x2, self.y2, self.neighbour2.x1, self.neighbour2.y1)
                distance2 = distanceBetweenPoints(self.x2, self.y2, self.neighbour2.x2, self.neighbour2.y2)
                if distance1 < distance2:
                    self.x2 = self.neighbour2.x1
                    self.y2 = self.neighbour2.y1
                else:
                    self.x2 = self.neighbour2.x2
                    self.y2 = self.neighbour2.y2
            if self.flag2 == True:
                distance1 = distanceBetweenPoints(self.x2, self.y2, self.neighbour2.x1, self.neighbour2.y1)
                distance2 = distanceBetweenPoints(self.x2, self.y2, self.neighbour2.x2, self.neighbour2.y2)
                if distance1 < distance2:
                    self.x2 = self.neighbour2.x1
                    self.y2 = self.neighbour2.y1
                else:
                    self.x2 = self.neighbour2.x2
                    self.y2 = self.neighbour2.y2
                distance1 = distanceBetweenPoints(self.x1, self.y1, self.neighbour1.x1, self.neighbour1.y1)
                distance2 = distanceBetweenPoints(self.x1, self.y1, self.neighbour1.x2, self.neighbour1.y2)
                if distance1 < distance2:
                    self.x1 = self.neighbour1.x1
                    self.y1 = self.neighbour1.y1
                else:
                    self.x1 = self.neighbour1.x2
                    self.y1 = self.neighbour1.y2

print('Please select the SVG file')

Tk().withdraw()
filename = askopenfilename()

print('Running...')

doc = minidom.parse(filename)
svg_width = doc.getElementsByTagName('svg')[0].getAttribute('width')
svg_height = doc.getElementsByTagName('svg')[0].getAttribute('height')
# print(svg_width, svg_height)
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
verticalElements = []
horizontalElements = []
diagonalElements = []
special_symbols = []
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

# print(Xlowerbound, Xupperbound, Ylowerbound, Yupperbound)
for i in range(len(coordinates)):
    x_difference = abs(Xcoordinates[i][-1] - Xcoordinates[i][0])
    y_difference = abs(Ycoordinates[i][-1] - Ycoordinates[i][0])
    if abs(x_difference - y_difference) < 50:
        if distanceBetweenPoints(Xcoordinates[i][-1], Ycoordinates[i][-1], Xcoordinates[i][0], Ycoordinates[i][0]) < 40:
            special_symbols.append(Element(Xcoordinates[i], Ycoordinates[i], 'camera'))
        else : diagonalElements.append(Element(Xcoordinates[i],Ycoordinates[i], 'linea diagonale'))
    else :
        if abs(Xcoordinates[i][-1] - Xcoordinates[i][0]) < abs(Ycoordinates[i][-1] - Ycoordinates[i][0]):
        #print("elemento numero:", i, " : linea verticale")
            verticalElements.append(Element(Xcoordinates[i],Ycoordinates[i], 'linea verticale'))
        else:
        #print("elemento numero:", i, " : linea orizzontale")
            horizontalElements.append(Element(Xcoordinates[i], Ycoordinates[i], 'linea orizzontale'))

#print('Ci sono', len(diagonalElements), 'elementi diagonali')
#print('Ci sono', len(special_symbols), 'elementi speciali')

for i in range(len(verticalElements)):
    #print(elements[i].tag)
    verticalElements[i].adjust(Xupperbound, Xlowerbound, Yupperbound, Ylowerbound)

for i in range(len(horizontalElements)):
    #print(elements[i].tag)
    horizontalElements[i].adjust(Xupperbound, Xlowerbound, Yupperbound, Ylowerbound)

for i in range(len(diagonalElements)):
    # print("elemento diagonale:", i)
    # print(diagonalElements[i].xcoordinates)
    # print(diagonalElements[i].ycoordinates)
    diagonalElements[i].adjust(Xupperbound, Xlowerbound, Yupperbound, Ylowerbound)
    # print(diagonalElements[i].x1, diagonalElements[i].y1, diagonalElements[i].x2, diagonalElements[i].y2)

first_dwg = svgwrite.Drawing('First.svg')
first_dwg.viewbox(width= svg_width, height= svg_height)
for i in range(len(verticalElements)):
    first_dwg.add(first_dwg.line((verticalElements[i].x1, verticalElements[i].y1), (verticalElements[i].x2, verticalElements[i].y2), stroke = svgwrite.rgb(verticalElements[i].red, verticalElements[i].green, verticalElements[i].blue, '%'), stroke_width = verticalElements[i].stroke_width, id = verticalElements[i].role, onmouseover="playAudio()"))
for i in range(len(horizontalElements)):
    first_dwg.add(first_dwg.line((horizontalElements[i].x1, horizontalElements[i].y1), (horizontalElements[i].x2, horizontalElements[i].y2), stroke = svgwrite.rgb(horizontalElements[i].red, horizontalElements[i].green, horizontalElements[i].blue, '%'), stroke_width = horizontalElements[i].stroke_width, id = horizontalElements[i].role, onmouseover="playAudio()"))
for i in range(len(diagonalElements)):
    first_dwg.add(first_dwg.line((diagonalElements[i].x1, diagonalElements[i].y1), (diagonalElements[i].x2, diagonalElements[i].y2), stroke = svgwrite.rgb(diagonalElements[i].red, diagonalElements[i].green, diagonalElements[i].blue, '%'), stroke_width = diagonalElements[i].stroke_width, id = diagonalElements[i].role, onmouseover="playAudio()"))

first_dwg.save()

#ciclo per evidenziare i simboli speciali
special_dwg = svgwrite.Drawing('Special_Symbols.svg')
special_dwg.viewbox(width= svg_width, height= svg_height)
for i in range(len(special_symbols)):
    path_coordinates = 'M'
    for j in range(len(special_symbols[i].xcoordinates)):
        path_coordinates = path_coordinates + str(special_symbols[i].xcoordinates[j]) + ' '
        path_coordinates = path_coordinates + str(special_symbols[i].ycoordinates[j]) + ' '
        # path_coordinates = path_coordinates + str(special_symbols[0][j][0][1]) + ' '

    # print(special_symbols[i].red, special_symbols[i].green, special_symbols[i].blue)
    special_dwg.add(special_dwg.path(d=path_coordinates, stroke = svgwrite.rgb(0, 0, 0), stroke_width = 1))
special_dwg.save()


drawing = svg2rlg('Special_Symbols.svg')
renderPDF.drawToFile(drawing, "file.pdf")
renderPM.drawToFile(drawing, "file.png", fmt="PNG")

base = Image.open('file.png').convert('RGBA')
#print(special_symbols[i].xcoordinates, special_symbols[i].ycoordinates)
#ImageDraw.floodfill(base, (special_symbols[i].xcoordinates, special_symbols[i].ycoordinates), (0, 0, 255, 255))

#base.show()
base.save('special_symbols.png')

# Read image as gray-scale
img = cv2.imread('special_symbols.png', cv2.IMREAD_COLOR)
# Convert to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur the image to reduce noise
img_blur = cv2.medianBlur(gray, 5)
# cv2.imshow('A',gray)
# cv2.waitKey(0)
# Apply hough transform on the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, img.shape[0]/64, param1=200, param2=10, minRadius=5, maxRadius=30)
# Draw detected circles
if circles is not None:
    print('Ci sono cerchi!')
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # Draw outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # Draw inner circle
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
cv2.imshow('A',img)
cv2.waitKey(0)




# for i in range(len(horizontalElements)):
#     for j in range(len(horizontalElements)):
#         if i != j:
#             if abs(horizontalElements[i].y1 - horizontalElements[j].y1) <= 10:
#                 # horizontalElements[i].y1 = horizontalElements[j].y1
#                 # horizontalElements[i].y2 = horizontalElements[j].y1
#                 if horizontalElements[i].x1 > horizontalElements[j].x2:
#                     if abs(horizontalElements[i].x1 - horizontalElements[j].x2) > 50:
#                         horizontalElements[i].flag1 = False
#                     else: horizontalElements[i].flag1 = True
#                 if horizontalElements[i].x2 < horizontalElements[j].x1:
#                     if abs(horizontalElements[i].x2 - horizontalElements[j].x1) > 50:
#                         horizontalElements[i].flag2 = False
#                     else:  horizontalElements[i].flag2 = True
#
# for i in range(len(verticalElements)):
#     for j in range(len(verticalElements)):
#         if i != j:
#             if abs(verticalElements[i].x1 - verticalElements[j].x1) <= 10:
#                 # verticalElements[i].x1 = verticalElements[j].x1
#                 # verticalElements[i].x2 = verticalElements[j].x1
#                 if verticalElements[i].y1 > verticalElements[j].y2:
#                     if abs(verticalElements[i].y1 - verticalElements[j].y2) > 50:
#                         verticalElements[i].flag1 = False
#                     else: verticalElements[i].flag1 = True
#                 if verticalElements[i].y2 < verticalElements[j].y1:
#                     if abs(verticalElements[i].y2 - verticalElements[j].y1) > 50:
#                         verticalElements[i].flag2 = False
#                     else: verticalElements[i].flag2 = True

#cicli per individuare gli spazi vuoti ed assegnare gli eventuali elementi adiacenti
for i in range(len(verticalElements)):
    distance = 1000
    for j in range(len(horizontalElements)):
            if abs(verticalElements[i].y1 - horizontalElements[j].y1) < distance:
                distance = abs(verticalElements[i].y1 - horizontalElements[j].y1)
                verticalElements[i].neighbour1 = horizontalElements[j]
    if distance < 50: verticalElements[i].flag1 = True
    else :
        verticalElements[i].flag1 = False
    horizontal_distance = distance
    distance = 1000
    for j in range(len(verticalElements)):
        if i != j:
            if abs(verticalElements[i].x1 - verticalElements[j].x1) <= 30:
                # verticalElements[i].x1 = verticalElements[j].x1
                # verticalElements[i].x2 = verticalElements[j].x1
                if verticalElements[i].y1 > verticalElements[j].y2:
                    if abs(verticalElements[i].y1 - verticalElements[j].y2) < distance:
                        distance = abs(verticalElements[i].y1 - verticalElements[j].y2)
                        if distance < horizontal_distance:
                            verticalElements[i].neighbour1 = verticalElements[j]
                            verticalElements[i].x1 = verticalElements[j].x1
                            verticalElements[i].x2 = verticalElements[j].x2
    if distance < horizontal_distance:
        if distance < 50: verticalElements[i].flag1 = True
        else:
            verticalElements[i].flag1 = False
    distance = 1000
    for j in range(len(horizontalElements)):
        if abs(verticalElements[i].y2 - horizontalElements[j].y1) < distance:
            distance = abs(verticalElements[i].y2 - horizontalElements[j].y1)
            verticalElements[i].neighbour2 = horizontalElements[j]
    if distance < 50: verticalElements[i].flag2 = True
    else :
        verticalElements[i].flag2 = False
    horizontal_distance = distance
    distance = 1000
    for j in range(len(verticalElements)):
        if i != j:
            if abs(verticalElements[i].x1 - verticalElements[j].x1) <= 30:
                # verticalElements[i].x1 = verticalElements[j].x1
                # verticalElements[i].x2 = verticalElements[j].x1
                if verticalElements[i].y2 < verticalElements[j].y1:
                    if abs(verticalElements[i].y2 - verticalElements[j].y1) < distance:
                        distance = abs(verticalElements[i].y2 - verticalElements[j].y1)
                        if distance < horizontal_distance:
                            verticalElements[i].neighbour2 = verticalElements[j]
                            verticalElements[i].x1 = verticalElements[j].x1
                            verticalElements[i].x2 = verticalElements[j].x2
    if distance < horizontal_distance:
        if distance < 50:
            verticalElements[i].flag2 = True
        else:
            verticalElements[i].flag2 = False



for i in range(len(horizontalElements)):
    distance = 1000
    for j in range(len(verticalElements)):
        if abs(horizontalElements[i].x1 - verticalElements[j].x1) < distance:
            distance = abs(horizontalElements[i].x1 - verticalElements[j].x1)
            horizontalElements[i].neighbour1 = verticalElements[j]
    if distance < 50: horizontalElements[i].flag1 = True
    else :
        horizontalElements[i].flag1 = False
    vertical_distance = distance
    distance = 1000
    for j in range(len(horizontalElements)):
        if i != j:
            if abs(horizontalElements[i].y1 - horizontalElements[j].y1) <= 30:
                # horizontalElements[i].y1 = horizontalElements[j].y1
                # horizontalElements[i].y2 = horizontalElements[j].y1
                if horizontalElements[i].x1 > horizontalElements[j].x2:
                    if abs(horizontalElements[i].x1 - horizontalElements[j].x2) < distance:
                        distance = abs(horizontalElements[i].x1 - horizontalElements[j].x2)
                        if distance < vertical_distance:
                            horizontalElements[i].neighbour1 = horizontalElements[j]
                            horizontalElements[i].y1 = horizontalElements[j].y1
                            horizontalElements[i].y2 = horizontalElements[j].y2
    if distance < vertical_distance:
        if distance < 50:
            horizontalElements[i].flag1 = True
        else:
            horizontalElements[i].flag1 = False
    distance = 1000
    for j in range(len(verticalElements)):
        if abs(horizontalElements[i].x2 - verticalElements[j].x1) < distance:
            distance = abs(horizontalElements[i].x2 - verticalElements[j].x1)
            horizontalElements[i].neighbour2 = verticalElements[j]
    if distance < 50: horizontalElements[i].flag2 = True
    else :
        horizontalElements[i].flag2 = False
    vertical_distance = distance
    for j in range(len(horizontalElements)):
        if i != j:
            if abs(horizontalElements[i].y1 - horizontalElements[j].y1) <= 30:
                # horizontalElements[i].y1 = horizontalElements[j].y1
                # horizontalElements[i].y2 = horizontalElements[j].y1
                if horizontalElements[i].x2 < horizontalElements[j].x1:
                    if abs(horizontalElements[i].x2 - horizontalElements[j].x1) < distance:
                        distance = abs(horizontalElements[i].x2 - horizontalElements[j].x1)
                        if distance < vertical_distance:
                            horizontalElements[i].neighbour2 = horizontalElements[j]
                            horizontalElements[i].y1 = horizontalElements[j].y1
                            horizontalElements[i].y2 = horizontalElements[j].y2
    if distance < vertical_distance:
        if distance < 50:
            horizontalElements[i].flag2 = True
        else:
            horizontalElements[i].flag2 = False

for i in range(len(diagonalElements)):
    distance = 1000
    for j in range(len(horizontalElements)):
        if distanceBetweenPoints(diagonalElements[i].x1, diagonalElements[i].y1, horizontalElements[j].x1, horizontalElements[j].y1) < distance:
            distance = distanceBetweenPoints(diagonalElements[i].x1, diagonalElements[i].y1, horizontalElements[j].x1, horizontalElements[j].y1)
            diagonalElements[i].neighbour1 = horizontalElements[j]
        if distanceBetweenPoints(diagonalElements[i].x1, diagonalElements[i].y1, horizontalElements[j].x2, horizontalElements[j].y1) < distance:
            distance = distanceBetweenPoints(diagonalElements[i].x1, diagonalElements[i].y1, horizontalElements[j].x2, horizontalElements[j].y1)
            diagonalElements[i].neighbour1 = horizontalElements[j]
    #horizontal_distance = distance
    for j in range(len(verticalElements)):
        if distanceBetweenPoints(diagonalElements[i].x1, diagonalElements[i].y1, verticalElements[j].x1, verticalElements[j].y1) < distance:
            distance = distanceBetweenPoints(diagonalElements[i].x1, diagonalElements[i].y1, verticalElements[j].x1, verticalElements[j].y1)
            diagonalElements[i].neighbour1 = verticalElements[j]
        if distanceBetweenPoints(diagonalElements[i].x1, diagonalElements[i].y1, verticalElements[j].x1, verticalElements[j].y2) < distance:
            distance = distanceBetweenPoints(diagonalElements[i].x1, diagonalElements[i].y1, verticalElements[j].x1, verticalElements[j].y2)
            diagonalElements[i].neighbour1 = verticalElements[j]
    #diagonalElements[i].flag1 = True
    if distance < 50:
        diagonalElements[i].flag1 = True
    else: diagonalElements[i].flag1 = False
    distance1 = distance
    distance = 1000
    for j in range(len(horizontalElements)):
        #print(horizontalElements[j] == diagonalElements[i].neighbour1)
        if horizontalElements[j] != diagonalElements[i].neighbour1:
            if distanceBetweenPoints(diagonalElements[i].x2, diagonalElements[i].y2, horizontalElements[j].x1, horizontalElements[j].y1) < distance:
                distance = distanceBetweenPoints(diagonalElements[i].x2, diagonalElements[i].y2, horizontalElements[j].x1, horizontalElements[j].y1)
                diagonalElements[i].neighbour2 = horizontalElements[j]
            if distanceBetweenPoints(diagonalElements[i].x2, diagonalElements[i].y2, horizontalElements[j].x2, horizontalElements[j].y1) < distance:
                distance = distanceBetweenPoints(diagonalElements[i].x2, diagonalElements[i].y2, horizontalElements[j].x2, horizontalElements[j].y1)
                diagonalElements[i].neighbour2 = horizontalElements[j]
    #horizontal_distance = distance
    for j in range(len(verticalElements)):
        #print(verticalElements[j] == diagonalElements[i].neighbour1)
        if verticalElements[j] != diagonalElements[i].neighbour1:
            if distanceBetweenPoints(diagonalElements[i].x2, diagonalElements[i].y2, verticalElements[j].x1, verticalElements[j].y1) < distance:
                distance = distanceBetweenPoints(diagonalElements[i].x2, diagonalElements[i].y2, verticalElements[j].x1, verticalElements[j].y1)
                diagonalElements[i].neighbour2 = verticalElements[j]
            if distanceBetweenPoints(diagonalElements[i].x2, diagonalElements[i].y2, verticalElements[j].x1, verticalElements[j].y2) < distance:
                distance = distanceBetweenPoints(diagonalElements[i].x2, diagonalElements[i].y2, verticalElements[j].x1, verticalElements[j].y2)
                diagonalElements[i].neighbour2 = verticalElements[j]
    #diagonalElements[i].flag2 = True
    if distance < 50:
        diagonalElements[i].flag2 = True
    else: diagonalElements[i].flag2 = False
    distance2 = distance
    if distance1 < distance2:
        diagonalElements[i].flag2 = False
    else: diagonalElements[i].flag1 = False


#cicli per sistemare gli spazi vuoti
for i in range(len(verticalElements)):
    verticalElements[i].fix()
    elements.append(verticalElements[i])

for i in range(len(horizontalElements)):
    horizontalElements[i].fix()
    elements.append(horizontalElements[i])

for i in range(len(diagonalElements)):
    # print("punto1 elemento diagonale :", i, ":", diagonalElements[i].x1, diagonalElements[i].y1)
    # print("punto2 elemento diagonale :", i, ":", diagonalElements[i].x2, diagonalElements[i].y2)
    diagonalElements[i].fix()
    # print("Neighbour1 elemento diagonale:", i, ":", diagonalElements[i].flag1, diagonalElements[i].neighbour1.x1, diagonalElements[i].neighbour1.y1, diagonalElements[i].neighbour1.x2, diagonalElements[i].neighbour1.y2 )
    # print("Neighbour2 elemento diagonale:", i, ":", diagonalElements[i].flag2, diagonalElements[i].neighbour2.x1, diagonalElements[i].neighbour2.y1, diagonalElements[i].neighbour2.x2, diagonalElements[i].neighbour2.y2 )
    # print("punto1 elemento diagonale dopo fix:", i, ":", diagonalElements[i].x1, diagonalElements[i].y1)
    # print("punto2 elemento diagonale dopo fix:", i, ":", diagonalElements[i].x2, diagonalElements[i].y2)
    #print('Elemento diagonale ', i, diagonalElements[i].neighbour1.x1, diagonalElements[i].neighbour1.y1, diagonalElements[i].neighbour1.x2, diagonalElements[i].neighbour1.y2, diagonalElements[i].neighbour2.x1, diagonalElements[i].neighbour2.y1, diagonalElements[i].neighbour2.x2, diagonalElements[i].neighbour2.y2)
    elements.append(diagonalElements[i])


#ciclo per individuare il bordo esterno
topElement = horizontalElements[0]
for i in range(len(horizontalElements)):
    if horizontalElements[i].y1 < topElement.y1:
        topElement = horizontalElements[i]

# print(topElement.y1)
loop = True
current = topElement
next = topElement.neighbour2
visited = []

while loop == True:
    current.stroke_width = 15
    current.role = 'bordo'
    visited.append(current)
    if current.neighbour2 not in visited:
        next = current.neighbour2
    else: next = current.neighbour1
    current = next
    if current == topElement:
        loop = False

for i in range(len(elements)):
    if elements[i].role != 'bordo':
        if elements[i].tag == 'linea diagonale':
            elements[i].role = 'porta'
            elements[i].stroke_width = 8
            elements[i].red = 50
            elements[i].green = 250
            elements[i].blue = 50
        else:
            elements[i].role = 'interno'
            elements[i].red = 255
            elements[i].green = 0
            elements[i].blue = 0

dwg = svgwrite.Drawing('Final_SVG.svg', size=('100%', '100%'))
empty_dwg = svgwrite.Drawing('Empty.svg')

dwg.viewbox(width= svg_width, height= svg_height)
empty_dwg.viewbox(width= svg_width, height= svg_height)

for i in range(len(elements)):
    dwg.add(dwg.line((elements[i].x1, elements[i].y1), (elements[i].x2, elements[i].y2), stroke = svgwrite.rgb(elements[i].red, elements[i].green, elements[i].blue, '%'), stroke_width = elements[i].stroke_width, id = elements[i].role, onmouseover="playAudio()"))
    empty_dwg.add(empty_dwg.line((elements[i].x1, elements[i].y1), (elements[i].x2, elements[i].y2), stroke=svgwrite.rgb(elements[i].red, elements[i].green, elements[i].blue, '%'), stroke_width=elements[i].stroke_width, id=elements[i].role, onmouseover="playAudio()"))

dwg.save()
empty_dwg.save()

for i in range(len(special_symbols)):

    drawing = svg2rlg("Empty.svg")
    renderPDF.drawToFile(drawing, "file.pdf")
    renderPM.drawToFile(drawing, "file.png", fmt="PNG")

    base = Image.open('file.png').convert('RGBA')
    #print(special_symbols[i].xcoordinates, special_symbols[i].ycoordinates)
    ImageDraw.floodfill(base, (special_symbols[i].xcoordinates[0], special_symbols[i].ycoordinates[0]), (0, 0, 255, 255))

    #base.show()
    base.save('final_file.png')

    image = cv2.imread('final_file.png')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv, low_blue, high_blue)
    blue = cv2.bitwise_and(image, image, mask = blue_mask)

    #cv2.imshow('Blue', blue)
    #cv2.waitKey(0)
    cv2.imwrite('blue.jpg', blue)

    im = cv2.imread('blue.jpg')
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 10, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    path_coordinates = 'M'
    for j in range(len(contours[0])):
        path_coordinates = path_coordinates + str(contours[0][j][0][0]) + ' '
        path_coordinates = path_coordinates + str(contours[0][j][0][1]) + ' '

    #print(special_symbols[i].red, special_symbols[i].green, special_symbols[i].blue)
    dwg.add(dwg.path(d = path_coordinates, fill = svgwrite.rgb(special_symbols[i].red, special_symbols[i].green, special_symbols[i].blue), id = special_symbols[i].role, onmouseover="playAudio()"))
    dwg.save()
    #cv2.imshow('A', thresh)
    #cv2.waitKfey(0)


html_svg = open('Final_SVG.svg', 'r').read()
#print(html_svg)

Html_file= open("Final_Plan.html","w")
Html_file.write("""<meta name="viewport" content="width=device-width, initial-scale=1.0">""")
Html_file.write(html_svg)
Html_file.write("""<script>

    var audio1 = new Audio();
    audio1.src = 'http://iss240.net/tempfiles/menu-click/1.mp3';
    var audio2 = new Audio();
    audio2.src = 'http://iss240.net/tempfiles/sound-effects/5.mp3';
    var audio3 = new Audio();
    audio3.src = 'http://iss240.net/tempfiles/sound-effects/3.mp3';

    function playAudio(id) {

        //var id = event.srcElement.id;
        if (id == "bordo"){
            audio1.play();
            navigator.vibrate(200);
            //alert("riproduco audio bordo")
        }
        else if(id == "interno"){
            audio2.play();
            alert("riproduco audio interno")
        }
        else if(id == "porta"){
            audio3.play();
            alert("riproduco audio porta")
        }
        else if(id == "camera"){
            audio1.play();
            alert("riproduco audio camera")
        }
    }

    function touchStart(e){

        e.preventDefault();
        // e.preventDefault();
        // var target = e.target;
        // targetID = target.id;
        // if (targetID == 'camera'){
        //     //alert("sto toccando camera")
        //     target.fill = "rgb(0,0,255)";
        //     target.style.left = '900px';
        //     target.style.top = '500px';
        // }
        // var touch = e.touches[0];
        // var moveOffsetX = target.offsetLeft - touch.pageX;
        // var moveOffsetY = target.offsetTop - touch.pageY;
        //
        // target.addEventListener('touchmove', function () {
        //     if (targetID == 'camera'){
        //         alert("sto muovendo il dito")
        //         // target.fill = "rgb(0,0,255)";
        //         // target.style.left = '900px';
        //         // target.style.top = '500px';
        //     }
        //     var positionX = touch.pageX + moveOffsetX;
        //     var positionY = touch.pageY + moveOffsetY;
        //     target.style.left = positionX + 'px';
        //     target.style.top = positionY + 'px';
        //
        // }, false);

    }

    function getTouchMouseTargetElement(e) {
        if (e.touches) {
            return document.elementFromPoint(e.touches[0].pageX, e.touches[0].pageY);
        }
        return e.target;
    }

    function touchMove(e){

        //alert('Sto muovendo il dito')
        e.preventDefault();
        //navigator.vibrate(200);
        var target = getTouchMouseTargetElement(e);
        targetID = target.id;
        playAudio(targetID)
        // if (targetID == 'camera'){
        //     alert("sto toccando camera")
        //     target.fill = "rgb(0,0,255)";
        //     target.style.left = '900px';
        //     target.style.top = '500px';
        // }




    }
    
   
    document.querySelector('body').addEventListener('touchstart', touchStart, false)
    document.querySelector('body').addEventListener('touchmove', touchMove, false)
</script>
""")
Html_file.close()
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

#print(path_stringsM)
path_stringsL = []
for i in range(len(path_strings)):
    path_stringsL.append(path_stringsM[i].replace('L', ''))

#print(path_stringsL)
    #path_strings[i].replace('L', '')
Xcoordinates = []
Ycoordinates = []
coordinates = []

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

# dwg = svgwrite.Drawing('test.svg', profile='tiny')
# dwg.add(dwg.line((Xcoordinates[0], Ycoordinates[0][1]), (coordinates[0][-2], coordinates[0][-1]), stroke=svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.line((coordinates[1][0], coordinates[1][1]), (coordinates[1][-2], coordinates[1][-1]), stroke = svgwrite.rgb(10, 10, 16, '%')))
# dwg.save()

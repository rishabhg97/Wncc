import urllib.request
import json
import codecs
import pprint
import fileinput
import math


def origin():  # to define the origin
    orig='IIT Bombay,Powai'
    orig=orig.replace(' ','%20')
    print(orig)
    return orig

def accessiblebyroad(res): ## returns whether the destination is accessible by road or not
    if res["status"] == "ZERO_RESULTS" :
        return False
    else:
        return True


def mergesort(mylist):

    if len(mylist)>1:
        mid = len(mylist)//2
        lefthalf = mylist[:mid]
        righthalf = mylist[mid:]

        mergesort(lefthalf)
        mergesort(righthalf)

        i = 0
        j = 0
        k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i].distance < righthalf[j].distance:
                mylist[k]=lefthalf[i]
                i += 1
            else:
                mylist[k]=righthalf[j]
                j += 1
            k += 1

        while i < len(lefthalf):
            mylist[k]=lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            mylist[k]=righthalf[j]
            j += 1
            k += 1


class GlobalPos:## gps class
    def __init__(self, x, y):
        self.latitude = x
        self.longitude = y


class InfoOnAccessible:## accessible
    def __init__(self, st, disr):
        self.place = st
        self.distance = disr


class InfoOnInaccessible:
    def __init__(self, nam):
        self.place = nam





urlstart = 'https://maps.googleapis.com/maps/api/directions/json?origin='
origin = origin()
dest = '&destination='
key = '&key=AIzaSyCmVNsWuU_qpSPEy6mvVAIxL8-9df7Zuac'
roadaccessible = []
roadinaccessible = []

destlist = []

f = open('t.txt')## open file of your choice
line=f.readline()
while line:
    destlist.append(line)
    line=f.readline()
f.close()
no = len(destlist)

for i in range(0, no):
    print(destlist[i])

for i in range(0, no):
    destination = str(destlist[i])
    destination = destination.replace(' ','%20')
    url = urlstart+origin+dest+destination+key
    openreq = urllib.request.urlopen(url)
    reader = codecs.getreader("utf-8")
    result = json.load(reader(openreq))
    distc = 0
    if accessiblebyroad(result):
        distc = result["routes"][0]["legs"][0]["distance"]["value"]
        inf = InfoOnAccessible(destination, distc)
        roadaccessible.append(inf)
    else:
        uninf = InfoOnInaccessible(destination)
        roadinaccessible.append(uninf)

mergesort(roadaccessible) ## sorting done

finallist= roadaccessible + roadinaccessible ## final list

z = 0
print('The cities in order of their distance from IIT Bombay :')
'''while z <len(finallist):
    print(finallist[z].place)
    z += 1'''
## for two global points

newlist = finallist
globalurl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
global_origi = origin.replace('%20','+')
global_list = []
global_desti = str(destlist[0])
globaloriginurl = globalurl + global_origi + key
global_openreq = urllib.request.urlopen(globaloriginurl)
global_oreader = codecs.getreader("utf-8")
global_oresult = json.load(global_oreader(global_openreq))
pprint.pprint(global_oresult)
gpsorigipos = GlobalPos(global_oresult["results"][0]["geometry"]["location"]["lat"],global_oresult["results"][0]["geometry"]["location"]["lng"])
def spheredist(gps_original, gpsorigipos1):
    alpha1 = float(gpsorigipos1.latitude)
    phi1 = float(gpsorigipos1.longitude)
    alpha = float(gps_original.latitude)
    phi = float(gps_original.longitude)
    x1 = math.cos(alpha1)*math.sin(phi1)
    y1 = math.cos(alpha1)*math.cos(phi1)
    z1 = math.sin(alpha1)
    x2 = math.cos(alpha)*math.sin(phi)
    y2 = math.cos(alpha)*math.cos(phi)
    z2 = math.sin(alpha)
    angle = math.acos(x1*x2 + y1*y2 + z1*z2 )
    dist = 6371000 * angle
    return dist

for var1 in range(0, no):
    global_desti = str(destlist[var1])
    global_destifin = global_desti.replace(' ','+')
    globalfinalurl = globalurl + global_destifin + key
    global_openreq = urllib.request.urlopen(globalfinalurl)
    global_reader = codecs.getreader("utf-8")
    global_result = json.load(global_reader(global_openreq))
    gpspos1 = GlobalPos(global_result["results"][0]["geometry"]["location"]["lat"], global_result["results"][0]["geometry"]["location"]["lng"])
    g_distance = spheredist(gpspos1, gpsorigipos)
    print(g_distance)
    temp = InfoOnAccessible(global_desti, g_distance)
    global_list.append(temp)


for varh1 in range(0, no):
    print(global_list[varh1].place)
    print(global_list[varh1].distance)

mergesort(global_list)
for varh in range(0, no):
    print(global_list[varh].place)
    print(global_list[varh].distance)







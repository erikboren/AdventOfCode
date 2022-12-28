with open("day15 data.txt") as file:
    input = file.readlines()

y_to_check = 10   
y_to_check = 2000000 
import numpy as np

# find max x and y

x = list()
y = list()
maxx = 0
maxy = 0
sensor_x = list()
sensor_y = list()
beacon_x = list()
beacon_y = list()
dist = list()


for line in input:
    line = line.strip()
    x1 = int(line[line.find("x="):line.find(",")][2:])
    y1 = int(line[line.find("y="):line.find(":")][2:])

    x2= int(line[line.rfind("x="):line.rfind(",")][2:])
    y2 = int(line[line.rfind("y="):][2:])

    x.append(x1)
    x.append(x2)
    y.append(y1)
    y.append(y2)

    sensor_x.append(x1)
    sensor_y.append(y1)

    beacon_x.append(x2)
    beacon_y.append(y2)

    dist.append(abs(x1-x2) + abs(y1-y2))

#  Construct map matrix

y_limits = list()
x_limits = list()

for i in range(len(sensor_x)):

    x_limits.append(sensor_x[i]+dist[i])
    x_limits.append(sensor_x[i]-dist[i])


x_size_orig = max(x)- min(x)

x_size = max(x_limits) - min(x_limits)
# Metod for converting coordinates.

def convert(xc):
    xc = xc + (x_size - x_size_orig)  
    return xc

map = np.full(x_size*2,".")

# Fill map with sensors and beacons:

def mark_non_beacons(map,ys,xs,dist,y_to_check,m="#"):
    y_dist = abs(ys-y_to_check)
    def x_dist(xs,x):
        return abs(xs-x)
    
    for idx,cell in enumerate(map):
        if y_dist+x_dist(xs,idx) <= dist and cell ==".":
            map[idx] = "#"
        
    
    return map


for i in range(len(sensor_x)):
    print(i)
    ys, xs = sensor_y[i], convert(sensor_x[i])
    yb, xb = beacon_y[i],convert(beacon_x[i])

    if ys == y_to_check:
        map[xs] == "S"
    if yb == y_to_check:
        map[xb] = "B"

    map = mark_non_beacons(map,ys,xs,dist[i],y_to_check)

def save(map,x,y,maxdist):
    # vectorx=np.arange(min(x),min(x)+maxdist+1)
    # vectory = np.arange(min(y)-1,min(y)+maxdist+3)

    # map = np.insert(map,0,vectorx, axis=0)
    # map = np.insert(map,0,vectory,axis=1)
    np.savetxt("day15.out",map,fmt="%s")
    
count = 0


# save(map,x,y,max(dist))
for cell in map:
    if cell =="#" or cell =="S":
        count +=1

print(map[-1])
print(count)



import numpy as np
import copy
sand_point = [0,500]

with open("day14 data.txt") as file:
    rocks = file.readlines()

width_limits = [400,525]

height_limits = [0,180]

grid1 = np.full((height_limits[1],width_limits[1]-width_limits[0]),".")



def convert_width(width,width_limits):
    return width - width_limits[0]-1

sand_point = [sand_point[0], convert_width(sand_point[1],width_limits)]

grid1[0][convert_width(500,width_limits)] = "+"

def connect_points(p1,p2,grid):
    p1 = [p1[0],convert_width(p1[1],width_limits)]
    p2 = [p2[0],convert_width(p2[1],width_limits)]
    ydiff = p1[0] - p2[0]
    xdiff = p1[1] - p2[1]

    grid[p1[0]][p1[1]] = "#"
    grid[p2[0]][p2[1]] = "#"

    if xdiff == 0:
        direction = 1
        if ydiff <0:
            direction = -1
        ydiff = direction*ydiff 
        while ydiff > 0:
            grid[p1[0] -direction*ydiff][p1[1]] = "#"

            ydiff -= 1
    elif ydiff == 0:
        direction = 1
        if xdiff <0:
            direction = -1
        xdiff = direction * xdiff 
        while xdiff > 0:
            grid[p1[0],p1[1] - direction*xdiff] = "#"

            xdiff -= 1
    return grid
ymax = 0        
for line in rocks:
    line = line.strip()
    line = line.split(" -> ")
    for idx , point in enumerate(line):
        if idx >0:
            x2 = int(point.split(",")[0])
            y2 = int(point.split(",")[1])
            
            x1 = int(line[idx-1].split(",")[0])
            y1 = int(line[idx-1].split(",")[1])
            
            grid1 = connect_points([y1,x1],[y2,x2],grid1)

            if y1 > ymax:
                ymax = y1
            if y2 > ymax:
                ymax = y1




def drop(grid,sand_point):

    def extend(grid,x):
        if x == 1:
            vector = grid[:,0]
            grid =np.insert(grid,0,vector, axis=1)

        else:
            xmax = np.shape(grid)[1] -1
            vector = grid[:,xmax]
            grid = np.insert(grid,xmax,vector,axis = 1)

        return grid

    loc = sand_point
    rest = False
    output = None
    while not rest:

        if loc[1] == 1 or loc[1] == np.shape(grid)[1]-1:
            
            grid = extend(grid,loc[1])
            
            if loc[1] == 1:
                loc[1] += 1
                sand_point[1] +=1 
                print("sand_point :" + str(sand_point))
            
            print("Extended " + str(np.shape(grid)))
        if loc[0] == np.shape(grid)[0]-1:
            output = "of"
            break
        if grid[loc[0]+1,loc[1]] == ".":
            loc = [loc[0]+1,loc[1]]
        elif grid[loc[0]+1][loc[1]-1] == ".":
            loc = [loc[0]+1,loc[1]-1]
        elif grid[loc[0]+1][loc[1]+1] == ".":
            loc = [loc[0]+1,loc[1]+1]
        else:
            rest = True
        
    grid[loc[0]][loc[1]] = "o"
    if loc[0] == 0:
        output = "sp"
    
    return grid,output,sand_point

overflow = False
sand_counter = -1

grid2 = copy.deepcopy(grid1)

while not overflow:
    grid1, output, sand_point = drop(grid1,sand_point)
    if output == "of":
        overflow = True
    sand_counter += 1

print(sand_counter)

np.savetxt('day14 p1.out',grid1,fmt='%s')  

# create floor:
print(ymax)
floor = ymax+2
for idx,cell in enumerate(grid2[floor]):
    grid2[floor][idx] ="#"

p2 = False
sand_counter = 0

while not p2:
    sand_counter +=1
    grid2, output, sand_point = drop(grid2,sand_point)
    if(sand_counter%100 == 0):
        print(sand_counter)  
    if output == "sp" or sand_counter == 30000:
        p2 = True

print(sand_counter)

np.savetxt('day14 p2.out',grid2,fmt='%s')  
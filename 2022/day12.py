import numpy as np
import re
import sys
sys.setrecursionlimit(1000)
with open("day12 data.txt") as file:
    input = file.readlines()

start = None
goal = None

xmax = len(input[0].strip())
ymax = len(input)


map = np.zeros((ymax,xmax), dtype =int)

for idxy, line in enumerate(input):
    line = line.strip()
    for idxx, char in enumerate(line):
        if char == "S":
            start = [idxy,idxx]
        elif char == "E":
            goal = [idxy,idxx]
        map[idxy][idxx] = ord(char)

map[start[0],start[1]] = 97
map[goal[0],goal[1]] = 122

visited = np.full((ymax,xmax), False)

numbered =np.linspace(0,ymax*xmax-1,ymax*xmax).astype(int).reshape((ymax,xmax))


adjacency =  np.zeros((ymax*xmax,ymax*xmax))

for idx1, line in enumerate(numbered):
    for idx2, cell in enumerate(line):
        y= idx1
        x= idx2
        height = map[y][x]
        if(x != 0):
            adjacent_nbr = numbered[y][x-1]
            a_height = map[y][x-1]-1
            if(height>= a_height):
                adjacency[cell][adjacent_nbr] = 1
        if(x != xmax-1):
            adjacent_nbr = numbered[y][x+1]
            a_height = map[y][x+1]-1
            if(height>= a_height):
                adjacency[cell][adjacent_nbr] = 1
        if(y != 0):
            adjacent_nbr = numbered[y-1][x]
            a_height = map[y-1][x]-1
            if(height>= a_height):
                adjacency[cell][adjacent_nbr] = 1
        if(y != ymax-1):
            adjacent_nbr = numbered[y+1][x]
            a_height = map[y+1][x]-1
            if(height>= a_height):
                adjacency[cell][adjacent_nbr] = 1

def bsf(start,map,adjacency,numbered,goal):
    
    def solve(start,visited,adjacency,numbered):
        que = np.array([start])
        number = numbered[start[0]][start[1]]
        visited = np.full((ymax,xmax), False)
        prev = np.full((ymax,xmax), None)
        visited[start[0]][start[1]] = True

        while len(que) >0:
            node = que[0]

            number = numbered[node[0]][node[1]]
            
            
            for idx, adjacent in enumerate(adjacency[number]):
                if adjacent == 1:
                    next = np.array([np.where(numbered == idx)[0][0],np.where(numbered == idx)[1][0]])
                    if( not visited[next[0]][next[1]]):
                        que = np.append(que,[next],axis =0)
                        visited[next[0]][next[1]] = True
                        # print(next)
                        prev[next[0]][next[1]] = str(node[0])+ ":" + str(node[1])
            
            que = np.delete(que,0,0)
            
        return prev
    
    prev = solve(start,visited,adjacency,numbered)
    # print(prev)
    def recronstruct(start,goal,prev):
        path = np.array([goal])
        cell = goal
        size = 0
        while cell != start and prev[cell[0]][cell[1]] != None:
            next_cellx = int(prev[cell[0]][cell[1]].split(":")[1])
            next_celly = int(prev[cell[0]][cell[1]].split(":")[0])
            # print(cell)
            cell = [next_celly, next_cellx]
            path = np.append(path, [cell], axis =0)
            size += 1
        if(path[-1][0] == start[0] and path[-1][1] == start[1]):
            return size
        else:
            return prev.size*prev.size
    return recronstruct(start,goal,prev)
# size = bsf(start,map,adjacency,numbered,goal)
# print("Task1: " + str(size))

# FIND ALL CELLS WITH HEIGHT a

path_sizes = list()

height_a = ord("a")

a_indexes = np.where(map == height_a)

a_cells = np.full((a_indexes[0].size,2), None)

for idx,cell in enumerate(a_indexes[0]):
    a_cells[idx][0] = a_indexes[0][idx]
    a_cells[idx][1] = a_indexes[1][idx]
print(len(a_cells))
for idx,cell in enumerate(a_cells):
    print(idx)
    # RUN bsf to find the shortest path from current a_cell to the goal (same goal as in part 1)
    size = bsf(cell.tolist(),map,adjacency,numbered,goal)
    path_sizes.append(size)

print("Shortest path: " + str(min(path_sizes)))




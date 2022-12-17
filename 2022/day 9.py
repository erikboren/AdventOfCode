import numpy as np
with open("day9 data.in") as file:
    head_moves = file.readlines()


# [y,x]
# head = [0,0]
# tail = [0,0]

knots = []

nbr_of_knots = 10

start = np.array([0,0])

for i in range(nbr_of_knots):
    knots.append(start)

knots =np.asarray(knots)


dir = dict()


dir["U"] = [1,0]
dir["D"] =[-1,0]
dir["L"] = [0,-1]
dir["R"] =[0,1]



def distance(knot1,knot2):
    # returns true if distance is larger than 1 diagonal
    return (abs(knot1[0]-knot2[0])**2 + abs(knot1[1]- knot2[1])**2)**(1/2)

def move(knot,direction):
    for idx,coord in enumerate(knot):
            knot[idx] = int(knot[idx]) + dir[direction][idx]

    return knot
    

tail_spaces = set()

# add the start point to the set tail_spaces
tail_spaces.add(str(start))

for head_move in head_moves:
    head_move = head_move.strip()
    head_direction = head_move[0]
    head_steps = int(head_move[head_move.rfind(" "):])

    
    for i in range(head_steps):

        # Move head
        
        for idx,knot in enumerate(knots):
            
            if idx == 0:
                knot = move(knot,head_direction)
                pass
            else:
                knot_ahead = knots[idx-1]
                dist = distance(knot,knot_ahead)

                if dist <=2**(1/2):
                    # Either right next to or on top or diagonal. Not enough distance to move knot
                    continue
                else:
                    # check distance in y-dir
                    if knot[0] > int(knot_ahead[0]):
                        knot = move(knot, "D")
                    elif knot[0] < int(knot_ahead[0]):
                        knot = move(knot,"U")
                    # distance in x-dir
                    if knot[1] > int(knot_ahead[1]):
                        knot = move(knot,"L")
                    elif knot[1] < int(knot_ahead[1]):
                        knot = move(knot,"R")
                    
                    if(idx == nbr_of_knots -1):
                        # if tail
                        tail_spaces.add(str(knot))

print(len(tail_spaces))

   
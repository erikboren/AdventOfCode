class sensor:
    def __init__(self,pos: tuple[int,int], beacon: tuple[int,int]) -> None:
        self.pos = pos
        self.beacon = beacon
        self.dist = abs(pos[0]-beacon[0]) + abs(pos[1]-beacon[1])

def overlap(range1: tuple[int,int], range2: tuple[int,int]) -> bool:
    return range1[0] <= range2[0] <= range1[1] or range2[0] <= range1[0] <= range2[1]

class exc_range:
    def __init__ (self) -> None:
        self.ranges = []

    def add_range(self,start,stop):
        res: list[tuple[int,int]] = []
        overlaps: list[tuple[int,int]] = []

        for rstart,rstop in self.ranges:
            if overlap((rstart,rstop), (start,stop)):
                overlaps.append((min(rstart,start), max(rstop,stop)))
            else: res.append((rstart,rstop)) #Transfer all non overlapping existing ranges to res.

        if len(overlaps) >=1:
            mins = min(map(lambda range: range[0],overlaps))
            maxe = max(map(lambda range: range[1],overlaps))
            res.append((mins,maxe))

        else: res.append((start,stop))

        res.sort()

        self.ranges = res
        # This ensures that the number of ranges are kept to a minimum.
    def remove_point(self,point):
        res: list[tuple[int,int]] = []
        for rstart, rstop in self.ranges:
            if rstart < point < rstop:
                # if the point is inside a range, split the range and append both parts
                res.append((rstart,point-1))
                res.append((point+1,rstop))
            elif rstart == point:
                res.append((point+1,rstop))
            elif rstop == point:
                res.append((rstart,point-1))
            else:
                res.append((rstart,rstop))
        self.ranges = res

def find_unavailable_pos(y,sensors: list[sensor]) -> list[tuple[int,int]]:
    res: exc_range = exc_range()

    occupied: list[int] = []

    for sensor in sensors:
        distance_left = sensor.dist - abs(sensor.pos[1]-y)

        if distance_left <=0:
            continue
        if sensor.pos[1] == y:
            occupied.append(sensor.pos[0])
        if sensor.beacon[1] == y:
            occupied.append(sensor.beacon[0])
        rstart = sensor.pos[0] - distance_left
        rstop = sensor.pos[0] + distance_left

        res.add_range(rstart,rstop)
    
    # for point in occupied:
    #     res.remove_point(point)
    
    return res.ranges

def find_beacon(ranges,limit,y) -> None:
    for i in range(len(ranges)-1):
        
        range1 = ranges[i]
        range2 = ranges[i+1]

        if range1[1] != range2[0]-1:
            x  = range1[1]+1
            if x > limit or x <0:
                return 0
            else:
                print("Frequency: " + str(x*4000000+y))
                return 1


def parse(string: str):
    res: list[sensor] = []
    for line in string.splitlines():
        first, second = line.split(": ")
        x, y = first[12:].split(", ")
        x = int(x)
        y = int(y[2:])

        bx, by = second[23:].split(", ")
        bx = int(bx)
        by = int(by[2:])
        res.append(sensor((x, y), (bx, by)))

    return res

def main(input):
    sensors = parse(input)
    limit = 4000000
    for y in range(0,limit+1):
        res = find_beacon(find_unavailable_pos(y,sensors),limit,y)
        if res == 1:
            break

if __name__ == "__main__":
    with open("day15 data.txt") as f:
        input = f.read()
    print(main(input))

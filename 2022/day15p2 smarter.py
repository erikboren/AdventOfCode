class sensor:
    def __init__(self,pos: tuple[int,int], beacon: tuple[int,int]) -> None:
        self.pos = pos
        self.beacon = beacon
        self.dist = abs(pos[0]-beacon[0]) + abs(pos[1]-beacon[1])

    def inside_range(self, point: tuple[int,int]) -> bool:
        return distance(self.pos,point) <= self.dist

    def lines(self) -> list[tuple[int,int]]:
        res: list[tuple[int,int]] = []
        y = self.pos[1]
        x = self.pos[0]
        d = self.dist
        # lines surrounding the "diamond" of the sensor, 1,2,3,4, in the counter-clockwise direction starting at the top right.
        # example line 1 goes through (x-sensor,ysensor+dist) and (x-sensor+dist,y)
        # straigh lines on the formula y=kx+m, here all k =1 or k=-1
        line1 = (-1,y+d+x+1)
        line2 = (1,y+d-x+1)
        line3 = (-1,y+x-d-1)
        line4 = (1,y-x-d-1)

        res.append(line1)
        res.append(line2)
        res.append(line3)
        res.append(line4)

        return res


def distance(point1: tuple[int,int], point2: tuple[int,int]) -> int:
    return abs(point1[0]-point2[0]) + abs(point1[1] - point2[1])

def free(sensors,point) -> bool:
    for sensor in sensors:
        if sensor.inside_range(point):
            return False
    
    return True



def find_beacon(sensors,limit) -> None:
    lines: dict[tuple[int,int],int] = {}

    for sensor in sensors:
        for line in sensor.lines():
            if line in lines:
                lines[line] +=1
            else:
                lines[line] =1

    asc_lines: list[int] = []
    desc_lines: list[int] =[]

    # Since k can only be 1 or -1 we only need to store the m-value and divide them into lists that have either k = 1 or k = -1

    for line,count in lines.items():
        if count >1:
            if line[0] ==-1:
                desc_lines.append(line[1]) # m-value
            else:
                asc_lines.append(line[1])

    points: list[tuple[int,int]] = []
    
    for m_asc in asc_lines:
        for m_desc in desc_lines:
            x = (m_desc-m_asc) // 2
            y = -x+m_desc
            points.append((x,y))

    for point in points:
        if 0<= point[0] <= limit and 0<= point[1] <= limit and free(sensors,point):
            print("Point: " + str(point))
            return point[0]*4000000+point[1]







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

def main(input,limit):
    sensors = parse(input)
    return find_beacon(sensors,limit)
    

if __name__ == "__main__":
    with open("day15 data.txt") as f:
        input = f.read()
    limit = 4000000
    print(main(input,limit))

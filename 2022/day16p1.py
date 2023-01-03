import copy
import time
class valve:
    def __init__(self,name:str, flow: int,adj: list[str],id) -> None:
        self.name = name
        self.flow = flow
        self.adj = adj
        self.open = False
        self.duration = 0
        self.id = id

    def pass_time(self) -> None:
        if self.open:
            duration += 1
    
    def total_volume(self) -> int:
        return self.flow*self.duration


def parse(input) -> list[valve]:
    valves: dict[int[valve]] = {}
    id = 0
    for line in input:
        line = line.strip()
        valve_name: str = line[6:8]
        flow:int = int(line[23:line.find(";")])
        
        adj1:list[str] = line.split(" ")[9:]
        adj:list[str] = []
        
        for adjvalve in adj1:
            adj.append(adjvalve.split(",")[0])
        
        valves[valve_name] = valve(valve_name,flow,adj,id)
        id += 1
    return valves

def find_distances(valves:list[valve]) -> dict[tuple[str,str]]:
    # finds the smallest distance between each combination of two vales  
        res:dict[tuple[str,str]] = {}
        def bsf(start: str,valves:list[valve])->dict[str,str]:
            visited: list[str] = []
            prev:dict(str,str) = {}
            que:list[str] = []
            visited.append(start)
            que.append(start)

            while len(que)>0:
                node = que[0]

                for neighbour in valves[node].adj:
                    if not neighbour in visited:
                        que.append(neighbour)
                        visited.append(neighbour)
                        prev[neighbour] = node
                
                que.pop(0)
            
            return prev
        
        def reconstruct(start: str,end:str,prev)-> int:
            path:list[str] = []
            path.append(end)

            node = end
            while node != start:
                node = prev[node]
                path.append(node)

            return len(path)-1
        for start in valves:
            prev = bsf(start,valves)
            for end in valves:
                res[start,end] = reconstruct(start,end,prev)    

        return res

def solve(valves: list[valve], distances:dict[tuple[str,str]],start_location:str,time_cap:int)->int:
    valves = {k:v for (k,v) in valves.items() if k==start_location or v.flow>0}
    # Filter out all valves with a flow not larger than 0
    
    # At each point in time you can either move to a valve with a flow rate, open a valve, or do nothing

    pressure_relived:list[int] = []

    # node (state) =time,location, opened valves, flow, acc.flow
    node = dict()
    node["time"] = 0
    node["location"] = start_location
    node["open_valves"] = []
    node["flow"] = 0
    node["acc_flow"] = 0
    
    best = 0
    flow_pot:dict[tuple[int,int]] = {}

    que:list[list[dict,str,str]] = []

    if not node["location"] in node["open_valves"] and valves[node["location"]].flow >0 and node["time"]<time_cap-1:
        que.append([node,"open",node["location"],1])

    # Possible move-locations
    
    for valve in valves:
        if not valve in node["open_valves"] and valve != node["location"] and valve != "AA":
            if distances[valve,node["location"]] + node["time"] < time_cap:
                que.append([node,"move",valve,distances[valve,node["location"]]])



    counter = 0
    while len(que) >0:
        counter += 1

        que_item = que[0]

        action = que_item[1]
        target = que_item[2]
        time = que_item[3]
        
        node = copy.deepcopy(que_item[0])
        node["acc_flow"] += node["flow"]*time
        
        
        
        

        if action == 'move':
            node["time"] += time
            node["location"] = target

        if action == "open":
            node["time"] += time
            node["flow"] += valves[node["location"]].flow
            node["open_valves"].append(target)
        
        que_not_extended = True

        cut = False
        
        der = node["flow"]
        acc = node["acc_flow"]
        
        # Pruning by checking if both the integral (flow acc) and derivative (flow) has been achieved with fewer time passed.

        for time in flow_pot:
            if time<node["time"]:
                if flow_pot[time][0] > der and flow_pot[time][1] > acc:
                    cut = True
        
        if not cut:
            if node["time"] in flow_pot:
                if der > flow_pot[node["time"]][0] and acc > flow_pot[node["time"]][1]:
                    flow_pot[node["time"]] =(der,acc)
                    
            else: 
                flow_pot[node["time"]] = (der,acc)
      
        
        
        

        if not node["location"] in node["open_valves"] and valves[node["location"]].flow >0 and node["time"]<time_cap-1 and not cut:
            que.append([node,"open",node["location"],1])
            que_not_extended = False

        # Possible move-locations
        
        for valve in valves:
            if not valve in node["open_valves"] and valve != node["location"] and valve != "AA" and action != "move" and not cut:
                if len(node["open_valves"]) != len(valves):
                    if distances[valve,node["location"]] + node["time"] < time_cap -2:
                        que.append([node,"move",valve,distances[valve,node["location"]]])
                        que_not_extended = False


        


        que.pop(0)
        if que_not_extended:
            res = node["acc_flow"]+node["flow"]*(time_cap-node["time"])
            pressure_relived.append(res)
            if res > best:
                best = res

    return best


def main(input):
    valves = parse(input)
    distances = find_distances(valves)

    start_location = "AA"
    time_cap = 30

    print(solve(valves,distances,start_location,time_cap))






if __name__ == "__main__":
    st = time.time()
    with open("day16 data.txt") as f:
        input = f.readlines()
    main(input)
    et = time.time()
    print("Time: " + str(et-st))
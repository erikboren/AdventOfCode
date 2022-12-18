import math

class monkey:
    def __init__(self, id,starting_items, operation, throw_test, true_throw, false_throw):
        self.id = id
        self.throw_test = throw_test
        self.operation = operation
        self.true_throw = int(true_throw)
        self.false_throw = int(false_throw)
        self.inspected = 0
        self.modulo = 0

        self.inventory = starting_items

    def do_operation(self,item):
        item = int(item)
        if(self.operation.startswith("old +")):
            return item + int(self.operation[6:])
        elif(self.operation == "old * old"):
            return item*item
        elif (self.operation.startswith("old *")):
            return item * int(self.operation[6:])

            # parse operation

    def throw(self,to_id,item):
        self.inventory.pop(0)
        return to_id, item

    def inspect(self):
        self.inspected += 1

    def recieve(self,item):
        self.inventory.append(item)

    def process_item(self,part = 1):
        self.inspect()
        self.inventory[0] = self.do_operation(self.inventory[0])
        test = 0
        if part ==1:
            self.inventory[0] = self.inventory[0]//3
            test = self.inventory[0]
        elif part == 2:
            self.inventory[0] = self.inventory[0] % self.modulo


        if(self.inventory[0] % self.throw_test == 0):
            return self.throw(self.true_throw,self.inventory[0])

        else:
            return self.throw(self.false_throw,self.inventory[0])

    def no_items(self):
        return len(self.inventory)

monkeys = []

with open("day11 data.txt") as file:
    monkeys_in = file.readlines()


for idx,line in enumerate(monkeys_in):
    if line.startswith("Monkey "):
        # id
        id =line[7:line.rfind(":")]

        # starting items
        item_line = monkeys_in[idx+1].strip()
        starting_items = item_line[item_line.find("Starting items: ")+len("Starting items: )")-1:].split(", ")
    
        # Operation 
        operation_line = monkeys_in[idx+2].strip()
        operation = operation_line[operation_line.find("Operation: new = ") + len("Operation: new = "):]

        # Test:
        test_line = monkeys_in[idx+3].strip()
        test = int(test_line[test_line.find("Test: divisible by ")+len("Test: divisible by ")-1:])

        #True throw:
        true_throw_line = monkeys_in[idx+4].strip()
        true_throw = int(true_throw_line[true_throw_line.find("throw to monkey ")+len("throw to monkey ")-1:])

        #False throw:
        false_throw_line = monkeys_in[idx+5].strip()
        false_throw = int(false_throw_line[false_throw_line.find("throw to monkey ")+len("throw to monkey ")-1:])

        monkeys.append(monkey(id,starting_items,operation,test,true_throw,false_throw))

        
modulo = 1

for monkey in monkeys:
    modulo *= monkey.throw_test

print(modulo)
for monkey in monkeys:
    monkey.modulo = modulo

for i in range(10000):
    print(i)
    for monkey in monkeys:
        while monkey.no_items() > 0:
            reciever_id, item = monkey.process_item(2)
            monkeys[reciever_id].recieve(item)

def print_monkey_inventories(monkeys):
    for monkey in monkeys:
        print("Monkey " + monkey.id + ":")
        print(monkey.inventory)
    
print_monkey_inventories(monkeys)

def print_monkey_inspections(monkeys):
    for monkey in monkeys:
        print("Monkey " + monkey.id + ":")
        print(monkey.inspected)

print_monkey_inspections(monkeys)

def monkey_business(monkeys):
    first = 0
    second = 0

    for monkey in monkeys:
        if monkey.inspected > second:
            if monkey.inspected > first:
                second = first
                first = monkey.inspected
                
            else: 
                second = monkey.inspected
        
    return first*second


print(monkey_business(monkeys))
import numpy as np
import time
norm_k = 0
def std(values: list[float]):
    s: float = sum(values)/len(values)
    return np.sqrt(sum([(x-s)**2 for x in values]))
def mu(size:tuple) -> float:
    return size[0]*size[1]
def cost(chips,circuit_chips,circuit_connectivities,imbalance_cost:float = 100,interconnectivity_cost:float = 200):
    cost: float = 0
    for i in range(len(circuit_chips)):
        for j in range(len(circuit_chips)):
            if circuit_chips[i] != circuit_chips[j]:
                cost += interconnectivity_cost*circuit_connectivities[i][j]/norm_k
    cost += std([sum([mu(circuit_mapping[i]["size"]) for i in range(0,len(circuit_chips)) if j==current[i]])/mu(chips[j]["size"]) for j in range(0,len(chips))])*imbalance_cost
    return cost
def random_neighbour(chips: list[object], circuit_chips: list[int],circuit_mapping,n=0):
    if(n >= 5):
        return circuit_chips
    neighbour: list[int] = circuit_chips.copy()
    index: int = np.random.randint(0,len(neighbour))
    new_chip: int = np.random.randint(0,len(chips))
    while new_chip == neighbour[index]:
        new_chip: int = np.random.randint(0,len(chips))
    neighbour[index] = new_chip
    for j in range(0,len(chips)):
        if sum([mu(circuit_mapping[i]["size"]) for i in range(0,len(neighbour)) if j==neighbour[i]]) > mu(chips[j]["size"])*0.9:
            return random_neighbour(chips,circuit_chips,circuit_mapping,n=n+1)
    return neighbour
if __name__ == "__main__":

    # get chips
    chip_file = open("./chips.txt")
    chips: list[object] = []
    for chip in chip_file:
        args: list[str] = chip.split(" ")
        chips.append({"name":args[0],"size":(int(args[1]),int(args[2]))})
    chip_file.close()

    print("\n--- CHIPS ---")
    print(chips)

    # get circuit types
    circuit_type_file = open("./circuit_types.txt")
    circuit_types: dict[str] = {}
    for circuit_type in circuit_type_file:
        args: list[str] = circuit_type.split(" ")
        circuit_types[args[0]] = (int(args[1]),int(args[2]))
    circuit_type_file.close()
    print("\n--- CIRCUIT TYPES ---")
    print(circuit_types)

    # get circuits
    circuit_file = open("./circuits.txt")
    circuits: dict[dict[str]] = {}
    circuit_connections: list[object] = []
    for circuit in circuit_file:
        args: list[str] = circuit.split(" ")
        if args[0] not in circuits:
            circuits[args[0]] = {"id":len(circuits),"size":circuit_types[args[0].split("_")[0]]}
        if args[1] not in circuits:
            circuits[args[1]] = {"id":len(circuits),"size":circuit_types[args[1].split("_")[0]]}
        circuit_connections.append({"name_0":args[0],"name_1":args[1],"connectivity":int(args[2])})
        norm_k += int(args[2])
    circuit_type_file.close()
    circuit_mapping: list[object] = [None]*len(circuits)
    circuit_connectivities: np.ndarray = np.zeros((len(circuits),len(circuits)))
    for circuit_connection in circuit_connections:
        circuit_connectivities[circuits[circuit_connection["name_0"]]["id"]][circuits[circuit_connection["name_1"]]["id"]] = circuit_connection["connectivity"]
    for circuit in circuits:
        circuit_mapping[circuits[circuit]["id"]]  = {"name":circuit,"size":circuits[circuit]["size"]}
    circuit_file.close()
    print("\n--- CIRCUITS ---")
    print(circuits)
    print("\n--- CIRCUIT MAPPING ---")
    print(circuit_mapping)
    print("\n--- CONNECTIVITIES ---")
    print(circuit_connectivities)  
    avg_time: float = 0
    avg_start_cost: float = 0
    avg_end_cost: float = 0
    for k in range(50):
        current: np.ndarray = random_neighbour(chips,np.random.randint(0,len(chips),size=(len(circuits))),circuit_mapping,n=-100)
        print(f"{current} has cost: {cost(chips,current,circuit_connectivities)}")
        avg_start_cost += cost(chips,current,circuit_connectivities)
        T:float = 1000
        start_time = time.time()
        while T > 0.01:
            T *= 0.9
            for N in range(1,100):
                neighbour = random_neighbour(chips,current,circuit_mapping)
                p: float = min(np.exp(-(cost(chips,neighbour,circuit_connectivities)-cost(chips,current,circuit_connectivities))/T),1)
                if p >= np.random.rand():
                    current = neighbour.copy()
        avg_time += time.time() - start_time
        print(f"{current} has cost: {cost(chips,current,circuit_connectivities)}")
        avg_end_cost += cost(chips,current,circuit_connectivities)
    print(f"avg_time = {avg_time/50} s")
    print(f"avg_start_cost = {avg_start_cost/50}")
    print(f"avg_end_cost = {avg_end_cost/50}")
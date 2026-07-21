# Python program to print Eulerian circuit in given
# directed graph using Hierholzer algorithm

# Function to print Eulerian circuit
def printCircuit(adj):
    n = len(adj)

    if n == 0:
        return []

    # Maintain a stack to keep vertices
    # We can start from any vertex, here we start with 0
    currPath = [0]

    # list to store final circuit
    circuit = []

    while len(currPath) > 0:
        print(f" currPath={currPath}")
        currNode = currPath[-1]

        # If there's remaining edge in adjacency list
        # of the current vertex
        if len(adj[currNode]) > 0:

            # Find and remove the next vertex that is
            # adjacent to the current vertex
            nextNode = adj[currNode].pop()

            # Push the new vertex to the stack
            currPath.append(nextNode)
            print(f"   append nextNode={nextNode}")

        # back-track to find remaining circuit
        else:
            # Remove the current vertex and
            # put it in the circuit
            circuit.append(currPath.pop())
            print(f"   circuit append {circuit[-1]}")

    # reverse the result vector
    circuit.reverse()

    return circuit


if __name__ == "__main__":
    # adj = [[2, 3], [0], [1], [4], [0]]
    adj = [[3, 2], [0], [1], [4], [0]]
    ans = printCircuit(adj)

    for v in ans:
        print(v, end=" ")
    print()
# A recursive DFS based function used by getSCCs()
# u        -> The vertex to be visited next
# disc[]   -> Stores discovery times of visited vertices
# low[]    -> Earliest visited vertex that can be reached
#             from subtree rooted with current vertex
# st       -> Stack to store all active DFS vertices
# inSt[]   -> Boolean array to check whether a node is in stack
# timer    -> Global time counter for discovery times
# allSCCs  -> Stores all strongly connected components
def findSCC(u, adj, disc, low, inSt, st, timer, allSCCs):
    """Tarjan Algorithm to find all SCCs in directed graph"""

    # Initialize discovery time and low value
    timer[0] += 1  # timer is list so that we can update its item value
    disc[u] = low[u] = timer[0]

    # Push current vertex to stack and mark it as in stack
    st.append(u)
    inSt[u] = True

    # Go through all vertices adjacent to this
    for v in adj[u]:

        # If v is not visited yet, then recur for it
        # Case 1: Tree edge
        if disc[v] == -1:

            findSCC(v, adj, disc, low, inSt, st, timer, allSCCs)

            # Check if the subtree rooted with v has a
            # connection to one of the ancestors of u
            low[u] = min(low[u], low[v])

        # Update low value of u only if v is still in stack
        # Case 2: Back edge (not cross edge)
        elif inSt[v]:
            low[u] = min(low[u], disc[v])

    # If u is head node of SCC, pop the stack and store the SCC
    if low[u] == disc[u]:

        scc = []

        # Pop all vertices from stack till u is found
        while True:

            x = st.pop()
            inSt[x] = False
            scc.append(x)

            if x == u:
                break

        # Store one strongly connected component
        allSCCs.append(scc)


# The function to do DFS traversal.
# It uses findSCC() to find all strongly connected components
def getSCCs(adj):

    n = len(adj)
    disc = [-1] * n
    low = [-1] * n
    inSt = [False] * n

    st = []
    timer = [0]
    allSCCs = []

    # Call the recursive helper function to find SCCs
    # in DFS tree with vertex i
    for i in range(n):

        if disc[i] == -1:
            findSCC(i, adj, disc, low, inSt, st, timer, allSCCs)

    return allSCCs


if __name__ == "__main__":

    adj = [[] for _ in range(6)]

    # Graph construction
    adj[0].append(1)
    adj[1].append(2)
    adj[2].append(0)
    adj[2].append(3)
    adj[3].append(4)
    adj[4].append(3)
    adj[4].append(5)

    sccs = getSCCs(adj)

    print("Strongly Connected Components:")
    for scc in sccs:
        print(*scc)
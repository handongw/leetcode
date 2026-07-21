class SCC:
    # Function to return all the strongly connected components of a graph.
    def findSCC(self, n, edges):
        """ n - number of vertex. 
            edges - adjacent directed edge list
        """

        adjacent_map = {} # key is from vertex, value is list of to vertex
        for i in range(n):
            adjacent_map[i] = []

        for e in edges:
            adjacent_map[e[0]].append(e[1])

        UNVISITED = 0;   PROGRESS = 1;  VISITED = 2
        visited = [UNVISITED for i in range(n)]

        leader_list = [i for i in range(n)] # union-find data structure

        def get_leader(u):
            parent = leader_list[u]
            if parent == u:
                return u

            root = get_leader(parent)
            leader_list[u] = root
            return root

        def union(v, u):
            """ merge from v to u """
            lu = get_leader(u)
            lv = get_leader(v)
            if lu != lv:
                leader_list[lv] = lu
            
        path_index = [-1 for _ in range(n)]
        path = []

        def dfs(u):
            vlist = adjacent_map[u]
            print(f"path={path} path_index={path_index}")

            for v in vlist:
                if visited[v] == UNVISITED:
                    visited[v] = PROGRESS
                    path.append(v)
                    path_index[v] = len(path)-1
                    dfs(v)
                    path.pop()
                    path_index[v] = -1
                else:
                    # are we sure v is in current path?
                    if visited[v] == PROGRESS:
                        # find a partial SCC loop back from u to v
                        print(f"              partial SCC from {u} to {v}")

                        k = len(path) - 1
                        while k >= 0:
                            x = path[k]
                            root_x = get_leader(x)
                            
                            # If the root of x is the same as the root of v, we've closed the loop!
                            if root_x == get_leader(v):
                                print(f"                    x={x} root_x {root_x} == get_leader(v)")
                                break 
                                
                            # Otherwise, union them and jump!
                            union(root_x, v)
                            print(f"                    union root x={root_x} v={v} get_leader(x)={get_leader(x)}")
                            
                            # TELEPORT: move k instantly past all nodes in root_x's component
                            k = path_index[root_x] - 1
                            print(f"                    jump k to {k}")


            visited[u] = VISITED

        for v in range(n):
            if visited[v] == UNVISITED:
                visited[v] = PROGRESS
                path_index[v] = 0
                path.append(v)
                dfs(v)
                path.pop()
                path_index[v] = -1

        scc_map = {}
        for x in range(n):
            scc_map.setdefault(get_leader(x), []).append(x)

        return list(scc_map.values())

if __name__ == "__main__":
    obj = SCC()
    V = 5
    #  [1, 3], [1, 4], [2, 1], [3, 2], [4, 5]
    edges = [
        [0, 2], [0, 3], [1, 0], [2, 1], [3, 4]
    ]
    ans = obj.findSCC(V, edges)
    print(f"graph={edges}")
    print(f"{ans}\n\n") 
    # [[0, 1, 2], [3], [4]]

    n = 4
    edges2 = [
        [0,1], [1,2], [2,0], [1,3], [3,1]
    ]
    ans = obj.findSCC(n, edges2)
    print(f"graph={edges2}")
    print(f"{ans}\n\n") 

    n = 9
    edges3 = [ [i, i+1] for i in range(8) ]
    edges3.append([6,3])
    edges3.append([8,0])
    ans = obj.findSCC(n, edges3)
    print(f"graph={edges3}")
    print(f"{ans}\n\n") 

    
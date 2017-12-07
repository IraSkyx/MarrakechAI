# UnionFind.py

# Copyright pas complètement clair, (18/09/2017)
# Pas de licence claire non plus

# original at https://gist.github.com/AntiGameZ/67124a149d4c1d41e20ee82ba2cfdbe7
# Union-find data structure. Based on Josiah Carlson's code,
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
# with significant additional changes by D. Eppstein.

# Just add the comments for the 2 lines using list comprehension
# and a simple test

class UnionFind(object):
    """Union-find data structure.
    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:
    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.
    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.
    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root
        
    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self.parents)

    def union(self, objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects] 
        # for people who hates python list comprehension, the above line is equivalent to:
        # roots = []
        # for x in objects:
        #    roots.append(self[x])
            
        heaviest = max([(self.weights[r],r) for r in roots])[1]
        # for people who hates python list comprehension, the above line is equivalent to:
        # heaviest = 0
        # heaviest_weight = 0
        # for r in roots:
        #     if self.weights[r] >= heaviest_weight:
        #         heaviest_weight = self.weights[r]
        #         heaviest = r

        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest

if __name__ == "__main__":

    uf = UnionFind()
    maxi = 15
    # insert int from 0 to maxi-1
    for i in range(maxi):
        uf[i]

    print(uf.parents)
    print(uf.weights)

    import random
    #random.seed(0)
    # union numbers at random
    for i in range(8):
        r1 = random.randint(0, maxi-1)
        r2 = random.randint(0, maxi-1)
        print("union(%d, %d)"%(r1, r2))
        uf.union(r1, r2)

    print(uf.parents)
    print(uf.weights)

    # build the partition
    partition={}
    for (k, v) in uf.parents.items():
        if v in partition:
            partition[v].append(k)
        else:
            partition[v] = [k]
        
    print(partition.values())

    

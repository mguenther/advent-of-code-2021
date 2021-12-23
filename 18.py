class Node(object):

    def __init__(self):
        self.parent = None
        self.value = None
        self.left = None
        self.right = None


    def __str__(self):
        if isinstance(self.value, int):
            return str(self.value)
        else:
            return f"[{str(self.left)}, {str(self.right)}]"


    def __add__(self, other_node):
        assert self.parent is None
        root = Node()
        root.left = self
        root.left.parent = root
        root.right = other_node
        root.right.parent = root
        root.reduce()
        return root


    def is_leaf_node(self):
        return not(self.value == None)


    def is_intermediate_node(self):
        return not self.is_leaf_node() and self.left != None and self.right != None


    def magnitude(self):
        if isinstance(self.value, int):
            return self.value
        else:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()
    

    def reduce(self):


        def children_are_leafs(node):
            assert node.is_intermediate_node()
            return node.left != None and node.left.is_leaf_node() and node.right != None and node.right.is_leaf_node()


        def must_explode(node, depth):
            return depth >= 4 and node.is_intermediate_node() and children_are_leafs(node)


        def find_left(node):
            previous = node.left
            node = node
            while node != None and (node.left == previous or node.left == None):
                previous = node
                node = node.parent
            if node != None:
                node = node.left
                while node.is_intermediate_node():
                    if node.right != None:
                        node = node.right
                    else:
                        node = node.left
            return node


        def find_right(node):
            previous = node.right
            node = node
            while node != None and (node.right == previous or node.right == None):
                previous = node
                node = node.parent
            if node != None:
                node = node.right
                while node.is_intermediate_node():
                    if node.left != None:
                        node = node.left
                    else:
                        node = node.right
            return node


        def explode():
            S = [(self, 0)]
            while len(S) > 0:
                node, depth = S.pop()
                if must_explode(node, depth):
                    left_node = find_left(node)
                    if left_node != None:
                        left_node.value += node.left.value
                    right_node = find_right(node)
                    if right_node != None:
                        right_node.value += node.right.value
                    node.value = 0
                    node.left = None
                    node.right = None
                    # we have to evaluate reductions anew once we have
                    # performed an explosion
                    self.reduce()
                # if the current node is an intermediate node, then we have to process
                # all of its children as well
                if node.is_intermediate_node():
                    S.append((node.right, depth + 1))
                    S.append((node.left, depth + 1))

        
        def split():
            S = [self]
            while len(S) > 0:
                node = S.pop()
                if node.value != None:
                    assert node.left == None and node.right == None
                    if node.value >= 10:
                        nv = node.value // 2
                        node.left = Node()
                        node.left.value = nv
                        node.right = Node()
                        node.right.value = node.value - nv
                        node.left.parent = node
                        node.right.parent = node
                        node.value = None
                        # we have to evaluate reductions anew once we have
                        # performed a split
                        self.reduce()
                if node.is_intermediate_node():
                    S.append(node.right)
                    S.append(node.left)


        # a reduction operation is either an explosion or a split.
        # we look for explosions first, then go for splits.
        explode()
        split()


def parse(snailfish):

    def is_leaf_node(snailfish):
        return isinstance(snailfish, int)


    node = Node()

    if is_leaf_node(snailfish):
        # either we are at a leaf node
        node.value = snailfish
        return node
    else:
        # ... or we are at an intermediate node and have
        # to continue parsing
        l, r = snailfish
        node.left = parse(l)
        node.left.parent = node
        node.right = parse(r)
        node.right.parent = node
    
        node.reduce()

    return node


def magnitude_of_all(snailfish):
    tree = parse(snailfish[0])
    for s in snailfish[1:]:
        tree += parse(s)
    return tree.magnitude()


def highest_pairwise_magnitude(snailfish):
    highest_magnitude = 0
    for i in range(len(snailfish)):
        for j in range(len(snailfish)):
            if i == j: continue
            a, b = parse(snailfish[i]), parse(snailfish[j])
            magnitude = (a+b).magnitude()
            if magnitude > highest_magnitude:
                highest_magnitude = magnitude
    return highest_magnitude


snailfish = [eval(line.strip()) for line in open('18.in', 'r').read().strip().split("\n")]

print(magnitude_of_all(snailfish))
print(highest_pairwise_magnitude(snailfish))
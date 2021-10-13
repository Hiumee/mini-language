# a. unique for identifiers and constants (create one instance of  ST)

class TreeNode:
    def __init__(self, value, leftNode = None, rightNode = None):
        self.value = value
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.position = 0


class BinaryTree:
    def __init__(self, compareFn):
        self.root = None
        self.compareFn = compareFn
        self.position = 0

    def add_node(self, value):
        node = TreeNode(value)

        currentNode = self.root

        if self.root is None:
            self.position += 1
            node.position = self.position
            self.root = node
            return node.position

        while True:
            direction = self.compareFn(node.value, currentNode.value)

            if direction == -1:
                if currentNode.leftNode is None:
                    self.position += 1
                    node.position = self.position
                    currentNode.leftNode = node
                    return node.position

                currentNode = currentNode.leftNode
            elif direction == 1:
                if currentNode.rightNode is None:
                    self.position += 1
                    node.position = self.position
                    currentNode.rightNode = node
                    return node.position

                currentNode = currentNode.rightNode
            else:
                return currentNode.position

    def find_node(self, value):
        currentNode = self.root

        while currentNode is not None:
            direction = self.compareFn(value, currentNode.value)
            if direction == -1:
                currentNode = currentNode.leftNode
            elif direction == 1:
                currentNode = currentNode.rightNode
            else:
                return currentNode.position

        return -1

def compare(value1, value2):
    if value1 < value2:
        return -1

    if value1 > value2:
        return 1

    return 0

class SymbolTable:
    def __init__(self, compare=compare):
        self.tree = BinaryTree(compare)

    def get_position(self, token):
        return self.tree.find_node(token)

    def add_token(self, token):
        return self.tree.add_node(token)

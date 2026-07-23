"""A plain (unbalanced) Binary Search Tree, keyed on distance.

Average case is O(log n) for search/insert/delete, but with no balancing
this degrades to O(n) if data comes in sorted order (the tree becomes a
linked list). Compare with avl.py, which fixes this.
"""


class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.values = [value]  # list, so we can handle duplicate keys
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def insert(self, key, value):
        self._size += 1
        if self.root is None:
            self.root = BSTNode(key, value)
            return
        node = self.root
        while True:
            if key == node.key:
                node.values.append(value)
                return
            elif key < node.key:
                if node.left is None:
                    node.left = BSTNode(key, value)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = BSTNode(key, value)
                    return
                node = node.right

    def search(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return node.values
            node = node.left if key < node.key else node.right
        return None

    def delete(self, key):
        self.root, deleted = self._delete(self.root, key)
        if deleted:
            self._size -= 1
        return deleted

    def _delete(self, node, key):
        if node is None:
            return None, False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = self._delete(node.right, key)
            return node, deleted

        # found it - if more than one value at this key, just pop one
        if len(node.values) > 1:
            node.values.pop()
            return node, True

        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        # two children: swap in the in-order successor
        succ_parent = node
        succ = node.right
        while succ.left is not None:
            succ_parent = succ
            succ = succ.left
        node.key, node.values = succ.key, succ.values
        if succ_parent.left is succ:
            succ_parent.left = succ.right
        else:
            succ_parent.right = succ.right
        return node, True

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, acc):
        if node is None:
            return
        self._inorder(node.left, acc)
        for v in node.values:
            acc.append((node.key, v))
        self._inorder(node.right, acc)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

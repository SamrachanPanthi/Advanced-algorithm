
class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.values = [value]
        self.left = None
        self.right = None
        self.height = 1


def _h(node):
    return node.height if node else 0


def _update_height(node):
    node.height = 1 + max(_h(node.left), _h(node.right))


def _balance_factor(node):
    return _h(node.left) - _h(node.right) if node else 0


def _rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    _update_height(y)
    _update_height(x)
    return x


def _rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    _update_height(x)
    _update_height(y)
    return y


def _rebalance(node):
    _update_height(node)
    bf = _balance_factor(node)
    if bf > 1:
        if _balance_factor(node.left) < 0:
            node.left = _rotate_left(node.left)   # left-right case
        return _rotate_right(node)
    if bf < -1:
        if _balance_factor(node.right) > 0:
            node.right = _rotate_right(node.right)  # right-left case
        return _rotate_left(node)
    return node


class AVLTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def insert(self, key, value):
        self.root, added = self._insert(self.root, key, value)
        if added:
            self._size += 1

    def _insert(self, node, key, value):
        if node is None:
            return AVLNode(key, value), True
        if key == node.key:
            node.values.append(value)
            return node, True
        if key < node.key:
            node.left, added = self._insert(node.left, key, value)
        else:
            node.right, added = self._insert(node.right, key, value)
        return _rebalance(node), added

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
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            if len(node.values) > 1:
                node.values.pop()
                return node, True
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            succ = node.right
            while succ.left is not None:
                succ = succ.left
            node.key, node.values = succ.key, list(succ.values)
            node.right, _ = self._delete(node.right, succ.key)
            deleted = True
        if node is None:
            return None, deleted
        return _rebalance(node), deleted

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
        return _h(self.root) - 1 if self.root else -1

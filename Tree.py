from typing import Union, List
import math
from queue import Queue


class Node:
    def __init__(self, value: Union[int, float]):
        self.value = value
        self.left: Union[Node, None] = None
        self.right: Union[Node, None] = None


class BinarySearchTree:
    def __init__(self):
        self.root: Union[None, Node] = None

    def insert(self, value: Union[int, float]):
        self.root = self._insert(self.root, value)
        return self

    def _insert(self, curr: Node, value: Union[int, float]) -> Node:
        if curr is None:
            return Node(value)

        if value < curr.value:
            curr.left = self._insert(curr.left, value)
        else:
            curr.right = self._insert(curr.right, value)

        return curr

    def find(self, value: Union[int, float]) -> bool:
        return self._find(self.root, value)

    def _find(self, node, value: Union[int, float]) -> bool:
        if node is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._find(node.left, value)
        return self._find(node.right, value)

    def delete(self, value: Union[int, float]) -> None:
        if not self.find(value):
            print("Value not found")
            return
        self._delete(self.root, value)

    # Make the right child as the
    def _delete(self, node: Node, value: Union[int, float]):

        if node is None:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Current node is the node to be deleted

            # Case 1: No children
            if node.left is None and node.right is None:
                return None

            # Case 2.1: (One) Right child
            elif node.left is None:
                return node.right

            # Case 2.2: (One) Left child
            elif node.right is None:
                return node.left

            # Case 3: Two children
            else:
                # Find the min value in the right subtree
                min_right = self.find_min(node.right)
                node.value = min_right

                # Delete the min value in the right subtree
                node.right = self._delete(node.right, min_right)
        return node

    def find_min(self, node: Node) -> Union[int, float]:
        if node.left is None:
            return node.value
        return self.find_min(node.left)

    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Node) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def inorder(self):
        vals = []
        return self._inorder(self.root, vals)

    def _inorder(self, node: Node, vals: List[int]):
        if node is None:
            return

        if node.left:
            self._inorder(node.left, vals)

        vals.append(node.value)

        if node.right:
            self._inorder(node.right, vals)

        return vals

    def preorder(self):
        vals = []
        return self._preorder(self.root, vals)

    def _preorder(self, node: Node, vals: List[int]):
        if node is None:
            return

        vals.append(node.value)

        if node.left:
            self._preorder(node.left, vals)

        if node.right:
            self._preorder(node.right, vals)

        return vals

    def postorder(self):
        vals = []
        return self._postorder(self.root, vals)

    def _postorder(self, node: Node, vals: List[int]):
        if node is None:
            return

        if node.left:
            self._postorder(node.left, vals)

        if node.right:
            self._postorder(node.right, vals)

        vals.append(node.value)

        return vals

    def level_order(self):
        vals = []
        queue = Queue()
        queue.put(self.root)

        while not queue.empty():
            node = queue.get()
            if node is None:
                continue
            vals.append(node.value)
            queue.put(node.left)
            queue.put(node.right)

        return vals


class AVLTree:
    def __init__(self):
        self.root: Union[None, Node] = None

    def get_balance(self, node: Node):
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _balance(self, node: Node) -> Node:
        balance_factor = self.get_balance(node)

        # Left Left Case
        if balance_factor > 1 and self.get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Left Right Case
        if balance_factor > 1 and self.get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Right Case
        if balance_factor < -1 and self.get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Right Left Case
        if balance_factor < -1 and self.get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, value: Union[int, float]):
        self.root = self._insert(self.root, value)
        return self

    def _insert(self, curr: Node, value: Union[int, float]) -> Node:
        if curr is None:
            return Node(value)

        if value < curr.value:
            curr.left = self._insert(curr.left, value)
        else:
            curr.right = self._insert(curr.right, value)

        return self._balance(curr)

    def _rotate_left(self, node: Node) -> Node:
        new_node = node.right
        node.right = new_node.left
        new_node.left = node
        return new_node

    def _rotate_right(self, node: Node) -> Node:
        new_node = node.left
        node.left = new_node.right
        new_node.right = node
        return new_node

    def find(self, value: Union[int, float]) -> bool:
        return self._find(self.root, value)

    def _find(self, node, value: Union[int, float]) -> bool:
        if node is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._find(node.left, value)
        return self._find(node.right, value)

    def delete(self, value: Union[int, float]) -> None:
        if not self.find(value):
            print("Value not found")
            return
        self.root = self._delete(self.root, value)

    def _delete(self, node: Node, value: Union[int, float]):

        if node is None:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Current node is the node to be deleted

            # Case 1: No children
            if node.left is None and node.right is None:
                return None

            # Case 2.1: (One) Right child
            elif node.left is None:
                return node.right

            # Case 2.2: (One) Left child
            elif node.right is None:
                return node.left

            # Case 3: Two children
            else:
                # Find the min value in the right subtree
                min_right = self.find_min(node.right)
                node.value = min_right

                # Delete the min value in the right subtree
                node.right = self._delete(node.right, min_right)

        return self._balance(node)

    def find_min(self, node: Node) -> Union[int, float]:
        if node.left is None:
            return node.value
        return self.find_min(node.left)

    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Node) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def inorder(self):
        vals = []
        return self._inorder(self.root, vals)

    def _inorder(self, node: Node, vals: List[int]):
        if node is None:
            return

        if node.left:
            self._inorder(node.left, vals)

        vals.append(node.value)

        if node.right:
            self._inorder(node.right, vals)

        return vals

    def preorder(self):
        vals = []
        return self._preorder(self.root, vals)

    def _preorder(self, node: Node, vals: List[int]):
        if node is None:
            return

        vals.append(node.value)

        if node.left:
            self._preorder(node.left, vals)

        if node.right:
            self._preorder(node.right, vals)

        return vals

    def postorder(self):
        vals = []
        return self._postorder(self.root, vals)

    def _postorder(self, node: Node, vals: List[int]):
        if node is None:
            return

        if node.left:
            self._postorder(node.left, vals)

        if node.right:
            self._postorder(node.right, vals)

        vals.append(node.value)

        return vals

    def level_order(self):
        vals = []
        queue = Queue()
        queue.put(self.root)

        while not queue.empty():
            node = queue.get()
            if node is None:
                continue
            vals.append(node.value)
            queue.put(node.left)
            queue.put(node.right)

        return vals

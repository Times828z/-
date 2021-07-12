class tree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def __init__(self,root):
        self.size = 0
        self.root = root

    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True

        return contains_rec(self.root)

    def add(self, val):
        assert (val not in self)

        def add_rec(node):
            if not node:
                return tree.Node(val)
            elif val < node.val:
                return tree.Node(node.val, left=add_rec(node.left), right=node.right)
            else:
                return tree.Node(node.val, left=node.left, right=add_rec(node.right))

        self.root = add_rec(self.root)
        self.size += 1

    def __delitem__(self, val):
        assert (val in self)

        def delitem_rec(node):
            if val < node.val:
                node.left = delitem_rec(node.left)
                return node
            elif val > node.val:
                node.right = delitem_rec(node.right)
                return node
            else:
                if not node.left and not node.right:
                    return None
                elif node.left and not node.right:
                    return node.left
                elif node.right and not node.left:
                    return node.right
                else:
                    # remove the largest value from the left subtree as a replacement
                    # for the root value of this tree
                    t = node.left  # refers to the candidate for removal
                    if not t.right:
                        node.val = t.val
                        node.left = t.left
                    else:
                        n = t
                        while n.right.right:
                            n = n.right
                        t = n.right
                        n.right = t.left
                        node.val = t.val
                    return node

        self.root = delitem_rec(self.root)
        self.size -= 1

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)

        return iter_rec(self.root)

    def __len__(self):
        return self.size

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n, level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height - 1:
                    nodes.extend([(None, level + 1), (None, level + 1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width // 2 ** level)
            elif n:
                if n.left or level < height - 1:
                    nodes.append((n.left, level + 1))
                if n.right or level < height - 1:
                    nodes.append((n.right, level + 1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width // 2 ** level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""

        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1 + height_rec(t.left), 1 + height_rec(t.right))

        return height_rec(self.root)


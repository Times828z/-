from proposition import *
from Stack1 import *
from tree import *
from FindTruth import *


def check_delimiters(expr):
    s = Stack()
    d = {'(': 1, ')': 1, '{': 2, '}': 2, '[': 3, ']': 3, '<': 4, '>': 4}
    for c in expr:
        if c in '{([<':
            s.push(c)
        elif c in '})]>':
            try:
                a = s.pop()
                if d[a] != d[c]:
                    return False
            except:
                return False
    return s.empty()


prec = {'*': 2, '/': 2,
        '+': 1, '-': 1}


def infix_to_postfix(expr):
    """Returns the postfix form of the infix expression found in `expr`"""
    var = {'~': 2, '|': 1, '&': 1}
    ops = Stack()

    postfix = []
    for s in expr:
        if type(s) is proposition:
            postfix.append(s)
        else:
            if ops.empty() or ops.peek() == '(':
                ops.push(s)

            elif s == '(':
                ops.push(s)

            elif s == ')':
                while ops.peek() != '(':
                    postfix.append(ops.pop())
                ops.pop()

            else:
                flag = False
                while not flag:
                    if ops.peek() is None:
                        ops.push(s)
                        break;

                    if ops.peek() == '(':
                        ops.push(s)
                        break;

                    if var[s] > var[ops.peek()]:
                        ops.push(s)
                        flag = True

                    elif var[s] == var[ops.peek()]:
                        postfix.append(ops.pop())
                        ops.push(s)
                        flag = True

                    elif var[s] < var[ops.peek()]:
                        postfix.append(ops.pop())

    while not ops.empty():
        postfix.append(ops.pop())

    return postfix


# print(s)
# print(c | (a & b))

def buildTree(lst):
    treeNodeStack = Stack()
    for i in lst:
        if type(i) is proposition:
            node = tree.Node(i)
            treeNodeStack.push(node)
        elif type(i) is str and i == "~":
            p = treeNodeStack.pop()
            node = tree.Node(i, left=p)
            treeNodeStack.push(node)
        elif type(i) is str and (i == "&" or i == "|"):
            p1 = treeNodeStack.pop()
            p2 = treeNodeStack.pop()
            node = tree.Node(i, left=p1, right=p2)
            treeNodeStack.push(node)

    root = treeNodeStack.pop()
    return root


def postorder(node):
    if not node:
        return None
    postorder(node.left)
    postorder(node.right)
    if type(node.val) is proposition:
        node.val = node.val.val
    if node.val == "~":
        if type(node.left.val) is proposition:
            node.val = not node.left.val.val
        else:
            node.val = not node.left.val
    if node.val == "&":
        node.val = (node.left.val & node.right.val)
    if node.val == "|":
        node.val = (node.left.val | node.right.val)

    return node.val


def printP(lstP):
    str1 = ""
    for i in lstP:
        if type(i) is proposition:
            str1 += i.name
        else:
            str1 += i

    return str1


def printTrueValueTable(lstOfP):
    totalStr = printP(lstOfP)
    A = FindTruth(totalStr)


# 封装好的方法
def all(lst):
    str11 = printP(lst)
    print(str11)
    lstS = infix_to_postfix(lst)
    trees = buildTree(lstS)
    print(postorder(trees))
    printTrueValueTable(str11)


a = proposition("a", False)
b = proposition("b", True)
c = proposition("c", False)
lst = ["(", "~", a, "&", b, "&", a, ")", "|", c]
all(lst)

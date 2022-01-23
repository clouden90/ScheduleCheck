#!/usr/bin/env python3
"""
schedule-conflict library
"""


def conflicts_check1(data_):
    conflicts = []
    # schedules get sorted by end time
    data_.sort(key=lambda x: x[1])
    for i, p1 in enumerate(data_):
        for j in range(i+1, len(data_)):
            p2 = data_[j]
            # if start of second meeting is before end of first meeting
            if p1[1] > p2[0]:
                conflicts.append((p1, p2))
            else:
                break
    return conflicts


def conflicts_check2(data_):
    n = len(data_)
    conflicts = []
    # Create an empty Interval Search Tree,
    # add first appointment
    root = None
    root = insert(root, data_[0])

    # Process rest of the intervals
    for i in range(1, n):

        # If current appointment conflicts
        # with any of the existing intervals,
        # append the pair
        p2 = overlapsearch(root, data_[i])

        if (p2 is not None):
            conflicts.append((data_[i], p2))

        # Insert this appointment
        root = insert(root, data_[i])
    return conflicts


class ITNode:
    def __init__(self):
        self.max = None
        self.i = None
        self.left = None
        self.right = None


def newNode(j):
    temp = ITNode()
    temp.i = j
    temp.max = j[1]
    return temp


def overlap(i1, i2):
    if (i1[0] < i2[1] and i2[0] < i1[1]):
        return True
    return False


def overlapsearch(root, i):
    # Base Case, tree is empty
    if (root is None):
        return None
    # If given interval overlaps with root
    if (overlap(root.i, i)):
        return root.i
    # If left child of root is present and
    # max of left child is greater than or
    # equal to given interval, then it may
    # overlap with a left subtree interval
    if (root.left is not None and root.left.max >= i[0]):
        return overlapsearch(root.left, i)
    # Else interval can only overlap
    # with right subtree
    return overlapsearch(root.right, i)


def insert(node, data_):
    # If the tree is empty, return a new node
    root = node

    if (node is None):
        return newNode(data_)
    # If key is smaller than root's key, go to left
    # subtree and set successor as current node
    if (data_[0] < node.i[0]):
        root.left = insert(node.left, data_)
    # Go to right subtree
    else:
        root.right = insert(node.right, data_)
    if root.max < data_[1]:
        root.max = data_[1]
    return root

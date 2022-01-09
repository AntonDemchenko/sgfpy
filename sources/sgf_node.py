from .ordered_multi_dict import OrderedMultiDict


class SgfNode:
    def __init__(self, parent=None):
        self.parent = None
        self.first_child = None
        self.last_child = None
        self.prev_sibling = None
        self.next_sibling = None
        self.properties = OrderedMultiDict()
        self.attach_to(parent)

    def attach_to(self, node):
        self.detach()
        if node:
            node.attach_child(self)
    
    def detach(self):
        if self.parent:
            self.parent.detach_child(self)

    def attach_child(self, child):
        if not self.last_child:
            self.first_child = child
            self.last_child = child
        else:
            self.last_child.next_sibling = child
            child.prev_sibling = self.last_child
            self.last_child = child
        child.parent = self

    def detach_child(self, child):
        if child.prev_sibling:
            child.prev_sibling.next_sibling = child.next_sibling
        if child.next_sibling:
            child.next_sibling.prev_sibling = child.prev_sibling
        if child == self.first_child:
            self.first_child = child.next_sibling
        if child == self.last_child:
            self.last_child = child.prev_sibling
        child.parent = None
        child.prev_sibling = None
        child.next_sibling = None

    def children(self):
        child = self.first_child
        while child is not None:
            yield child
            child = child.next_sibling

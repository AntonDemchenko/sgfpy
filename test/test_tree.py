import unittest

from PySgf.SgfNode import SgfNode


class TreeTest(unittest.TestCase):
    def test_new_node(self):
        node = SgfNode()
        self.assertIsNone(node.parent)
        self.assertIsNone(node.first_child)
        self.assertIsNone(node.last_child)
        self.assertIsNone(node.prev_sibling)
        self.assertIsNone(node.next_sibling)
    
    def test_parent_and_child(self):
        parent = SgfNode()
        child = SgfNode(parent)

        self.assertEqual(child.parent, parent)
        self.assertEqual(parent.first_child, child)
        self.assertEqual(parent.last_child, child)

    def test_parent_and_two_children(self):
        parent = SgfNode()
        child1 = SgfNode(parent)
        child2 = SgfNode(parent)

        self.assertEqual(parent.first_child, child1)
        self.assertEqual(parent.last_child, child2)
        self.assertEqual(child1.next_sibling, child2)
        self.assertEqual(child2.prev_sibling, child1)

    def test_detach(self):
        parent = SgfNode()
        child1 = SgfNode(parent)
        child2 = SgfNode(parent)
        child3 = SgfNode(parent)

        child2.detach()
        self.assertEqual(child1.next_sibling, child3)
        self.assertEqual(child3.prev_sibling, child1)
        self.assertIsNone(child2.parent)
        self.assertIsNone(child2.prev_sibling)
        self.assertIsNone(child2.next_sibling)

    def test_detach_first_child(self):
        parent = SgfNode()
        child1 = SgfNode(parent)
        child2 = SgfNode(parent)

        child1.detach()
        self.assertEqual(parent.first_child, child2)
        self.assertEqual(parent.last_child, child2)
        self.assertIsNone(child2.prev_sibling)

    def test_detach_last_child(self):
        parent = SgfNode()
        child1 = SgfNode(parent)
        child2 = SgfNode(parent)

        child2.detach()
        self.assertEqual(parent.first_child, child1)
        self.assertEqual(parent.last_child, child1)
        self.assertIsNone(child1.next_sibling)

    def test_reattach(self):
        parent1 = SgfNode()
        parent2 = SgfNode()
        child = SgfNode(parent1)

        child.attach_to(parent2)
        self.assertEqual(child.parent, parent2)
        self.assertIsNone(parent1.first_child)
        self.assertIsNone(parent1.last_child)
        self.assertEqual(parent2.first_child, child)
        self.assertEqual(parent2.last_child, child)

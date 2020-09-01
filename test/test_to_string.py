import unittest

from PySgf.SgfNode import SgfNode
from PySgf.SgfTree import SgfTree


class ToStringTest(unittest.TestCase):
    def test_minimal_tree(self):
        tree = SgfTree()
        self.assertEqual(
            tree.to_string(),
            '(;)'
        )

    def test_root_properties(self):
        tree = SgfTree()
        for name, value in [['GM', '1'], ['SZ', '19']]:
            tree.root.properties.add(name, value)
        self.assertEqual(
            tree.to_string(),
            '(;GM[1]SZ[19])'
        )

    def test_main_branch(self):
        tree = SgfTree()
        tree.root.properties.add('GM', '1')
        node = SgfNode(tree.root)
        node.properties.add('B', 'qq')
        self.assertEqual(
            tree.to_string(),
            '(;GM[1]' + '\n'
            ';B[qq])'
        )

    def test_branching(self):
        tree = SgfTree()
        tree.root.properties.add('GM', '1')
        node = SgfNode(tree.root)
        node.properties.add('B', 'qq')
        node = SgfNode(tree.root)
        node.properties.add('B', 'dd')
        self.assertEqual(
            tree.to_string(),
            '(;GM[1]' + '\n'
            '(;B[qq])' + '\n'
            '(;B[dd]))'
        )

    def test_value_with_spaces(self):
        tree = SgfTree()
        tree.root.properties.add('C', 'T\ne\ts t')
        self.assertEqual(
            tree.to_string(),
            '(;C[T' + '\n'
            'e\ts t])'
        )

    def test_value_with_bracket(self):
        tree = SgfTree()
        tree.root.properties.add('C', '[]a\\')  # Value is []a\
        self.assertEqual(
            tree.to_string(),
            r'(;C[\[\]a\\])'
        )

    def test_empty_value(self):
        tree = SgfTree()
        tree.root.properties.add('C', '')
        self.assertEqual(
            tree.to_string(),
            '(;C[])'
        )

    def test_multivalue(self):
        tree = SgfTree()
        tree.root.properties.add('AB', 'dd')
        tree.root.properties.add('AB', 'qq')
        self.assertEqual(
            tree.to_string(),
            '(;AB[dd][qq])'
        )
import unittest

from sources.sgf_node import SgfNode
from sources.sgf_writer import SgfWriter


class WritingTest(unittest.TestCase):
    def test_minimal_tree(self):
        writer = SgfWriter()
        node = SgfNode()
        self.assertEqual(
            writer.write(node),
            '(;)'
        )

    def test_root_properties(self):
        writer = SgfWriter()
        node = SgfNode()
        for name, value in [['GM', '1'], ['SZ', '19']]:
            node.properties.add(name, value)
        self.assertEqual(
            writer.write(node),
            '(;GM[1]SZ[19])'
        )

    def test_main_branch(self):
        writer = SgfWriter()
        node = SgfNode()
        node.properties.add('GM', '1')
        child = SgfNode(node)
        child.properties.add('B', 'qq')
        self.assertEqual(
            writer.write(node),
            '(;GM[1]' + '\n'
            ';B[qq])'
        )

    def test_branching(self):
        writer = SgfWriter()
        node = SgfNode()
        node.properties.add('GM', '1')
        child = SgfNode(node)
        child.properties.add('B', 'qq')
        child = SgfNode(node)
        child.properties.add('B', 'dd')
        self.assertEqual(
            writer.write(node),
            '(;GM[1]' + '\n'
            '(;B[qq])' + '\n'
            '(;B[dd]))'
        )

    def test_value_with_spaces(self):
        writer = SgfWriter()
        node = SgfNode()
        node.properties.add('C', 'T\ne\ts t')
        self.assertEqual(
            writer.write(node),
            '(;C[T' + '\n'
            'e\ts t])'
        )

    def test_value_with_bracket(self):
        writer = SgfWriter()
        node = SgfNode()
        node.properties.add('C', '[]a\\')  # Value is []a\
        self.assertEqual(
            writer.write(node),
            r'(;C[\[\]a\\])'
        )

    def test_empty_value(self):
        writer = SgfWriter()
        node = SgfNode()
        node.properties.add('C', '')
        self.assertEqual(
            writer.write(node),
            '(;C[])'
        )

    def test_multivalue(self):
        writer = SgfWriter()
        node = SgfNode()
        node.properties.add('AB', 'dd')
        node.properties.add('AB', 'qq')
        self.assertEqual(
            writer.write(node),
            '(;AB[dd][qq])'
        )

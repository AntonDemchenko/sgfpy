import unittest

from sources.ordered_multi_dict import OrderedMultiDict
from sources.sgf_reader import SgfReader


class SgfWalker:
    def __init__(self):
        self.size = 0

    def get_size(self, root):
        self.size = 0
        if root:
            self.go(root)
        return self.size

    def go(self, node):
        self.size += 1
        if node.first_child:
            self.go(node.first_child)
        if node.next_sibling:
            self.go(node.next_sibling)


def parse(sgf):
    reader = SgfReader()
    root = reader.read(sgf)
    return root


class ReadingTest(unittest.TestCase):
    def test_minimal_sgf(self):
        sgf = r'(;)'
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 1)
        self.assertEqual(root.properties, OrderedMultiDict())

    def test_root(self):
        sgf = r'(;GM[1]FF[4]CA[UTF-8]AP[Sabaki:0.51.1]KM[6.5]SZ[19]DT[2020-06-30])'
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 1)
        self.assertEqual(
            root.properties,
            OrderedMultiDict(
                ['GM', '1'],
                ['FF', '4'],
                ['CA', 'UTF-8'],
                ['AP', 'Sabaki:0.51.1'],
                ['KM', '6.5'],
                ['SZ', '19'],
                ['DT', '2020-06-30']
            )
        )

    def test_branching(self):
        sgf = r'(;GM[1](;B[dp])(;B[dq]))'
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 3)
        expected = OrderedMultiDict()
        expected.add('GM', '1')
        self.assertEqual(root.properties, expected)
        expected.clear()
        expected.add('B', 'dp')
        self.assertEqual(root.first_child.properties, expected)
        expected.clear()
        expected.add('B', 'dq')
        self.assertEqual(root.last_child.properties, expected)

    def test_value_with_spaces(self):
        sgf = r"""(;C[Multiline
commentary with spaces])"""
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 1)
        expected = OrderedMultiDict(['C', r"""Multiline
commentary with spaces"""])
        self.assertEqual(root.properties, expected)

    def test_value_with_bracket(self):
        sgf = r'(;C[\[\]\a\\])'  # Input: \[\]\a\\]
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 1)
        self.assertEqual(
            root.properties,
            OrderedMultiDict(
                ['C', '[]a\\']  # Expected: []a\
            )
        )
    
    def test_value_brackets_absence(self):
        sgf = r'(;A)'
        root = parse(sgf)
        self.assertIsNone(root)

    def test_value_absence(self):
        sgf = r'(;A[])'
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 1)
        self.assertEqual(
            root.properties,
            OrderedMultiDict(['A', ''])
        )

    def test_multivalue(self):
        sgf = r'(;AB[dp][dd])'
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 1)
        self.assertEqual(
            root.properties,
            OrderedMultiDict(
                ['AB', 'dp'],
                ['AB', 'dd']
            )
        )

    def test_property_repeating(self):
        sgf = r'(;AB[dp]AB[dd])'
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 1)
        self.assertEqual(
            root.properties,
            OrderedMultiDict(
                ['AB', 'dp'],
                ['AB', 'dd']
            )
        )

    def test_multiline_sgf(self):
        sgf = r"""
            (;
                GM[1]
                FF[4]
                CA[UTF-8]
                AP[Sabaki:0.51.1]
                KM[6.5]
                SZ[19]
                DT[2020-06-30]
                (
                    ;B[dp]
                )
                (
                    ;B[dq]
                )
            )
        """
        root = parse(sgf)
        self.assertEqual(SgfWalker().get_size(root), 3)
        self.assertEqual(
            root.properties,
            OrderedMultiDict(
                ['GM', '1'],
                ['FF', '4'],
                ['CA', 'UTF-8'],
                ['AP', 'Sabaki:0.51.1'],
                ['KM', '6.5'],
                ['SZ', '19'],
                ['DT', '2020-06-30']
            )
        )
        self.assertEqual(
            root.first_child.properties,
            OrderedMultiDict(
                ['B', 'dp']
            )
        )
        self.assertEqual(
            root.last_child.properties,
            OrderedMultiDict(
                ['B', 'dq']
            )
        )

    def test_no_closing_parenthesis(self):
        sgf = r'(;'
        root = parse(sgf)
        self.assertIsNone(root)

    def test_no_nodes(self):
        sgf = r'()'
        root = parse(sgf)
        self.assertIsNone(root)

    def test_no_opening_parenthesis(self):
        sgf = r';)'
        root = parse(sgf)
        self.assertIsNone(root)

    def test_no_property_name(self):
        sgf = r';[value]'
        root = parse(sgf)
        self.assertIsNone(root)

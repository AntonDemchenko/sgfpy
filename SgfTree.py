from .SgfNode import SgfNode


class State:
    FINISH = 0
    EXPECT_BRANCH_START = 1
    EXPECT_BRANCH_FINISH = 2
    EXPECT_NODE_START = 4
    EXPECT_PROPERTY_NAME = 8
    EXPECT_PROPERTY_VALUE_START = 16
    EXPECT_PROPERTY_VALUE = 32
    EXPECT_PROPERTY_VALUE_FINISH = 64


def quote(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('[', '\[')
    s = s.replace(']', '\]')
    return s


def make_string_from(node):
    has_sibling = node.prev_sibling or node.next_sibling
    s = ''
    if has_sibling:
        s += '('
    s += ';'
    prev_name = None
    for name, value in node.properties.items():
        value = quote(value)
        if name != prev_name:
            s += '{}[{}]'.format(name, value)
            prev_name = name
        else:
            s += '[{}]'.format(value)
    if node.first_child:
        s += '\n' + make_string_from(node.first_child)
    if has_sibling:
        s += ')'
    if node.next_sibling:
        s += '\n' + make_string_from(node.next_sibling)
    return s


class SgfTree:
    def __init__(self, root=None):
        self.root = root if root else SgfNode()

    @classmethod
    def from_string(cls, s):
        root = None
        current_node = None
        property_name = ''
        property_value = ''
        stack = []
        brace_balance = 0
        state = State.EXPECT_BRANCH_START
        escape = False

        for c in s:
            if (state & State.EXPECT_BRANCH_START) and c == '(':
                stack.append(current_node)
                brace_balance -= 1
                state = State.EXPECT_NODE_START
            elif (state & State.EXPECT_BRANCH_FINISH) and c == ')':
                current_node = stack.pop()
                brace_balance += 1
                state = (State.FINISH if brace_balance == 0
                    else State.EXPECT_BRANCH_START | State.EXPECT_BRANCH_FINISH)
            elif (state & State.EXPECT_NODE_START) and c == ';':
                current_node = SgfNode(current_node)
                if not root:
                    root = current_node
                state = (State.EXPECT_PROPERTY_NAME |
                    State.EXPECT_NODE_START |
                    State.EXPECT_BRANCH_START |
                    State.EXPECT_BRANCH_FINISH)
            elif (state & State.EXPECT_PROPERTY_NAME) and 'A' <= c <= 'Z':
                is_property_name_start = state & State.EXPECT_NODE_START
                if is_property_name_start:
                    property_name = ''
                property_name += c
                state = State.EXPECT_PROPERTY_NAME | State.EXPECT_PROPERTY_VALUE_START
            elif (state & State.EXPECT_PROPERTY_VALUE_START) and c == '[':
                state = State.EXPECT_PROPERTY_VALUE | State.EXPECT_PROPERTY_VALUE_FINISH
            elif (state & State.EXPECT_PROPERTY_VALUE) and (c != ']' or escape):
                if not escape and c == '\\':
                    escape = True
                else:
                    property_value += c
                    escape = False
            elif (state & State.EXPECT_PROPERTY_VALUE_FINISH) and c == ']':
                current_node.properties.add(property_name, property_value)
                property_value = ''
                state = (State.EXPECT_PROPERTY_NAME |
                    State.EXPECT_PROPERTY_VALUE_START |
                    State.EXPECT_BRANCH_START |
                    State.EXPECT_BRANCH_FINISH |
                    State.EXPECT_NODE_START)
            elif not c.isspace():
                break

        return cls(root) if state == State.FINISH else None

    def to_string(self):
        return '(' + make_string_from(self.root) + ')'

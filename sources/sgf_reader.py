from .sgf_node import SgfNode


class State:
    FINISH = 0
    EXPECT_BRANCH_START = 1
    EXPECT_BRANCH_FINISH = 2
    EXPECT_NODE_START = 4
    EXPECT_PROPERTY_NAME = 8
    EXPECT_PROPERTY_VALUE_START = 16
    EXPECT_PROPERTY_VALUE = 32
    EXPECT_PROPERTY_VALUE_FINISH = 64


class SgfReader:
    def __init__(self):
        self.__root = None
        self.__node = None
        self.__property_name = ''
        self.__property_value = ''
        self.__stack = []
        self.__brace_balance = 0
        self.__state = State.EXPECT_BRANCH_START
        self.__escape = False

    def read(self, string):
        self.__init__()
        for symbol in string:
            if self.__is_branch_start(symbol):
                self.__start_branch()
            elif self.__is_branch_finish(symbol):
                self.__finish_branch()
            elif self.__is_node_start(symbol):
                self.__start_node()
            elif self.__is_property_name(symbol):
                self.__add_to_property_name(symbol)
            elif self.__is_property_value_start(symbol):
                self.__start_property_value()
            elif self.__is_property_value(symbol):
                self.__add_to_property_value(symbol)
            elif self.__is_property_value_finish(symbol):
                self.__finish_property_value()
            elif not symbol.isspace():
                break
        return self.__root if self.__state == State.FINISH else None

    def __is_branch_start(self, symbol):
        return (self.__state & State.EXPECT_BRANCH_START) and symbol == '('

    def __start_branch(self):
        self.__stack.append(self.__node)
        self.__brace_balance -= 1
        self.__state = State.EXPECT_NODE_START

    def __is_branch_finish(self, symbol):
        return (self.__state & State.EXPECT_BRANCH_FINISH) and symbol == ')'

    def __finish_branch(self):
        self.__node = self.__stack.pop()
        self.__brace_balance += 1
        self.__state = (State.FINISH if self.__brace_balance == 0
            else State.EXPECT_BRANCH_START | State.EXPECT_BRANCH_FINISH)

    def __is_node_start(self, symbol):
        return (self.__state & State.EXPECT_NODE_START) and symbol == ';'

    def __start_node(self):
        self.__node = SgfNode(self.__node)
        if not self.__root:
            self.__root = self.__node
        self.__state = (State.EXPECT_PROPERTY_NAME |
            State.EXPECT_NODE_START |
            State.EXPECT_BRANCH_START |
            State.EXPECT_BRANCH_FINISH)

    def __is_property_name(self, symbol):
        return (self.__state & State.EXPECT_PROPERTY_NAME) and 'A' <= symbol <= 'Z'

    def __add_to_property_name(self, symbol):
        is_property_name_start = self.__state & State.EXPECT_NODE_START
        if is_property_name_start:
            self.__property_name = ''
        self.__property_name += symbol
        self.__state = State.EXPECT_PROPERTY_NAME | State.EXPECT_PROPERTY_VALUE_START

    def __is_property_value_start(self, symbol):
        return (self.__state & State.EXPECT_PROPERTY_VALUE_START) and symbol == '['

    def __start_property_value(self):
        self.__state = State.EXPECT_PROPERTY_VALUE | State.EXPECT_PROPERTY_VALUE_FINISH

    def __is_property_value(self, symbol):
        return (self.__state & State.EXPECT_PROPERTY_VALUE) and (symbol != ']' or self.__escape)

    def __add_to_property_value(self, symbol):
        if not self.__escape and symbol == '\\':
            self.__escape = True
        else:
            self.__property_value += symbol
            self.__escape = False

    def __is_property_value_finish(self, symbol):
        return (self.__state & State.EXPECT_PROPERTY_VALUE_FINISH) and symbol == ']'

    def __finish_property_value(self):
        self.__node.properties.add(self.__property_name, self.__property_value)
        self.__property_value = ''
        self.__state = (State.EXPECT_PROPERTY_NAME |
            State.EXPECT_PROPERTY_VALUE_START |
            State.EXPECT_BRANCH_START |
            State.EXPECT_BRANCH_FINISH |
            State.EXPECT_NODE_START)

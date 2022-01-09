class SgfWriter:
    def write(self, node):
        return '(' + self.__write_node(node) + ')'

    def __write_node(self, node):
        has_sibling = node.prev_sibling or node.next_sibling
        s = ''
        if has_sibling:
            s += '('
        s += ';'
        prev_name = None
        for name, value in node.properties.items():
            value = self.__quote(value)
            if name != prev_name:
                s += '{}[{}]'.format(name, value)
                prev_name = name
            else:
                s += '[{}]'.format(value)
        if node.first_child:
            s += '\n' + self.__write_node(node.first_child)
        if has_sibling:
            s += ')'
        if node.next_sibling:
            s += '\n' + self.__write_node(node.next_sibling)
        return s

    @staticmethod
    def __quote(s):
        s = s.replace('\\', '\\\\')
        s = s.replace('[', '\[')
        s = s.replace(']', '\]')
        return s

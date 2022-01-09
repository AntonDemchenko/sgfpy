# sgfpy
## Library for reading and writing SGF (Smart Go Format) strings

Reading:
```python
with open(file_path, 'r') as f:
	sgf = f.read()
	reader = SgfReader()
	root = reader.read(sgf)
```

Writing:
```python
with open(file_path, 'w') as f:
	writer = SgfWriter()
	sgf = writer.write(root)
	print(sgf, file=f)
```

Property getting and setting:
```python
gm_prop_value = root.properties.value_of('GM')  # Get value of property GM
ab_prop_values = root.properties.values_of('AB')  # Get list of values of property AB
root.properties.add(prop_key, prop_value)  # Add property
root.properties.erase(prop_key)  # Erase property
```

Tree building:
```python
    root = SgfNode()
    child = SgfNode(root)  # create node and attach it to root
    node = SgfNode()
    node.attach_to(root)  # attach node to root
    child.detach()  # detach node from root
```

Tree traversal:
```python
    node = SgfNode()
    node.parent  # parent of node
    node.children()  # node's children
    node.first_child  # first child of node
    node.last_child  # last child of node
    node.prev_sibling  # left sibling of node in parent's children list
    node.next_sibling  # right sibling of node in parent's children list
```
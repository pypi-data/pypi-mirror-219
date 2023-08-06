# Tree Structure

Tree Structure is a module that implements some common trees in data structure.

## Quick Start

There are two basic components in each type of tree structure: **Node** and **Tree**.  
Each node has two basic attributes: **order** and **value**.  
Order is the key to construct the tree structure. Default order is current timestamp.  
Value can be anything you want to store. Default value is None.

``` python
>>> import treestructure
>>> node = treestructure.BinaryNode(35, 'Stevie Wonder') # Create node
>>> node.order
35
>>> node.value
'Stevie Wonder'
```

Insert node into tree to build the tree structure.  
Use package() to check the tree structure.
It's better using package() with [pprint](https://docs.python.org/3/library/pprint.html) module.

``` python
>>> import pprint
>>> tree = treestructure.BinarySearchTree(node) # Create tree
>>> tree.insertNode(treestructure.BinaryNode(45, 'Ray Charles')) # Insert node
>>> tree.insertNode(treestructure.BinaryNode(25, 'Lionel Richie')) # Insert node
>>> pprint.pprint(tree.package(), sort_dicts=False) # Display tree
{'order': 35,
 'value': 'Stevie Wonder',
 'leftChildNode': {'order': 25,
                   'value': 'Lionel Richie',
                   'leftChildNode': None,
                   'rightChildNode': None},
 'rightChildNode': {'order': 45,
                    'value': 'Ray Charles',
                    'leftChildNode': None,
                    'rightChildNode': None}}
```

Delete node by specific order.

``` python
>>> delNode = tree.deleteNode(35) # Delete node
>>> pprint.pprint(delNode.package(), sort_dicts=False) # Display node
{'order': 35,
 'value': 'Stevie Wonder',
 'leftChildNode': {},
 'rightChildNode': {},
 'parentNode': {}}
>>> pprint.pprint(tree.package(), sort_dicts=False) # Display tree
{'order': 25,
 'value': 'Lionel Richie',
 'leftChildNode': None,
 'rightChildNode': {'order': 45,
                    'value': 'Ray Charles',
                    'leftChildNode': None,
                    'rightChildNode': None}}
```

## Contents

- [Binary Search Tree](https://github.com/Musicmathstudio/treeStructure/blob/main/doc/bst.md)
- [Binary Heap](https://github.com/Musicmathstudio/treeStructure/blob/main/doc/heap.md)

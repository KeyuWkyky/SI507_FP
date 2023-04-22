#!/usr/bin/env python
# coding: utf-8
# %%

# %%


import json


# %%


def save_tree_to_file(tree, filename):
    json_string = json.dumps(tree)
    with open(filename, 'w') as f:
        f.write(json_string)

def read_tree_from_file(filename):
    with open(filename, 'r') as f:
        tree = json.load(f)
    return tree


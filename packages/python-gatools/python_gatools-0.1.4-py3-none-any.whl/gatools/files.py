import os
import pathlib

__ALL__ = ["Tree", "fTree", "removeIfExists"]


class Tree(type(pathlib.Path())):
    def mkdir(self, parents=True, exist_ok=True):
        super().mkdir(parents=parents, exist_ok=exist_ok)


class fTree(Tree):
    def __new__(cls, *args, **kwargs):
        args = list(args)
        if (x := pathlib.Path(args[0])).is_file():
            args[0] = x.parent
        return super().__new__(cls, *args, **kwargs)

def removeIfExists(fname: str):
    """Remove `fname` if it exists"""
    if os.path.exists(fname):
        os.remove(fname)
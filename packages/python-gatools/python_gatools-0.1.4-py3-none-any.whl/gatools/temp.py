import logging
import os
import random
import shutil
import string
import tempfile

from gatools.files import Tree, removeIfExists


def rand(k=8):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=k))


def tmp_():
    return Tree(tempfile.gettempdir())


class TmpDir:
    def __init__(self, root=tempfile.gettempdir(), k=8):
        self.root = Tree(root)
        self.k = k

    def find_new(self):
        new_name = self.root / rand(k=self.k)
        if os.path.isdir(new_name):
            return self.find_new()
        else:
            return Tree(new_name)

    def __enter__(self):
        self.root = self.find_new()
        os.makedirs(self.root)
        return self.root

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.root.absolute())
        log.debug(f"Deleting {self.root.absolute()}")


class TmpFile:
    def __init__(self, mode="w+", suffix=None):
        self.mode = mode
        self.suffix = suffix
        self.fname = None

    def find_new(self):
        new_name = rand()
        return self.find_new() if os.path.isfile(new_name) else new_name

    def __enter__(self):
        return self.enter()

    def enter(self):
        new_name = self.find_new()
        if self.suffix is not None:
            new_name += self.suffix
        self.fname = os.path.join(tempfile.gettempdir(), new_name)
        self.f = open(self.fname, mode=self.mode)
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

    def exit(self):
        self.f.close()
        removeIfExists(self.fname)


log = logging.getLogger(__name__)

import logging
from collections import defaultdict

from munch import munchify


def analyse(d):
    # Analyse a list of dict
    r = defaultdict(list)
    for x in d:
        for k, v in x.items():
            r[k].append(v)
    return munchify(r)


def query(d, **kw):
    # Query a list of dict
    xkeep = []
    for x in d:
        cond = True
        for k, v in kw.items():
            if x.get(k) != v:
                cond = False
                break
        if cond:
            xkeep.append(x)
    if len(xkeep) == 1:
        return munchify(xkeep[0])
    return xkeep


log = logging.getLogger(__name__)

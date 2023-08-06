import datetime
import logging
import re

from   cxmlinvbot.errors.errors import MapActionError

logger = logging.getLogger(__name__)

FLOAT_RE = re.compile('[0-9]*\.[0-9]*')
INT_RE = re.compile('[0-9]*')
DATE_RE = re.compile('(?P<day>[0-3]?[0-9])/(?P<month>[0-1][0-9])/(?P<year>[0-9]{4})')

class MapAction(object):
    
    def __init__(self, paths=None):
        self._paths = paths if type(paths) == type(()) or type(paths) == list else [paths]

    def perform(self, key, nvPairs):
        return {}


class Default(MapAction):

    def __init__(self, paths, defVal):
        super(Default, self).__init__(paths)
        self._defVal = defVal

    def perform(self, key, nvPairs):
        m = {}
        for p in self._paths:
            tmp = nvPairs.get(key, '')
            m[p] = tmp if len(tmp) else self._defVal
        return m
            

class Ignore(MapAction):
    pass


class Lambda(MapAction):
    
    def __init__(self, paths, op, keys):
        super(Lambda, self).__init__(paths)
        self._op = op
        self._keys = keys
    
    def perform(self, _, nvPairs):
        m = {}
        for p in self._paths:

            args = []
            for k in self._keys:
                arg = nvPairs.get(k, '')
                if not len(arg):
                    raise MapActionError('Lambda field %s is missing from invoice CSV.' % k)
                if FLOAT_RE.fullmatch(arg):
                    arg = float(arg)
                elif INT_RE.fullmatch(arg):
                    arg = int(arg)
                elif DATE_RE.fullmatch(arg):
                    arg = datetime.datetime.strptime(arg, '%d/%m/%Y')
                args.append(arg)
            m[p] = str(self._op(*args))
        return m 


class Required(MapAction):
    
    def perform(self, key, nvPairs):
        m = {}
        for p in self._paths:
            m[p] = nvPairs.get(key, '')
            if not len(m[p]):
                raise MapActionError('Required field %s is missing from invoice CSV.' % key)

        return m 


class TBD(MapAction):
    pass



#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from .wanneng import WannengSearcher
from .aidian import AiDianSearcher
from .cx import CxSearcher
from .enncy import EnncySearcher
from .heibook import HeibookSearcher
from .every import EverySearcher


searchers = [EverySearcher, EnncySearcher, WannengSearcher, AiDianSearcher, HeibookSearcher, CxSearcher]
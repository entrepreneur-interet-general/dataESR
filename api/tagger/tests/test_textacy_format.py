import unittest
from tagger.app import TextacyFormatting
from operator import itemgetter
import numpy as np

class TestTextacyFormatting(unittest.TestCase):
    params = {
            'text': '"The next important step might be the derivation of the Dirac equation. The Creutz model  [32] suggests that we should consider incorporating into the logical inference treatment, the additional knowledge that one has objects hopping on a lattice instead of particles moving in a space-time continuum. Recall that up to Section  2.4, the description of the measurement scenario, robustness etc. is explicitly discrete. In Section  2.4, the continuum limit was taken only because our aim was to derive the Pauli equation, which is formulated in continuum space-time. Of course, the description of the motion of the particle in Section  2.6 is entirely within a continuum description but there is no fundamental obstacle to replace this treatment by a proper treatment of objects hopping on a lattice. Therefore it seems plausible that the logical inference approach can be extended to describe massless spin-1/2 particles moving in continuum space-time by considering the continuum limit of the corresponding lattice model. An in-depth, general treatment of this problem is beyond the scope of the present paper and we therefore leave this interesting problem for future research.'
            }

    def test_initialization(self):
        tc = TextacyFormatting(self.__class__.params)
        assert tc

    def test_sgrank_defaults(self):
        tc = TextacyFormatting(self.__class__.params, lang=u'en')
        keywords = tc.get_keyterms()
        assert set(map(itemgetter(0), keywords)) == set(['massless spin-1/2 particle',
                                                         'logical inference treatment',
                                                         'logical inference approach',
                                                         'continuum limit',
                                                         'continuum space',
                                                         'pauli equation',
                                                         'creutz model',
                                                         'fundamental obstacle',
                                                         'continuum description',
                                                         'proper treatment'])

    def test_sgrank(self):
        self.__class__.params['method'] = 'sgrank'
        tc = TextacyFormatting(self.__class__.params, lang=u'en')
        keywords = tc.get_keyterms()
        assert set(map(itemgetter(0), keywords)) == set(['massless spin-1/2 particle',
                                                         'logical inference treatment',
                                                         'logical inference approach',
                                                         'continuum limit',
                                                         'continuum space',
                                                         'pauli equation',
                                                         'creutz model',
                                                         'fundamental obstacle',
                                                         'continuum description',
                                                         'proper treatment'])

    def test_textrank(self):
        self.__class__.params['method'] = 'textrank'
        tc = TextacyFormatting(self.__class__.params, lang=u'en')
        keywords = tc.get_keyterms()
        assert set(zip(*keywords)[0]) == set(['treatment',
                                            'continuum',
                                            'description',
                                            'particle',
                                            'problem',
                                            'lattice',
                                            'equation',
                                            'model',
                                            'section',
                                            'inference'])
    
    def test_singlerank(self):
        self.__class__.params['method'] = 'singlerank'
        tc = TextacyFormatting(self.__class__.params, lang=u'en')
        keywords = tc.get_keyterms()
        assert set(zip(*keywords)[0]) == set(['time continuum',
                                            'continuum space',
                                            'continuum description',
                                            'continuum limit',
                                            'inference treatment',
                                            'treatment',
                                            'lattice',
                                            'particle',
                                            'time',
                                            'space'])
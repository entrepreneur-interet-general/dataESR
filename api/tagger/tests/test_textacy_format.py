import unittest
from src.app import TextacyFormatting
from operator import itemgetter

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
        assert keywords == [('treatment', 0.055888797213371644),
                            ('continuum', 0.04564028843856736),
                            ('description', 0.04147435059411628),
                            ('particle', 0.040285831640575774),
                            ('problem', 0.03652277091122243),
                            ('lattice', 0.03556310973780484),
                            ('equation', 0.0317939413740572),
                            ('model', 0.030691218910060165),
                            ('section', 0.027874555001248403),
                            ('inference', 0.024670228221595807)]
    
    def test_singlerank(self):
        self.__class__.params['method'] = 'singlerank'
        tc = TextacyFormatting(self.__class__.params, lang=u'en')
        keywords = tc.get_keyterms()
        assert keywords == [('time continuum', 0.12075620099061243),
                            ('continuum space', 0.12072300449666701),
                            ('continuum description', 0.11948703463619625),
                            ('continuum limit', 0.10895909838974659),
                            ('inference treatment', 0.0902938037965455),
                            ('treatment', 0.05962939589508113),
                            ('lattice', 0.044481858270253354),
                            ('particle', 0.042016100170522444),
                            ('time', 0.04191528319387767),
                            ('space', 0.04188208669993223)]
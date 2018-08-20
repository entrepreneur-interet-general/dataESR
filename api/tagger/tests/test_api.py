from flask import json
from src.app import app
import unittest


class TestTextacyResponse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_doc_textacy(self):
        params = {
                'text': 'The next important step might be the derivation of \
                        the Dirac equation. The Creutz model  [32] suggests \
                        that we should consider incorporating into the logical \
                        inference treatment, the additional knowledge that one \
                        has objects hopping on a lattice instead of particles \
                        moving in a space-time continuum. Recall that up to Section \
                        2.4, the description of the measurement scenario, robustness \
                        etc. is explicitly discrete. In Section  2.4, the continuum \
                        limit was taken only because our aim was to derive the Pauli \
                        equation, which is formulated in continuum space-time. Of \
                        course, the description of the motion of the particle in \
                        Section 2.6 is entirely within a continuum description but \
                        there is no fundamental obstacle to replace this treatment \
                        by a proper treatment of objects hopping on a lattice. \
                        Therefore it seems plausible that the logical inference \
                        approach can be extended to describe massless spin-1/2 \
                        particles moving in continuum space-time by considering \
                        the continuum limit of the corresponding lattice model. \
                        An in-depth, general treatment of this problem is beyond \
                        the scope of the present paper and we therefore leave this \
                        interesting problem for future research.'
                }
        response = self.client.post('/keywords', data=params, content_type='application/json')
        response_json = json.loads(response.data.decode('utf8'))

        assert response_json['keywords'] == [(u'massless spin-1/2 particle',
                                    0.15387941999481636),
                                   (u'logical inference treatment',
                                    0.11715332737705884),
                                   (u'logical inference approach',
                                    0.09136901016959438),
                                   (u'continuum limit',
                                    0.08033973111784386),
                                   (u'continuum space',
                                    0.06630463582851502),
                                   (u'pauli equation',
                                    0.03132777999751102),
                                   (u'creutz model',
                                    0.026581337388402043),
                                   (u'fundamental obstacle',
                                    0.02639697723912133),
                                   (u'continuum description',
                                    0.026300408365873586),
                                   (u'proper treatment',
                                    0.025135452800462643)]


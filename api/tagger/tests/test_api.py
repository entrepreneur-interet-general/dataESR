from flask import jsonify, json
from src.app import app
import unittest
from operator import itemgetter


class TestTextacyResponse(unittest.TestCase):

    def test_doc_textacy(self):
        with app.test_client() as client:  
            params = {
                'text': 'The next important step might be the derivation of the Dirac equation. The Creutz model  [32] suggests that we should consider incorporating into the logical inference treatment, the additional knowledge that one has objects hopping on a lattice instead of particles moving in a space-time continuum. Recall that up to Section  2.4, the description of the measurement scenario, robustness etc. is explicitly discrete. In Section  2.4, the continuum limit was taken only because our aim was to derive the Pauli equation, which is formulated in continuum space-time. Of course, the description of the motion of the particle in Section  2.6 is entirely within a continuum description but there is no fundamental obstacle to replace this treatment by a proper treatment of objects hopping on a lattice. Therefore it seems plausible that the logical inference approach can be extended to describe massless spin-1/2 particles moving in continuum space-time by considering the continuum limit of the corresponding lattice model. An in-depth, general treatment of this problem is beyond the scope of the present paper and we therefore leave this interesting problem for future research.',
                }
            response = client.post('/keywords', data=json.dumps(params), content_type='application/json')
            response_json = json.loads(response.data)
            assert response.status_code == 200
            assert set(map(itemgetter(0), response_json['keywords'])) == set(['massless spin-1/2 particle',
                                                            'logical inference treatment',
                                                            'logical inference approach',
                                                            'continuum limit',
                                                            'continuum space',
                                                            'pauli equation',
                                                            'creutz model',
                                                            'fundamental obstacle',
                                                            'continuum description',
                                                            'proper treatment'])


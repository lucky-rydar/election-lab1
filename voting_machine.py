from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

class VotingMachine:

    def define_voters(self, voter_public_keys):
        pass

    def register_candidate(self, candidate):
        pass

    def vote(self, candidate, signature):
        pass

    def voted_list(self) -> list:
        pass
    
    def voting_results(self) -> list:
        pass


class KeyGiver():
    def __init__(self):
        self._registered_pb_keys = []
        
        pass

    def emit_keys(passport):
        # must 
        pass

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii
import regex as re

class VotingMachine:

    def __init__(self):
        self._voters = []
        self._candidates = []
        
        self._voted_list = []
        self._voting_results = []
        self.gamma_key = "tsvk_vybori_2023_golosyite_za_jakubovicha"

        # TSVK keys
        _key_pair = RSA.generate(2048)
        self.pub_key = _key_pair.publickey().export_key("PEM")
        self.__priv_key = _key_pair.exportKey("PEM")

    def define_voters(self, voter_pub_keys):
        for pub_key in voter_pub_keys:
            self.define_voter(pub_key)

    def define_voter(self, pub_key):
        if pub_key not in self._voters:
            self._voters.append(pub_key)

    def register_candidate(self, candidate):
        for c in self._candidates:
            if c == candidate:
                return False
        self._candidates.append(candidate)

    def form_bulletin(self, voter_pub_key):
        if voter_pub_key not in self._voters or voter_pub_key is None:
            return None
        return self._candidates

    def vote(self, candidate, voter_pub_key):
        if candidate not in self._candidates:
            return "Candidate you voted is not registered"
        if voter_pub_key in self._voted_list:
            return "You have already voted"

        self._voted_list.append(voter_pub_key)
        self._voting_results.append(candidate)
        return "You have successfully voted"

    def get_voting_results(self, result, signature, voter_pub_key):
        # check if voter have a right to vote, if not voted yet
        result_tsvk = self.decrypt(result, self.__priv_key)
        if self.verify(result_tsvk, signature, voter_pub_key):
            result_final = self._xor_encrypt_decrypt(result_tsvk, self.gamma_key)
            candidate, date = result_final.split("|")
            if candidate in self._candidates:
                voting_status = self.vote(candidate, voter_pub_key)
                return voting_status
        else:
            return "Voting results are not verified"

    def _xor_encrypt_decrypt(self, text, key):
        if isinstance(text, bytes):
            text = text.decode("utf-8")
        result = ""
        for i in range(len(text)):
            result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
        return result

    def decrypt(self, message, key):
        if not isinstance(key, RSA.RsaKey):
            key = RSA.import_key(key)
        chipher = PKCS1_OAEP.new(key)
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        decrypted_message = chipher.decrypt(message)
        return decrypted_message

    def verify(self, message, signature, key):
        if not isinstance(key, RSA.RsaKey):
            key = RSA.import_key(key)
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        h = SHA256.new(message)
        try:
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    def count_results(self):
        candidates = {}
        for candidate in self._voting_results:
            if candidate in candidates:
                candidates[candidate] += 1
            else:
                candidates[candidate] = 1

        return candidates


    def voted_list(self) -> list:
        return self._voted_list
    
    def voting_results(self) -> list:
        return self._voting_results


APPROVED_VOTERS_FILE = "approved_voters.txt"

class KeyGiver():
    def __init__(self):
        self._registered_keys = []
        pass

    def register(self, passport):
        file = open(APPROVED_VOTERS_FILE, "r")
        for line in file:
            line = line.split()[0]
            if str(line) == str(passport):
                key_pair = RSA.generate(2048)
                self._registered_keys.append([key_pair, passport])
                return key_pair
            
    def check_if_registered(self, passport):
        for pair in self._registered_keys:
            _, _passport = pair
            if _passport == passport:
                return True
        return False

    def get_keys(self, passport):
        for pair in self._registered_keys:
            keys, _passport = pair
            if _passport == passport:
                return keys
        return None


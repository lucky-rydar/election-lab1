from voting_machine import KeyGiver, VotingMachine
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
import random


class VotingMachineClient():
    def __init__(self, name, passport, kg, vm) -> None:
        self.pub_key = None
        self.priv_key = None
        self.name = name
        self.passport = passport
        self.kg = kg
        self.vm = vm
        self.register_voter()


    def register_voter(self):
        if not self.kg.check_if_registered(self.passport):
            keys = self.kg.register(self.passport)
            if keys is None:
                print("You are not authorized to vote!")
                return
        else:
            keys = self.kg.get_keys(self.passport)
        if keys is not None:
            self.pub_key = keys.publickey().exportKey("PEM")
            self.priv_key = keys.exportKey("PEM")
            self.vm.define_voter(self.pub_key)
        

    def get_bulletin(self):
        bulletin = self.vm.form_bulletin(self.pub_key)
        return bulletin
    

    def encrypt(self, message, key):
        if not isinstance(key, RSA.RsaKey):
            key = RSA.import_key(key)
        chipher = PKCS1_OAEP.new(key)
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        signed_message = chipher.encrypt(message)
        return signed_message
    
    def sign(self, message, key):
        if not isinstance(key, RSA.RsaKey):
            key = RSA.import_key(key)
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        h = SHA256.new(message)
        signature = pkcs1_15.new(key).sign(h)
        return signature
    
    def vote(self, candidate):
        # TODO: move in voting machine
        # if candidate in self.vm.form_bulletin():
        data = candidate + "|" + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data_xor = self.vm._xor_encrypt_decrypt(data, self.vm.gamma_key)
        signature = self.sign(data_xor, self.priv_key)
        data_encrypted = self.encrypt(data_xor, self.vm.pub_key)

        # send to voting machine
        voting_status = self.vm.get_voting_results(data_encrypted, signature, self.pub_key)

        return voting_status

    
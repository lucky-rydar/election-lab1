from voting_machine import KeyGiver, VotingMachine
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
import random


vm = VotingMachine()
kg = KeyGiver()

class VotingMachineClient():
    def __init__(self, name, passport) -> None:
        self.pub_key = None
        self.priv_key = None
        self.name = name
        self.passport = passport
        self.register_voter()


    def register_voter(self):
        if not kg.check_if_registered(self.passport):
            keys = kg.register(self.passport)
            if keys is None:
                print("You are not authorized to vote!")
                return
        else:
            keys = kg.get_keys(self.passport)
        if keys is not None:
            self.pub_key = keys.publickey().exportKey("PEM")
            self.priv_key = keys.exportKey("PEM")
            vm.define_voters(self.pub_key)
        

    def get_bulletin(self):
        bulletin = vm.form_bulletin(self.pub_key)
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
        data_xor = vm._xor_encrypt_decrypt(data, vm.gamma_key)
        signature = self.sign(data_xor, self.priv_key)
        data_encrypted = self.encrypt(data_xor, vm.pub_key)

        # send to voting machine
        voting_status = vm.get_voting_results(data_encrypted, signature, self.pub_key)

        return voting_status



def imitate_voting(name, passport):
    print("Voter: ", name, passport)
    voter = VotingMachineClient(name, passport)
    candidates = voter.get_bulletin()
    if candidates is not None:
        chousen_candidate = candidates[random.randint(0, len(candidates) - 1)]
        status = voter.vote(chousen_candidate)
        print("status: ", status)

if __name__ == "__main__":
    imitate_voting('Vasya', '6472583019')
    imitate_voting('Vasya', '6472583019')
    imitate_voting('Sasha', '1111111111')
    imitate_voting('Maria', '8350179426')
    imitate_voting('Alexandr', '6857312409')
    imitate_voting('Katya', '1980750196')



    vm.count_results()
    # key = "petuh852"
    # text = "hello"
    # vt = Voter('Vasya', '6472583019')
    # vm = VotingMachine()
    # enc =vt.xor_encrypt_decrypt(text, vm.gamma_key)
    # print("enc: ", enc)
    # dec = vt.xor_encrypt_decrypt(enc, vm.gamma_key)
    # print("dec: ", dec)

    
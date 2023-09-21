import random

from voting_machine_client import VotingMachineClient
from voting_machine import KeyGiver, VotingMachine

def imitate_voting(name, passport, kg, vm):
    print("Voter: ", name, passport)
    voter = VotingMachineClient(name, passport, kg, vm)
    candidates = voter.get_bulletin()
    if candidates is not None:
        chousen_candidate = candidates[random.randint(0, len(candidates) - 1)]
        status = voter.vote(chousen_candidate)
        print("status: ", status)

if __name__ == "__main__":
    vm = VotingMachine()
    kg = KeyGiver()
    
    # add candidates
    vm.register_candidate('cand1')
    vm.register_candidate('cand2')
    vm.register_candidate('cand3')
    vm.register_candidate('cand4')

    # vote,
    imitate_voting('Vasya', '6472583019', kg, vm)
    imitate_voting('Vasya', '6472583019', kg, vm)
    imitate_voting('Sasha', '1111111111', kg, vm)
    imitate_voting('Maria', '8350179426', kg, vm)
    imitate_voting('Alexandr', '6857312409', kg, vm)
    imitate_voting('Katya', '1980750196', kg, vm)

    voting_res = vm.count_results()
    print('========================')
    print(voting_res)

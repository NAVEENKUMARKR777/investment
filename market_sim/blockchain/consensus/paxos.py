import random

class Acceptor:
    def __init__(self, id):
        self.id = id
        self.promised_id = None
        self.accepted_id = None
        self.accepted_value = None

    def receive_prepare(self, proposal_id):
        if not self.promised_id or proposal_id > self.promised_id:
            self.promised_id = proposal_id
            return True, self.accepted_id, self.accepted_value
        return False, None, None

    def receive_accept_request(self, proposal_id, value):
        if not self.promised_id or proposal_id >= self.promised_id:
            self.promised_id = proposal_id
            self.accepted_id = proposal_id
            self.accepted_value = value
            return True
        return False

class Proposer:
    last_proposal_id = 0  # shared across all proposers

    def __init__(self, id, value):
        self.id = id
        Proposer.last_proposal_id += 1
        self.proposal_id = Proposer.last_proposal_id
        self.value = value

    def run_paxos(self, acceptors):
        # Phase 1: Prepare
        promises = []
        for acc in acceptors:
            ok, acc_id, acc_val = acc.receive_prepare(self.proposal_id)
            if ok:
                promises.append((acc_id, acc_val))

        if len(promises) <= len(acceptors) // 2:
            return False, "Not enough promises"

        # Use the value with highest accepted_id if available
        accepted_values = [(aid, val) for aid, val in promises if aid is not None and val is not None]
        if accepted_values:
            # Choose the value with the highest accepted_id
            self.value = sorted(accepted_values, key=lambda x: x[0], reverse=True)[0][1]

        # Phase 2: Accept
        accepted = 0
        for acc in acceptors:
            if acc.receive_accept_request(self.proposal_id, self.value):
                accepted += 1

        if accepted > len(acceptors) // 2:
            return True, self.value
        return False, "Not enough acceptances"

class Learner:
    def __init__(self):
        self.learned_value = None

    def learn(self, value):
        self.learned_value = value

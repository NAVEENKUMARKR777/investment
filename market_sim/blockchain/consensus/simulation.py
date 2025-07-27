from paxos import Proposer, Acceptor, Learner
import random
import time

def run_simulation(num_acceptors=5, num_proposers=2, retries=3):
    # Create acceptors and learners
    acceptors = [Acceptor(i) for i in range(num_acceptors)]
    learners = [Learner() for _ in range(num_proposers)]

    # Create proposers with random values
    proposer_values = [f"Value_{random.randint(1, 100)}" for _ in range(num_proposers)]
    proposers = [Proposer(i, val) for i, val in enumerate(proposer_values)]

    print("📊 Paxos Simulation Started")
    print("=" * 40)

    for i, proposer in enumerate(proposers):
        print(f"\nProposer {proposer.id} proposing: {proposer.value}")
        for attempt in range(retries):
            success, result = proposer.run_paxos(acceptors)
            if success:
                learners[i].learn(result)
                print(f"✅ Consensus achieved with value: {learners[i].learned_value}")
                break
            else:
                print(f"⚠️ Attempt {attempt+1} failed: {result}")
                proposer.proposal_id += 1  # try with higher ID
        else:
            print(f"❌ Consensus failed after {retries} attempts")

    # Show learner outcomes
    print("\n🧠 Learned values:")
    for i, learner in enumerate(learners):
        print(f"  Learner {i}: {learner.learned_value}")

    # Show acceptor states
    print("\n📬 Acceptor States:")
    for acc in acceptors:
        print(f"  Acceptor {acc.id} accepted: ({acc.accepted_id}, {acc.accepted_value})")

if __name__ == "__main__":
    run_simulation()

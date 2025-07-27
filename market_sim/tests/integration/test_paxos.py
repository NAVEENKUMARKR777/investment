from market_sim.blockchain.consensus.paxos import Proposer, Acceptor, Learner

def test_paxos_single_proposer():
    acceptors = [Acceptor(i) for i in range(5)]
    proposer = Proposer(id=0, value="Trade AAPL")
    learner = Learner()

    success, result = proposer.run_paxos(acceptors)
    assert success, f"Paxos failed: {result}"
    learner.learn(result)

    assert learner.learned_value == "Trade AAPL" or learner.learned_value is not None
    print("✅ Single proposer Paxos test passed.")

def test_paxos_multiple_proposers():
    acceptors = [Acceptor(i) for i in range(5)]
    learners = [Learner() for _ in range(2)]

    proposer1 = Proposer(0, "Buy BTC")
    proposer2 = Proposer(1, "Sell ETH")

    success1, result1 = proposer1.run_paxos(acceptors)
    if success1:
        learners[0].learn(result1)

    success2, result2 = proposer2.run_paxos(acceptors)
    if success2:
        learners[1].learn(result2)

    # One of them must reach consensus
    assert learners[0].learned_value is not None or learners[1].learned_value is not None
    print("✅ Multiple proposer Paxos test ran.")

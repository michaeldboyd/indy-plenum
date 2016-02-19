from zeno.common.util import getMaxFailures
from zeno.test.cli.helper import isNameToken


def checkNodeStatusToken(node, msgs):

    assert "Name: {}".format(node.name) in msgs[0]['msg']
    assert "Node listener: {}:{}".format(node.nodestack.ha[0],
                                         node.nodestack.ha[1]) in msgs[1]['msg']
    assert "Client listener: {}:{}".format(node.clientstack.ha[0],
                                           node.clientstack.ha[1]) in msgs[2]['msg']
    assert "Status:" in msgs[3]['msg']
    assert "Connections:" in msgs[4]['msg']
    assert not msgs[4]['newline']
    assert msgs[5]['msg'] == '<none>'
    assert "Replicas: 2".format() in msgs[6]['msg']
    assert "Up time (seconds)" in msgs[7]['msg']
    assert "Clients: " in msgs[8]['msg']
    assert not msgs[8]['newline']


def checkForNamedTokens(printedTokens, expectedNames):
    # Looking for the expected names in given tokens

    lookingForNames = set(expectedNames)

    for printedToken in printedTokens['tokens']:
        assert isNameToken(printedToken[0])
        assert printedToken[1] in lookingForNames
        # Remove the name if token for that name is found
        lookingForNames.remove(printedToken[1])

    assert len(lookingForNames) == 0


def testStatusAtCliStart(cli):
    """
    Testing `status` command at the start of cli when no nodes or clients
    are created
    """
    cli.enterCmd("status")
    printeds = cli.printeds
    nodeStatus = printeds[3]
    clientStatus = printeds[2]
    assert nodeStatus['msg'] == "No nodes are running. Try typing " \
                                "'new node <name>'."
    assert clientStatus['msg'] == "Clients: No clients are running. Try " \
                                  "typing 'new client <name>'."


def testStatusAfterOneNodeCreated(cli, validNodeNames):
    """
    Testing `status` and `status node <nodeName>` command after one node is
    created
    """
    nodeName = validNodeNames[0]
    cli.enterCmd("new node {}".format(nodeName))
    # Let the node start up
    cli.looper.runFor(3)

    cli.enterCmd("status")
    startedNodeToken = cli.printedTokens[1]
    printeds = cli.printeds
    clientStatus = printeds[2]
    checkForNamedTokens(startedNodeToken, (nodeName,))
    assert clientStatus['msg'] == "Clients: No clients are running. Try " \
                                  "typing " \
                                  "'new client <name>'."

    cli.enterCmd("status node {}".format(nodeName))
    msgs = list(reversed(cli.printeds[:10]))
    node = cli.nodes[nodeName]
    assert "Name: {}".format(node.name) in msgs[0]['msg']
    assert "Node listener: {}:{}".format(node.nodestack.ha[0],
                                         node.nodestack.ha[1]) in msgs[1]['msg']
    assert "Client listener: {}:{}".format(node.clientstack.ha[0],
                                           node.clientstack.ha[1]) in msgs[2]['msg']
    assert "Status:" in msgs[3]['msg']
    assert "Connections:" in msgs[4]['msg']
    assert not msgs[4]['newline']
    assert msgs[5]['msg'] == '<none>'
    assert "Replicas: 2".format() in msgs[6]['msg']
    assert "Up time (seconds)" in msgs[7]['msg']
    assert "Clients: " in msgs[8]['msg']
    assert not msgs[8]['newline']


def testStatusAfterAllNodesUp(cli, validNodeNames, allNodesUp):
    # Checking the output after command `status`. Testing the pool status here
    cli.enterCmd("status")
    printeds = cli.printeds
    clientStatus = printeds[4]
    fValue = printeds[3]['msg']
    assert clientStatus['msg'] == "Clients: No clients are running. Try " \
                                  "typing " \
                                  "'new client <name>'."
    assert fValue == "f-value (number of possible faulty nodes): {}".format(
            getMaxFailures(len(validNodeNames)))

    for name in validNodeNames:
        # Checking the output after command `status node <name>`. Testing
        # the node status here
        cli.enterCmd("status node {}".format(name))
        otherNodeNames = (set(validNodeNames) - {name, })
        cli.looper.runFor(3)
        # checkNodeStatusToken(cli.nodes[name], list(reversed(cli.printeds[:10])))
        msgs = list(reversed(cli.printeds[:10]))
        node = cli.nodes[name]
        assert "Name: {}".format(node.name) in msgs[0]['msg']
        assert "Node listener: {}:{}".format(node.nodestack.ha[0],
                                             node.nodestack.ha[1]) in msgs[1]['msg']
        assert "Client listener: {}:{}".format(node.clientstack.ha[0],
                                               node.clientstack.ha[1]) in msgs[2]['msg']
        assert "Status:" in msgs[3]['msg']
        assert "Connections:" in msgs[4]['msg']
        assert not msgs[4]['newline']
        assert msgs[5]['msg'] == '<none>'
        assert "Replicas: 2".format() in msgs[5]['msg']
        assert "Up time (seconds)" in msgs[7]['msg']
        assert "Clients: " in msgs[8]['msg']
        assert not msgs[8]['newline']
        checkForNamedTokens(cli.printedTokens[1], otherNodeNames)
        if cli.clients:
            checkForNamedTokens(cli.printedTokens[1], cli.voidMsg)


def testStatusAfterClientAdded(cli, validNodeNames, allNodesUp):
    clientName = "Joe"
    cli.enterCmd("new client {}".format(clientName))
    # Let the client get connected to the nodes
    cli.looper.runFor(3)

    for name in validNodeNames:
        # Checking the output after command `status node <name>`. Testing
        # the node status here after the client is connected
        cli.enterCmd("status node {}".format(name))
        otherNodeNames = (set(validNodeNames) - {name, })
        checkNodeStatusToken(cli.nodes[name], list(reversed(cli.printeds[:10])))
        checkForNamedTokens(cli.printedTokens[3], otherNodeNames)
        if cli.clients:
            checkForNamedTokens(cli.printedTokens[1], {clientName, })

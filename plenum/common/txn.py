# TODO: Change this file name to `constants`

# inter-node communication
from enum import IntEnum

NOMINATE = "NOMINATE"
REELECTION = "REELECTION"
PRIMARY = "PRIMARY"
PRIMDEC = "PRIMARYDECIDED"

BATCH = "BATCH"

REQACK = "REQACK"

REQNACK = "REQNACK"

CLINODEREG = "CLINODEREG"

PROPAGATE = "PROPAGATE"

PREPREPARE = "PREPREPARE"
PREPARE = "PREPARE"
COMMIT = "COMMIT"
REPLY = "REPLY"

ORDERED = "ORDERED"
REQDIGEST = "REQDIGEST"

INSTANCE_CHANGE = "INSTANCE_CHANGE"

LEDGER_STATUS = "LEDGER_STATUS"
LEDGER_STATUSES = "LEDGER_STATUSES"
CONSISTENCY_PROOF = "CONSISTENCY_PROOF"
CONSISTENCY_PROOFS = "CONSISTENCY_PROOFS"
CATCHUP_REQ = "CATCHUP_REQ"
CATCHUP_REQS = "CATCHUP_REQS"
CATCHUP_REP = "CATCHUP_REP"
CATCHUP_REPS = "CATCHUP_REPS"

BLACKLIST = "BLACKLIST"

NAME = "name"
VERSION = "version"
IP = "ip"
PORT = "port"
KEYS = "keys"
TYPE = "type"
TXN_TYPE = "type"
TXN_ID = "txnId"
ORIGIN = "origin"
IDENTIFIER = "identifier"
TARGET_NYM = "dest"
DATA = "data"
RAW = "raw"
ENC = "enc"
HASH = "hash"
ALIAS = "alias"
PUBKEY = "pubkey"
VERKEY = "verkey"
NODE_IP = "node_ip"
NODE_PORT = "node_port"
CLIENT_IP = "client_ip"
CLIENT_PORT = "client_port"
NEW_NODE = "NEW_NODE"
NEW_STEWARD = "NEW_STEWARD"
NEW_CLIENT = "NEW_CLIENT"
CHANGE_HA = "CHANGE_HA"
CHANGE_KEYS = "CHANGE_KEYS"
STEWARD = "STEWARD"
CLIENT = "CLIENT"
ROLE = 'role'
NONCE = 'nonce'
ATTRIBUTES = 'attributes'
TXN_TIME = 'txnTime'
TXN_DATA = "txnData"
LAST_TXN = "lastTxn"
TXNS = "Txns"

CREDIT = "CREDIT"
AMOUNT = "AMOUNT"
GET_BAL = "GET_BAL"
GET_ALL_TXNS = "GET_ALL_TXNS"
SUCCESS = "success"
BALANCE = "balance"
ALL_TXNS = "all_txns"

BY = "by"

POOL_TXN_TYPES = {NEW_NODE, NEW_STEWARD, NEW_CLIENT, CHANGE_HA, CHANGE_KEYS}


class ClientBootStrategy(IntEnum):
    Simple = 1
    PoolTxn = 2
    Custom = 3


class StorageType(IntEnum):
    File = 1
    Ledger = 2
    OrientDB = 3

#!/usr/bin/env python
# coding: utf-8

import dataclasses

from xrpl.models.transactions import Transaction
from xrpl.wallet import Wallet


@dataclasses.dataclass
class SmartContractParams:
    wallet: Wallet
    tx: Transaction

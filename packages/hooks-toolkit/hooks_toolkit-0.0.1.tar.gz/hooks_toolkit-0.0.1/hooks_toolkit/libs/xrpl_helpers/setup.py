#!/usr/bin/env python
# coding: utf-8

import asyncio
from typing import Dict
from xrpl.clients import Client, WebsocketClient
from xrpl.wallet import Wallet
from xrpl.ledger import get_network_id

from hooks_toolkit.libs.xrpl_helpers.constants import (
    NOT_ACTIVE_WALLET,
    MASTER_ACCOUNT_WALLET,
    GW_ACCOUNT_WALLET,
    ALICE_ACCOUNT_WALLET,
    BOB_ACCOUNT_WALLET,
    CAROL_ACCOUNT_WALLET,
)
from hooks_toolkit.libs.xrpl_helpers.fund_system import fund_system
from hooks_toolkit.libs.xrpl_helpers.tools import IC


class XrplIntegrationTestContext:
    def __init__(
        self,
        client: WebsocketClient,
        notactive: Wallet,
        master: Wallet,
        gw: Wallet,
        ic: IC,
        alice: Wallet,
        bob: Wallet,
        carol: Wallet,
    ):
        self.client = client
        self.notactive = notactive
        self.master = master
        self.gw = gw
        self.ic = ic
        self.alice = alice
        self.bob = bob
        self.carol = carol


def teardown_client(context: XrplIntegrationTestContext) -> None:
    if not context or not context.client:
        return
    return context.client.close()


def setup_client(server: str) -> XrplIntegrationTestContext:
    currency = "USD"

    with WebsocketClient(server) as client:
        context = XrplIntegrationTestContext(
            client=client,
            notactive=NOT_ACTIVE_WALLET,
            master=MASTER_ACCOUNT_WALLET,
            gw=GW_ACCOUNT_WALLET,
            ic=IC.gw(currency, GW_ACCOUNT_WALLET.classic_address),
            alice=ALICE_ACCOUNT_WALLET,
            bob=BOB_ACCOUNT_WALLET,
            carol=CAROL_ACCOUNT_WALLET,
        )
        context.client.network_id = get_network_id(client)
        fund_system(context.client, context.master, context.ic)
        return context

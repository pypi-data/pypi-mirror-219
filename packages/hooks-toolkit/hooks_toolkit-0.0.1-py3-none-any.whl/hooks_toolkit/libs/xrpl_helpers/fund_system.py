#!/usr/bin/env python
# coding: utf-8

from typing import List

from xrpl.clients import Client
from xrpl.wallet import Wallet
from xrpl.models.amounts import IssuedCurrencyAmount

from hooks_toolkit.libs.xrpl_helpers.tools import (
    Account,
    ICXRP,
    balance,
    fund,
    account_set,
    limit,
    trust,
    pay,
)


def fund_system(client: Client, wallet: Wallet, ic: IssuedCurrencyAmount) -> None:
    # INIT ACCOUNTS
    gw = Account("gw")
    alice = Account("alice")
    bob = Account("bob")
    carol = Account("carol")
    # INIT IC
    USD = ic

    # FUND GW
    if balance(client, gw.wallet.classic_address) == 0:
        # Setup GW
        fund(client, wallet, ICXRP(10000), gw.wallet.classic_address)
        print(f"FUNDED: {gw.wallet.classic_address}")
        account_set(client, gw.wallet)
        print(f"SET ACCOUNT: {gw.wallet.classic_address}")

    # Check Funded
    needs_funding = []
    if balance(client, gw.wallet.classic_address) < 2000:
        needs_funding.append(gw.wallet.classic_address)
    if balance(client, alice.wallet.classic_address) < 2000:
        needs_funding.append(alice.wallet.classic_address)
    if balance(client, bob.wallet.classic_address) < 2000:
        needs_funding.append(bob.wallet.classic_address)
    if balance(client, carol.wallet.classic_address) < 2000:
        needs_funding.append(carol.wallet.classic_address)

    # Check Trustline
    needs_lines = []
    if limit(client, alice.wallet.classic_address, USD) < 20000:
        needs_lines.append(alice.wallet)
    if limit(client, bob.wallet.classic_address, USD) < 20000:
        needs_lines.append(bob.wallet)
    if limit(client, carol.wallet.classic_address, USD) < 20000:
        needs_lines.append(carol.wallet)
    # Check IC Balance
    needs_ic = []
    if balance(client, alice.wallet.classic_address, USD) < 20:
        needs_ic.append(alice.wallet.classic_address)
    if balance(client, bob.wallet.classic_address, USD) < 20:
        needs_ic.append(bob.wallet.classic_address)
    if balance(client, carol.wallet.classic_address, USD) < 20:
        needs_ic.append(carol.wallet.classic_address)

    print(f"FUNDING: {len(needs_funding)}")
    print(f"TRUSTING: {len(needs_lines)}")
    print(f"PAYING: {len(needs_ic)}")

    fund(client, wallet, ICXRP(2000), *needs_funding)
    trust(client, USD.set(100000), *needs_lines)
    pay(client, USD.set(2000), gw.wallet, *needs_ic)

    print(f"ALICE XRP: {balance(client, alice.account)}")
    print(f"ALICE TRUST: {limit(client, alice.account, USD)}")
    print(f"ALICE USD: {balance(client, alice.account, USD)}")

    print(f"BOB XRP: {balance(client, bob.account)}")
    print(f"BOB TRUST: {limit(client, bob.account, USD)}")
    print(f"BOB USD: {balance(client, bob.account, USD)}")

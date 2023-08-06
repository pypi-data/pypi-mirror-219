#!/usr/bin/env python
# coding: utf-8

from typing import Union, Dict, Any

from xrpl.clients import Client
from xrpl.wallet import Wallet
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests import AccountInfo, LedgerEntry
from xrpl.models.transactions import Payment, TrustSet, AccountSet, AccountSetFlag
from xrpl.utils import str_to_hex, xrp_to_drops
from hooks_toolkit.libs.xrpl_helpers.transaction import app_transaction

LEDGER_ACCEPT_REQUEST = {"command": "ledger_accept"}


class Account:
    def __init__(self, name: str = None, seed: str = None):
        print(name)
        self.name = name
        if name == "gw":
            self.wallet = Wallet("safmpBLsy2paxybRMpvXqFqSrV5HG", 0)
            self.account = self.wallet.classic_address
        if name == "notactivated":
            self.wallet = Wallet("snqPCkCnfAbK4p981HZZGMj8SnhZ7", 0)
            self.account = self.wallet.classic_address
        if name == "alice":
            self.wallet = Wallet("ssbTMHrmEJP7QEQjWJH3a72LQipBM", 0)
            self.account = self.wallet.classic_address
        if name == "bob":
            self.wallet = Wallet("spkcsko6Ag3RbCSVXV2FJ8Pd4Zac1", 0)
            self.account = self.wallet.classic_address
        if name == "carol":
            self.wallet = Wallet("snzb83cV8zpLPTE4nQamoLP9pbhB7", 0)
            self.account = self.wallet.classic_address
        if name == "dave":
            self.wallet = Wallet("sh2Q7wDfjdvyVaVHEE8JT3C9osGFD", 0)
            self.account = self.wallet.classic_address
        if name == "elsa":
            self.wallet = Wallet("sEdTeiqmPdUob32gyD6vPUskq1Z7TP3", 0)
            self.account = self.wallet.classic_addressff

        # raise KeyError('invalid account')


class ICXRP:
    def __init__(self, value: int):
        self.issuer = None
        self.currency = "XRP"
        self.value = value
        self.amount = xrp_to_drops(self.value)


class IC:
    def __init__(self, issuer: str, currency: str, value: int):
        self.issuer = issuer
        self.currency = currency
        self.value = value
        self.amount = IssuedCurrencyAmount(
            currency=self.currency, value=str(self.value), issuer=self.issuer
        )

    @staticmethod
    def gw(name: str, gw: str) -> "IC":
        return IC(gw, name, 0)

    def set(self, value: int):
        self.value = value
        self.amount = IssuedCurrencyAmount(
            currency=self.currency, value=str(self.value), issuer=self.issuer
        )
        return self


async def account_seq(ctx: Client, account: str) -> int:
    request = AccountInfo(account=account)
    try:
        response = await ctx.request(request)
        return response.result["account_data"]["Sequence"]
    except Exception as error:
        print(error)
        return 0


def xrp_balance(ctx: Client, account: str) -> float:
    request = AccountInfo(account=account)
    response = ctx.request(request)
    if "error" in response.result and response.result["error"] == "actNotFound":
        return 0
    return float(response.result["account_data"]["Balance"])


def ic_balance(ctx: Client, account: str, ic: IC) -> float:
    request = LedgerEntry(
        ripple_state={
            "currency": ic.currency,
            "accounts": [account, ic.issuer],
        }
    )
    response = ctx.request(request)
    if "error" in response.result:
        return 0
    node = response.result["node"]
    return abs(float(node["Balance"]["value"]))


def balance(ctx: Client, account: str, ic: Union[IC, None] = None) -> float:
    try:
        if not ic:
            return xrp_balance(ctx, account)
        return ic_balance(ctx, account, ic)
    except Exception as error:
        print(error)
        return 0


def limit(ctx: Client, account: str, ic: IC) -> float:
    try:
        request = LedgerEntry(
            ripple_state={
                "currency": ic.currency,
                "accounts": [account, ic.issuer],
            }
        )
        response = ctx.request(request)
        if "error" in response.result:
            return 0
        node = response.result["node"]
        if node["HighLimit"]["issuer"] == ic.issuer:
            return float(node["LowLimit"]["value"])
        else:
            return float(node["HighLimit"]["value"])
    except Exception as error:
        print(error)
        return 0


def fund(ctx: Client, wallet: Wallet, uicx: Union[IC, ICXRP], *accts: str) -> None:
    for acct in accts:
        try:
            built_tx = Payment(
                account=wallet.classic_address,
                destination=acct,
                amount=uicx.amount,
            )
            app_transaction(
                ctx,
                built_tx,
                wallet,
            )
        except Exception as error:
            print(error)
            # print(error.data.decoded)
            # print(error.data.tx)


def pay(ctx: Client, uicx: Union[IC, ICXRP], signer: Wallet, *accts: str) -> None:
    for acct in accts:
        try:
            built_tx = Payment(
                account=signer.classic_address,
                destination=acct,
                amount=uicx.amount,
            )
            app_transaction(
                ctx,
                built_tx,
                signer,
            )
        except Exception as error:
            print(error)


def trust(ctx: Client, uicx: Union[IC, ICXRP], *accts: Wallet) -> None:
    for acct in accts:
        try:
            built_tx = TrustSet(
                account=acct.classic_address,
                limit_amount=uicx.amount,
            )
            app_transaction(
                ctx,
                built_tx,
                acct,
            )
        except Exception as error:
            print(error)


def account_set(ctx: Client, account: Wallet) -> None:
    built_tx = AccountSet(
        account=account.classic_address,
        transfer_rate=0,
        domain=str_to_hex("https://usd.transia.io"),
        set_flag=AccountSetFlag.ASF_DEFAULT_RIPPLE,
    )
    app_transaction(
        ctx,
        built_tx,
        account,
    )


def rpc_tx(ctx: Client, account: Wallet, json: Dict[str, Any]) -> None:
    app_transaction(
        ctx,
        json,
        account,
    )


def rpc(ctx: Client, json: Dict[str, Any]) -> None:
    ctx.request(json)


def close(ctx: Client) -> None:
    ctx.request(LEDGER_ACCEPT_REQUEST)

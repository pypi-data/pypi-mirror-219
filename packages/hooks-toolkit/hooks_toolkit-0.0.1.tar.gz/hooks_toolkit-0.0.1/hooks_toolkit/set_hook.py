#!/usr/bin/env python
# coding: utf-8

from typing import List

from xrpl.clients.sync_client import SyncClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import SetHook
from xrpl.models.transactions.set_hook import Hook
from xrpl.utils import calculate_hook_on, hex_hook_parameters
from xrpl.models.transactions import SetHookFlag

# from xrpl.models import HookParameter, HookGrant
from hooks_toolkit.libs.xrpl_helpers.transaction import (
    get_transaction_fee,
    app_transaction,
)
from hooks_toolkit.utils import hex_namespace, read_hook_binary_hex_from_ns


def create_hook_payload(
    version: int = None,
    create_file: str = None,
    namespace: str = None,
    flags: List[SetHookFlag] = [],
    hook_on_array: str = None,
    hook_params: List[str] = None,
    hook_grants: List[str] = None,
) -> Hook:
    return Hook(
        hook_api_version=version,
        create_code=read_hook_binary_hex_from_ns(create_file),
        hook_namespace=hex_namespace(namespace),
        flags=flags,
        hook_on=calculate_hook_on(hook_on_array),
    )
    # if version is not None:
    #     hook.hook_api_version = version
    # if create_file is not None:
    #     hook.create_code = read_hook_binary_hex_from_ns(create_file)
    # if namespace is not None:
    #     hook.hook_namespace = hex_namespace(namespace)
    # if flags != 0:
    #     hook.flags = flags
    # if hook_on_array is not None:
    #     hook.hook_on = calculate_hook_on(hook_on_array)
    # if hook_params is not None:
    #     hook.hook_parameters = hex_hook_parameters(hook_params)
    # if hook_grants is not None:
    #     hook.hook_grants = hook_grants
    # # DA: validate
    # return hook


def set_hooks_v3(client: SyncClient, seed: str, hooks: List[Hook]):
    HOOK_ACCOUNT = Wallet(seed, 0)
    _tx = SetHook(
        account=HOOK_ACCOUNT.classic_address,
        hooks=hooks,
    )
    tx = SetHook(
        account=HOOK_ACCOUNT.classic_address,
        hooks=hooks,
        fee=get_transaction_fee(client, _tx),
    )

    print("1. Transaction to submit (before autofill):")
    print(tx.to_xrpl())
    print("\n2. Submitting transaction...")

    app_transaction(client, tx, HOOK_ACCOUNT, hard_fail=True, count=2, delay_ms=1000)

    print("\n3. SetHook Success...")

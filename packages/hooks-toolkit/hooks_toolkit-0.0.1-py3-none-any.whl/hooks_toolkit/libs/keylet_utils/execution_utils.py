#!/usr/bin/env python
# coding: utf-8

from typing import List

from xrpl.clients import WebsocketClient
from xrpl.models.transactions import Transaction
from xrpl.models.requests import Tx
from xrpl.models import TransactionMetadata
from xrpl.models.transactions.metadata import HookExecution, HookExecutionFields

from xrpl.models.transactions.metadata import CreatedNode

from xrpl.utils.str_conversions import hex_to_str


class iHookExecution:
    def __init__(self, hook_execution: HookExecutionFields):
        self.HookAccount = hook_execution["HookAccount"]
        self.HookEmitCount = hook_execution["HookEmitCount"]
        self.HookExecutionIndex = hook_execution["HookExecutionIndex"]
        self.HookHash = hook_execution["HookHash"]
        self.HookInstructionCount = hook_execution["HookInstructionCount"]
        self.HookResult = hook_execution["HookResult"]
        self.HookReturnCode = hook_execution["HookReturnCode"]
        self.HookReturnString = hex_to_str(hook_execution["HookReturnString"]).replace(
            "\x00", ""
        )
        self.HookStateChangeCount = hook_execution["HookStateChangeCount"]


class iHookExecutions:
    def __init__(self, results: List[HookExecution]):
        self.executions = [iHookExecution(entry["HookExecution"]) for entry in results]


class iHookEmittedTxs:
    def __init__(self, results):
        self.txs = results


class ExecutionUtility:
    @staticmethod
    def get_hook_executions_from_meta(
        client: WebsocketClient, meta: TransactionMetadata
    ):
        if not client.is_open():
            raise Exception("xrpl Client is not connected")

        if not meta["HookExecutions"]:
            raise Exception("No HookExecutions found")

        return iHookExecutions(meta["HookExecutions"])

    @staticmethod
    def get_hook_executions_from_tx(client: WebsocketClient, hash: str):
        if not client.is_open():
            raise Exception("xrpl Client is not connected")

        tx_response = client.request(
            {"method": "tx", "params": [{"transaction": hash}]}
        )

        hook_executions = tx_response.result.get("meta", {}).get("HookExecutions")
        if not hook_executions:
            raise Exception("No HookExecutions found")

        return iHookExecutions(hook_executions)

    @staticmethod
    def get_hook_emitted_txs_from_meta(
        client: WebsocketClient, meta: TransactionMetadata
    ):
        if not client.is_open():
            raise Exception("xrpl Client is not connected")

        affected_nodes = meta.get("AffectedNodes")
        if not affected_nodes:
            raise Exception("No `AffectedNodes` found")

        emitted_created_nodes = [
            n
            for n in affected_nodes
            if isinstance(n, CreatedNode)
            and n.CreatedNode.LedgerEntryType == "EmittedTxn"
        ]

        if not emitted_created_nodes:
            print("No `CreatedNodes` found")
            return iHookEmittedTxs([])

        return iHookEmittedTxs(
            [node.CreatedNode.NewFields.EmittedTxn for node in emitted_created_nodes]
        )

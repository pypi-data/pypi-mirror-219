from xrpl.clients import WebsocketClient
from xrpl.models.requests import LedgerEntry
from xrpl.models.requests.ledger_entry import Hook, HookDefinition, HookState

from hooks_toolkit.utils import hex_namespace


class StateUtility:
    @staticmethod
    async def get_hook(client: WebsocketClient, account: str) -> Hook:
        if not client.is_open():
            raise Exception("xrpl Client is not connected")
        hook_req = LedgerEntry(
            hook={
                "account": account,
            },
        )
        hook_res = await client.request(hook_req)
        return hook_res.result["node"]

    @staticmethod
    async def get_hook_definition(client: WebsocketClient, hash: str) -> HookDefinition:
        if not client.is_open():
            raise Exception("xrpl Client is not connected")
        hook_def_request = LedgerEntry(
            hook_definition=hash,
        )
        hook_def_res = await client.request(hook_def_request)
        return hook_def_res.result["node"]

    @staticmethod
    async def get_hook_state_dir(client: WebsocketClient, account: str, namespace: str):
        if not client.is_open():
            raise Exception("xrpl Client is not connected")
        request = {
            "account": account,
            "namespace_id": hex_namespace(namespace),
        }
        response = await client.request(request)
        return response.result["namespace_entries"]

    @staticmethod
    async def get_hook_state(
        client: WebsocketClient, account: str, key: str, namespace: str
    ) -> HookState:
        if not client.is_open():
            raise Exception("xrpl Client is not connected")
        hook_state_req = LedgerEntry(
            hook_state={
                "account": account,
                "key": key,
                "namespace_id": hex_namespace(namespace),
            },
        )
        hook_state_resp = await client.request(hook_state_req)
        return hook_state_resp.result["node"]

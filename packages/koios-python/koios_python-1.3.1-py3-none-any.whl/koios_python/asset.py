#!/usr/bin/env python
"""
Provides all asset functions
"""
import json
import requests
from .environment import *


@Exception_Handler
def get_asset_list(self, content_range="0-999"):
    """
    Get the list of all native assets (paginated, sorted)

    :return: list with all asset list.
    :param str content_range: number of selected elements to return
    :rtype: list.
    """
    timeout = get_timeout()
    custom_headers = {"Range": str(content_range)}
    custom_params = {"order": "asset_name.asc"}
    asset_list = requests.get(self.ASSET_LIST_URL, headers = custom_headers, params = custom_params, timeout=timeout)
    asset_list = json.loads(asset_list.content)

    return asset_list


@Exception_Handler
def get_asset_token_registry(self, content_range="0-999"):
    """
    Get a list of assets registered via token registry on Github

    :return: list of all asset token registry.
    :param str content_range: number of selected elements to return
    :rtype: list.    
    """
    timeout = get_timeout()
    custom_headers = {"Range": str(content_range)}
    token_registry = requests.get(self.ASSET_TOKEN_REGISTRY_URL, headers = custom_headers, timeout=timeout)
    token_registry = json.loads(token_registry.content)

    return token_registry


@Exception_Handler
def get_asset_addresses(self, asset_policy, asset_name, content_range="0-999"):
    """
    Get the list of all addresses holding a given asset.

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :param str asset_name: string with Asset Name in hexadecimal format (hex).
    :param str content_range: number of selected elements to return
    :return: list of all addresses.
    :rtype: list.
    """
    timeout = get_timeout()
    custom_headers = {"Range": str(content_range)}
    custom_params = {"order": "payment_address.asc"}
    info = requests.get(f"{self.ASSET_ADDRESSES_URL}{asset_policy}&_asset_name={asset_name}", \
        headers = custom_headers, params = custom_params, timeout=timeout)
    info = json.loads(info.content)

    return info


@Exception_Handler
def get_asset_nft_address(self, asset_policy, asset_name):
    """
    Get the address where specified NFT currently reside on.

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :param str asset_name: string with Asset Name in hexadecimal format (hex).
    :return: list with payment addresses.
    :rtype: list.
    """
    timeout = get_timeout()
    info = requests.get(f"{self.ASSET_NFT_ADDRESS_URL}{asset_policy}&_asset_name={asset_name}", timeout=timeout)
    info = json.loads(info.content)

    return info


@Exception_Handler
def get_asset_info(self, asset_policy, asset_name):
    """
    Get the information of an asset including first minting & token registry metadata.

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :param str asset_name: string with Asset Name in hexadecimal format (hex).
    :return: list of all asset info.
    :rtype: list.
    """
    timeout = get_timeout()
    info = requests.get(f"{self.ASSET_INFO_URL}{asset_policy}&_asset_name={asset_name}", timeout=timeout)
    info = json.loads(info.content)

    return info


@Exception_Handler
def get_asset_info_bulk(self, *asset_list):
    """
    Get the information of a list of assets including first minting & token registry metadata.
    :param list asset_list: list of assets to query.
    :return: list of all asset info.
    :rtype: list.
    """
    timeout = get_timeout()
    get_format = {"_asset_list": asset_list}
    asset_info = requests.post(self.ASSET_INFO_BULK_URL, json= get_format, timeout=timeout)
    asset_info = json.loads(asset_info.content)

    return asset_info


@Exception_Handler
def get_asset_history(self, asset_policy, asset_name):
    """
    Get the mint/burn history of an asset.

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :param str asset_name: string with Asset Name in hexadecimal format (hex).
    :return: list of asset mint/burn history.
    :rtype: list.
    """
    timeout = get_timeout()
    history = requests.get(f"{self.ASSET_HISTORY_URL}{asset_policy}&_asset_name={asset_name}", timeout=timeout)
    history = json.loads(history.content)

    return history


@Exception_Handler
def get_policy_asset_addresses(self, asset_policy, content_range="0-500"):
    """
    Get the list of addresses with quantity for each asset on the given policy

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :param str content_range: number of selected elements to return
    :return: list of all addresses.
    :rtype: list.
    """
    timeout = get_timeout()
    custom_headers = {"Range": str(content_range)}
    custom_params = {"order": "asset_name.asc"}
    info = requests.get(f"{self.POLICY_ASSET_ADDRESSES_LIST_URL}{asset_policy}",
            headers = custom_headers, params = custom_params, timeout = timeout)
    info = json.loads(info.content)

    return info


@Exception_Handler
def get_policy_asset_info(self, asset_policy):
    """
    Get the information for all assets under the same policy.

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :return: list of all mint/burn transactions for an asset
    :rtype: list.
    """
    timeout = get_timeout()
    info = requests.get(f"{self.POLICY_ASSET_INFO_URL}{asset_policy}", timeout=timeout)
    info = json.loads(info.content)

    return info


@Exception_Handler
def get_policy_asset_list(self, asset_policy, content_range="0-999"):
    """
    Get the list of asset under the given policy (including balances)

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :param str content_range: number of selected elements to return
    :return: list of all assets under the same policy.
    :rtype: list.
    """
    timeout = get_timeout()
    custom_headers = {"Range": str(content_range)}
    custom_params = {"order": "asset_name.asc"}
    info = requests.get(f"{self.POLICY_ASSET_LIST_URL}{asset_policy}",
            headers = custom_headers, params = custom_params, timeout = timeout)
    info = json.loads(info.content)

    return info


@Exception_Handler
def get_asset_summary(self, asset_policy, asset_name):
    """
    Get the summary of an asset (total transactions exclude minting/total wallets include only
    wallets with asset balance).

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :param str asset_name: string with Asset Name in hexadecimal format (hex).
    :return: list of asset summary information.
    :rtype: list.
    """
    timeout = get_timeout()
    summary = requests.get(f"{self.ASSET_SUMMARY_URL}{asset_policy}&_asset_name={asset_name}", timeout=timeout)
    summary = json.loads(summary.content)

    return summary


@Exception_Handler
def get_asset_txs(self, asset_policy, asset_name, after_block_height=0, history=False, content_range="0-999"):
    """
    Get the list of current or all asset transaction hashes (newest first)

    :param str asset_policy: asset Policy ID in hexadecimal format (hex).
    :param str asset name: Asset Name in hexadecimal format (hex), empty asset name returns royalties
    :param int after_block_height: Block height for specifying time delta
    :param bool history: Include all historical transactions, setting to false includes only the non-empty ones
    :param str content_range: number of selected elements to return
    :return: list of all assets under the same policy.
    :rtype: list.
    """
    timeout = get_timeout()
    custom_headers = {"Range": str(content_range)}
    
    if history is True:
        history = "true"
        txs = requests.get(f"{self.ASSET_TXS_URL}{asset_policy}&_asset_name={asset_name} \
                           &_after_block_height={after_block_height}&_history={history}",
                            headers=custom_headers, timeout=timeout)
        txs = json.loads(txs.content)
    if history is False:
        history = "false"
        txs = requests.get(f"{self.ASSET_TXS_URL}{asset_policy}&_asset_name={asset_name} \
                           &_after_block_height={after_block_height}&_history={history}",
                           headers=custom_headers, timeout=timeout)
        txs = json.loads(txs.content)

    return txs

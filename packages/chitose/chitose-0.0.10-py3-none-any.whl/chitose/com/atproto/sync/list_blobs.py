# GENERATED CODE - DO NOT MODIFY
""""""
from __future__ import annotations
import chitose
import typing

def _list_blobs(call: chitose.xrpc.XrpcCall, did: str, latest: typing.Optional[str]=None, earliest: typing.Optional[str]=None) -> bytes:
    """List blob cids for some range of commits


    :param did: The DID of the repo.

    :param latest: The most recent commit

    :param earliest: The earliest commit to start from
    """
    return call('com.atproto.sync.listBlobs', [('did', did), ('latest', latest), ('earliest', earliest)], None, {})
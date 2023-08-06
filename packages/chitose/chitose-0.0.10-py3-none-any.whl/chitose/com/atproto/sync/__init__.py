# GENERATED CODE - DO NOT MODIFY
from __future__ import annotations
from chitose.xrpc import XrpcCall
from chitose.xrpc import XrpcSubscribe
from .get_blob import _get_blob
from .get_blocks import _get_blocks
from .get_checkout import _get_checkout
from .get_commit_path import _get_commit_path
from .get_head import _get_head
from .get_record import _get_record
from .get_repo import _get_repo
from .list_blobs import _list_blobs
from .list_repos import _list_repos
from .notify_of_update import _notify_of_update
from .request_crawl import _request_crawl
from .subscribe_repos import _subscribe_repos
import chitose
import typing

class Sync_:
    """We recommend calling methods in this class via the :doc:`chitose.BskyAgent <chitose>` class instead of creating instances of this class directly."""

    def __init__(self, call: XrpcCall, subscribe: XrpcSubscribe) -> None:
        self.call = call
        self.subscribe = subscribe

    def get_head(self, did: str) -> bytes:
        """Gets the current HEAD CID of a repo.


        :param did: The DID of the repo.
        """
        return _get_head(self.call, did)

    def get_blob(self, did: str, cid: str) -> bytes:
        """Get a blob associated with a given repo.


        :param did: The DID of the repo.

        :param cid: The CID of the blob to fetch
        """
        return _get_blob(self.call, did, cid)

    def get_repo(self, did: str, earliest: typing.Optional[str]=None, latest: typing.Optional[str]=None) -> bytes:
        """Gets the repo state.


        :param did: The DID of the repo.

        :param earliest: The earliest commit in the commit range (not inclusive)

        :param latest: The latest commit in the commit range (inclusive)
        """
        return _get_repo(self.call, did, earliest, latest)

    def notify_of_update(self, hostname: str) -> bytes:
        """Notify a crawling service of a recent update. Often when a long break between updates causes the connection with the crawling service to break.


        :param hostname: Hostname of the service that is notifying of update.
        """
        return _notify_of_update(self.call, hostname)

    def request_crawl(self, hostname: str) -> bytes:
        """Request a service to persistently crawl hosted repos.


        :param hostname: Hostname of the service that is requesting to be crawled.
        """
        return _request_crawl(self.call, hostname)

    def list_blobs(self, did: str, latest: typing.Optional[str]=None, earliest: typing.Optional[str]=None) -> bytes:
        """List blob cids for some range of commits


        :param did: The DID of the repo.

        :param latest: The most recent commit

        :param earliest: The earliest commit to start from
        """
        return _list_blobs(self.call, did, latest, earliest)

    def subscribe_repos(self, handler: chitose.xrpc.XrpcHandler, cursor: typing.Optional[int]=None) -> None:
        """Subscribe to repo updates


        :param cursor: The last known event to backfill from.
        """
        _subscribe_repos(self.subscribe, handler, cursor)

    def get_record(self, did: str, collection: str, rkey: str, commit: typing.Optional[str]=None) -> bytes:
        """Gets blocks needed for existence or non-existence of record.


        :param did: The DID of the repo.

        :param commit: An optional past commit CID.
        """
        return _get_record(self.call, did, collection, rkey, commit)

    def list_repos(self, limit: typing.Optional[int]=None, cursor: typing.Optional[str]=None) -> bytes:
        """List dids and root cids of hosted repos"""
        return _list_repos(self.call, limit, cursor)

    def get_commit_path(self, did: str, latest: typing.Optional[str]=None, earliest: typing.Optional[str]=None) -> bytes:
        """Gets the path of repo commits


        :param did: The DID of the repo.

        :param latest: The most recent commit

        :param earliest: The earliest commit to start from
        """
        return _get_commit_path(self.call, did, latest, earliest)

    def get_blocks(self, did: str, cids: list[str]) -> bytes:
        """Gets blocks from a given repo.


        :param did: The DID of the repo.
        """
        return _get_blocks(self.call, did, cids)

    def get_checkout(self, did: str, commit: typing.Optional[str]=None) -> bytes:
        """Gets the repo state.


        :param did: The DID of the repo.

        :param commit: The commit to get the checkout from. Defaults to current HEAD.
        """
        return _get_checkout(self.call, did, commit)
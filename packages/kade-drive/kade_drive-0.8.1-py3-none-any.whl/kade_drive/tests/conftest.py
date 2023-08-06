# # import asyncio``
# import random
# import hashlib
# # pylint: disable=no-name-in-module
# from struct import pack

# import pytest

# from kade_drive.core.network import Server
# from kade_drive.core.node import Node
# from kade_drive.core.routing import RoutingTable


# # @pytest.fixture()
# # def event_loop():
# #     return asyncio.get_event_loop()


# # @pytest.fixture()
# # def bootstrap_node():
# #     server = Server()
# #     server.listen(8468)

#     # try:
#     #     yield ('127.0.0.1', 8468)
#     # finally:
#     #     server.stop()
#     #     event_loop.close()

# # pylint: disable=redefined-outer-name
# @pytest.fixture()
# def mknode():
#     def _mknode(node_id=None, ip_addy=None, port=None, intid=None):
#         """
#         Make a node.  Created a random id if not specified.
#         """
#         if intid is not None:
#             node_id = pack('>l', intid)
#         if not node_id:
#             randbits = str(random.getrandbits(255))
#             node_id = hashlib.sha1(randbits.encode()).digest()
#         return Node(node_id, ip_addy, port)
#     return _mknode


# # pylint: disable=too-few-public-methods
# class FakeProtocol:  # pylint: disable=too-few-public-methods
#     def __init__(self, source_id, ksize=20):
#         self.router = RoutingTable(ksize, Node(source_id))
#         self.storage = {}
#         self.source_id = source_id


# # pylint: disable=too-few-public-methods
# class FakeServer:
#     def __init__(self, node_id):
#         self.id = node_id  # pylint: disable=invalid-name
#         self.protocol = FakeProtocol(self.id)
#         self.router = self.protocol.router


# @pytest.fixture
# def fake_server(mknode):
#     return FakeServer(mknode().id)

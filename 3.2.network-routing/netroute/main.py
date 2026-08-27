from pprint import pprint

from netroute.factory import mobile_network, single_network
from netroute.network import IPAddress
from netroute.router import Router

net = mobile_network(25, 128)

routers = [d for d in net.values() if isinstance(d, Router)]
for r in routers:
    print(f"Router {r.address} routing table:")
    pprint(r.routing_table())
    break

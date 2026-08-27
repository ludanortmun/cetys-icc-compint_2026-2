# Network packet routing

## Introduction

In this activity, you will simulate the routing of packets across a network made up of several subnets. Each subnet has
one **router**, which acts as the gateway for that subnet, and any number of **clients**. Clients can only send traffic
to their own gateway, while routers can forward traffic either to their own clients, or to other routers they are
directly peered with.

Every link between two devices (client-to-router or router-to-router) introduces some latency, measured in milliseconds.
The total latency of a link is the sum of the latencies of the two devices at either end of that link. For example, if a
client with 10ms latency is connected to a router with 20ms latency, the total latency of the link between them is 30ms.
When a packet travels across the network, you will need to find a path from the source device to the destination device
that minimizes the total accumulated latency. This is a shortest-path problem, and you are expected to solve it using
**Dijkstra's algorithm**.

## Setup

From this project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run and validate

Run the TUI with:

```bash
python -m netroute.main
```

Run the grading tests with:

```bash
pytest
```

## Student instructions

Your implementation belongs in `netroute/client.py`, `netroute/router.py`, and `netroute/network.py`. Do not change the
public method signatures there.

You are provided with the following supporting classes, which you must not modify:

- `IPAddress` (`netroute/address.py`): represents an IPv4 address. Every address belongs to a `/24`
  subnet; `subnet_address` returns the subnet's own address (e.g. `192.168.1.0` for `192.168.1.5`), and `is_subnet`
  tells you whether an address *is* a subnet address rather than a host address.
- `RoutingTable` (`netroute/routing.py`): a mapping of destination addresses (or whole subnets) to the address of the
  next hop that should be used to reach them. `next_hop` resolves the next hop for a destination, falling back to the
  destination's subnet route, and then to a default route, if configured.
- `DeviceRegistry` / `DeviceResolver` (`netroute/registry.py`): lets you resolve a `Device` (a
  `Client` or `Router`) from its `IPAddress`.
- `Device` (`netroute/device.py`): the common interface implemented by `Client` and `Router`, exposing `address`,
  `get_routing_table`, and `get_link_latency` (the latency, in milliseconds, introduced by that device's link to the
  rest of the network).

A device's routing table is not limited to its immediate neighbors: a router's table must contain an
entry for *every* subnet reachable anywhere in the network, each one pointing to whichever
directly-peered router is the best next hop for reaching it. For example, given three routers
peered in a line, `RouterA — RouterB — RouterC`, `RouterA`'s routing table must include an entry
for `RouterB`'s subnet (via `RouterB`) as well as an entry for `RouterC`'s subnet, also via
`RouterB`, since that is the only way to reach it. Once every device's routing table is built this
way, `Network.send` and `Network.trace` simply follow the next hop recorded at each device in turn
until they reach the destination.

### Part 1: Client routing table

Implement `Client.get_routing_table`. A client can only reach its own gateway, so its routing table should default every
destination to the gateway's address.

### Part 2: Router routing table

Implement `Router.get_routing_table`. A router's routing table must include:

- A direct route to each of its clients.
- A route to every other subnet reachable in the network (whether directly peered or reachable
  only through other routers), using the peer that yields the lowest-latency path as the next hop.

Since a router may be able to reach the same distant subnet through more than one peer, you will
need to apply Dijkstra's algorithm over the network's devices, using each hop's link latency as its
edge weight, to determine, for every reachable subnet, which of the router's own peers should be
used as the next hop to minimize total latency.

### Part 3: Sending packets

Implement `Network.send`. This method must:

- Resolve the source and destination devices using the device registry.
- Walk the packet from hop to hop, consulting each intermediate device's routing table to determine the next hop, until
  it reaches the destination.
- Accumulate the latency introduced by each hop along the way.
- Decrement the packet's TTL (via `Packet.step`) on every hop, dropping the packet (returning a
  `TransmissionResult` with `dropped=True`) if the TTL reaches zero before the destination is reached, if no next hop
  can be resolved, or if the accumulated latency exceeds `timeout_ms`.
- Otherwise, return a `TransmissionResult` with `dropped=False` and the total accumulated latency.

### Part 4: Tracing routes

Implement `Network.trace`. This method must:

- Walk the path from source to destination one hop at a time, in the same way as `send`, using each device's routing
  table to resolve the next hop.
- Return a list of `(address, latency)` tuples, one per hop traversed (including the destination), where `latency` is
  the latency introduced by that specific hop.
- Stop early, returning only the hops discovered so far, if the number of hops exceeds `max_hops`, if the accumulated
  latency exceeds `timeout_ms`, or if no next hop can be resolved.

The TUI's `send` and `trace` commands can be used to validate your implementation manually. Note that this is only added
for your convenience, and is not part of the grading tests. The `pytest`
test suite is the only source of truth for grading.

### Scoring

| Component                  | Points  |
|----------------------------|---------|
| `Client.get_routing_table` | 10      |
| `Router.get_routing_table` | 40      |
| `Network.send`             | 25      |
| `Network.trace`            | 25      |
| **Total**                  | **100** |

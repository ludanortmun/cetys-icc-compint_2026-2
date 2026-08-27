# Network packet routing

## Introduction

In this activity, you will simulate the routing of packets across a network made up of several subnets. Each subnet has
one **router**, which acts as the gateway for that subnet, and any number of **clients**. Clients can only send traffic
to their own gateway, while routers can forward traffic either to their own clients, or to other routers they are
directly peered with.

In a real network, more than one route may connect two subnets. Depending on network hardware and conditions, some
routes may be faster than others, regardless of the number of devices involved (also known as hops). Because of this,
routing algorithms are used to determine the best route for network packets to take based on which path has the lowest
latency.

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

Run the randomized command-line demonstration with:

```bash
python -m netroute.main trace 192.168.10.2
```

Run the grading tests with:

```bash
pytest
```

The tests in `netroute/test_routing_service.py` and
`netroute/test_network.py` create deterministic topologies with explicit latencies. They are independent of the
randomized topology used by the CLI.

## Student instructions

Implement only `RoutingService.build`, `RoutingService.get_for`,
`Network.send`, and `Network.trace`. Do not change their public signatures.

The provided `NetworkResolver` interface and `DeviceRegistry` implementation resolve devices and subnet routers. The
provided factories in
`netroute/factory.py` include deterministic device and topology factories for tests, plus a randomized factory used only
by the CLI.

### Part 1: Build routing tables (40 points)

Implement `RoutingService.build`. Call it explicitly once, after the complete topology has been created.

- Build client tables with the client's gateway as the default route.
- Build router tables with direct routes to their local clients.
- Run Dijkstra's algorithm over routers only.
- The cost of an edge to a peer is
  `current.get_link_latency() + peer.get_link_latency()`.
- For every reachable remote subnet, store the first directly peered router on its minimum-cost path.
- When paths have equal cost, choose the first peer with the lowest
  `IPAddress.value`.
- Leave disconnected subnets without a route.

### Part 2: Retrieve routing tables (10 points)

Implement `RoutingService.get_for` as a lookup of the tables produced by
`build`. It raises `RuntimeError` before tables are built and `ValueError` for an unknown address after a successful
build.

### Part 3: Send packets (25 points)

Implement `Network.send` by following the built routing tables until the destination is reached or delivery must stop.

- Each traversed link adds the current device's latency plus the next device's latency.
- A successful result's total latency equals the sum of the link latencies reported by `trace` for the same route.
- TTL counts links; the source consumes none. Arrival at the destination with TTL exactly `0` is allowed, while
  traversing beyond the TTL drops the packet.
- Arrival at exactly `timeout_ms` is allowed. Exceeding it drops the packet.
- Unknown endpoints, an unavailable route, or an unresolved next hop drop the packet.

### Part 4: Trace routes (25 points)

Implement `Network.trace` by following the same built routing tables as
`send`.

- Start every valid trace with `(source, 0.0)`.
- Each subsequent tuple contains the reached next device and that link's latency: the current device's latency plus the
  next device's latency.
- `max_hops` counts links; the source consumes none. Reaching the destination with exactly `max_hops` is allowed, while
  exceeding it stops the trace.
- Reaching the destination at exactly `timeout_ms` is allowed. Exceeding it stops the trace.
- Unknown endpoints return an empty trace; an unavailable route or unresolved next hop returns the path reached so far.

### Scoring

| Component                |  Points |
|--------------------------|--------:|
| `RoutingService.build`   |      40 |
| `RoutingService.get_for` |      10 |
| `Network.send`           |      25 |
| `Network.trace`          |      25 |
| **Total**                | **100** |

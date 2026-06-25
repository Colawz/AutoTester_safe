# Architecture Decisions

## Storage Layer
We chose LevelDB for local storage due to its fast write performance.
The storage layer handles both block and metadata writes.

## Networking
gRPC is used for inter-node communication.
All traffic is encrypted using TLS 1.3.

## Monitoring
Prometheus metrics are exposed on port 9090.
Grafana dashboards visualize cluster health.

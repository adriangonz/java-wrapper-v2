# Seldon Java wrapper V2

Python adapter for Java code leveraging JPype.

## Benchmarking

Total: 44.5233 secs
Slowest: 0.9173 secs
Fastest: 0.0069 secs
Average: 0.4444 secs
Requests/sec: 224.6015

|                         | Requests/sec | Average (ms) | Slowest (ms) | Fastest (ms) |
| ----------------------- | ------------ | ------------ | ------------ | ------------ |
| Baseline (REST)         | 93.0452      | 1065.0       | 2672.8       | 212.6        |
| ProtobufEncoding (REST) | 224.6015     | 444.4        | 917.3        | 6.9          |

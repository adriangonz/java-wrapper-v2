# Seldon Java wrapper V2

Python adapter for Java code leveraging JPype.

## Benchmarking

|                         | Requests/sec | Average (ms) | Slowest (ms) | Fastest (ms) |
| ----------------------- | ------------ | ------------ | ------------ | ------------ |
| NoJava (REST)           | 439.8588     | 227.2        | 541.9        | 36.6         |
| Baseline (REST)         | 93.0452      | 1065.0       | 2672.8       | 212.6        |
| ProtobufEncoding (REST) | 167.5368     | 596.5        | 1752.9       | 7.5          |

## Approaches

## NoJava

The [`NoJava` wrapper](./python/NoJava.py) is a special case which implements
the Java model in pure Python.
It doesn't use Java or JPype at all.

### Baseline

The [`Baseline` wrapper](./python/Baseline.py) hardcodes the conversion for a
particular input and output type between Python and Java.
That is, it explicitly reads / write data from the relevant fields and converts
it as required.

Note that this approach is not scalable as-is, since it only works when those
input and output types are used (e.g. won't work with `strData`).

### ProtobufEncoding

The [`ProtobufEncoding` wrapper](./python/ProtobufEncoding.py) encodes and
decodes the full input from / to bytes using the `SeldonMessage` protobuf
definition.
This encoding / decoding happens on both the Java and Python side.

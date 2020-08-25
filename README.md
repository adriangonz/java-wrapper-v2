# Seldon Java wrapper V2

Python adapter for Java code leveraging JPype.

## Benchmarking

|                           | Requests/sec | Average (ms) | Slowest (ms) | Fastest (ms) |
| ------------------------- | ------------ | ------------ | ------------ | ------------ |
| NoJava (REST)             | 547.3972     | 180.5        | 2778.4       | 8.4          |
| Baseline (REST)           | 142.4239     | 701.4        | 1113.2       | 121.3        |
| ProtobufEncoding (REST)   | 238.6726     | 418.6        | 651.1        | 63.1         |
| PayloadPassthrough (REST) | 537.7259     | 185.7        | 537.6        | 66.0         |

## Approaches

### NoJava

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

### PayloadPassthrough

The [`PayloadPassthrough` wrapper](./python/PayloadPassthrough.py) passes the
input and output payloads as they are.
In other words, the Python side won't try to encode / decode the request /
response.
Instead, it will use the input / output formats as a communication protocol and
it will Java's responsibility to (de-)serialise it.

Note that this approach requires changes on the Python side.
You can check the [`java-wrapper-v2` branch in the
`github.com/adriangonz/seldon-core`
fork](https://github.com/adriangonz/seldon-core/tree/java-wrapper-v2) for a
prototype of the changes.

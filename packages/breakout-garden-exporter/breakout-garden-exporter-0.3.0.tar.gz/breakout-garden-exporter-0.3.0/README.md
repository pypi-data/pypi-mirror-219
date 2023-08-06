# breakout-garden-exporter

[![Pipeline](https://github.com/andrewjw/breakout-garden-exporter/actions/workflows/build.yml/badge.svg)](https://github.com/andrewjw/breakout-garden-exporter/actions/workflows/build.yml) ![PyPI](https://img.shields.io/pypi/v/breakout-garden-exporter) [![Coverage Status](https://coveralls.io/repos/github/andrewjw/breakout-garden-exporter/badge.svg?branch=main)](https://coveralls.io/github/andrewjw/breakout-garden-exporter?branch=master)

Exposes Prometheus metrics from sensors that are part of [Pimoroni's Breakout Garden family](https://shop.pimoroni.com/collections/breakout-garden).

```
usage: breakout-garden-exporter [-h] [-q] [--bind [BIND]]

Exposes Prometheus metrics from sensors that are part of Pimoroni's Breakout Garden family

optional arguments:
  -h, --help     show this help message and exit
  -q, --quiet    don't log HTTP requests
  --bind [BIND]  the ip address and port to bind to. Default: *:9101
```
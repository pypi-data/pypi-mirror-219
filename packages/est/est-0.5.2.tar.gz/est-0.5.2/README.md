# Est: Spectroscopy workflows

`est` is a library providing tools to define a workflow of treatments for X-ray Absorption Structure analysis.
Treatments are based on eather [PyMca](https://github.com/vasole/pymca)_ or [Larch](https://xraypy.github.io/xraylarch/)

The library offers a convenient object for connecting those two.

An [Orange3](https://github.com/biolab/orange3) add-on is also provided by the library to help user defining graphically the workflow they want to process.

## Installation

``` python
pip install est[full]
```

## Test

```bash
pytest --pyargs est.tests
```

## Documentation

https://ewoksest.readthedocs.io/

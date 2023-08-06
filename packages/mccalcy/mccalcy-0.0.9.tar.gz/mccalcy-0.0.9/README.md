# McCalcy Package

The McCalcy package provides a Calculator class that allows you to perform basic arithmetic operations and manipulate a memory value.

## Installation

To install the McCalcy package, you can use pip:

```
pip install mccalcy
```

## Usage

First, import the package:

```python
from mccalcy import mccalcy
```

Create a Calculator instance:

```python
calc = mccalcy.Calculator()
```

Perform calculations using the available methods:

```python
calc.add(5)
calc.subtract(2)
calc.multiply(3)
calc.divide(2)
calc.root(2)
```

Access the current memory value:

```python
print("Memory:", calc.memory)
```

Reset the memory:

```python
calc.reset_memory()
print("Memory after reset:", calc.memory)
```

Refer to the docstrings in the source code for detailed information on each method.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the [GitHub repository](https://github.com/VitalijusKiubis/mccalcy).

## License

This package is licensed under the [MIT License](LICENSE).

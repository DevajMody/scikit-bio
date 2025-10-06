# Unit Testing with Mocking and Stubbing

This directory contains documentation and instructions for running unit tests that use mocking and stubbing techniques.

## Component Under Test

**HTTPSource** (`skbio/io/_iosources.py`)

This component handles HTTP/HTTPS URL requests to fetch remote data files. It uses the `requests` library to make HTTP GET requests.

## Running the Mock-Based Tests

### Prerequisites

- Python 3.9+
- Virtual environment activated with dependencies installed

### Running Tests

To run the mock-based tests for HTTPSource:

```bash
cd ci
PYTHONPATH=.. python -m pytest ../skbio/io/tests/test_httpsource_mock.py -v
```

### Running All Tests with Coverage

To run all tests including the new mock-based tests and generate coverage:

```bash
cd ci
PYTHONPATH=.. python -m coverage run --rcfile ../.coveragerc -m skbio.test
python -m coverage report --rcfile ../.coveragerc
```

### Viewing Coverage for Specific Module

To see coverage for the HTTPSource module:

```bash
cd ci
python -m coverage report --rcfile ../.coveragerc --include="../skbio/io/_iosources.py"
```

## Test Files

- `skbio/io/tests/test_httpsource_mock.py` - Mock-based tests for HTTPSource

## Documentation

See `mocking.md` for details on:
- Test cases and rationale
- Mocking strategy
- Coverage improvement analysis

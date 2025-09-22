# How to Run Tests

This document explains how to reproduce the test results and coverage report for the scikit-bio project.

## Prerequisites

- Python 3.9+ (tested with Python 3.9.6)
- Git (for cloning and managing the repository)
- Virtual environment support

## Environment Setup

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install build dependencies:**
   ```bash
   pip install numpy cython
   ```

3. **Install the project in development mode with test dependencies:**
   ```bash
   pip install -e ".[test]"
   ```

4. **Install additional testing tools:**
   ```bash
   pip install coverage pytest
   ```

5. **Build Cython extensions:**
   ```bash
   python setup.py build_ext --inplace
   ```

## Running Tests

### Basic Test Execution

To run all tests without coverage:
```bash
cd ci
PYTHONPATH=.. python -m skbio.test
```

### Running Tests with Coverage

To run tests with coverage collection:
```bash
cd ci
PYTHONPATH=.. python -m coverage run --rcfile ../.coveragerc -m skbio.test
```

### Generating Coverage Reports

After running tests with coverage, generate reports:

**Text Report:**
```bash
cd ci
PYTHONPATH=.. python -m coverage report --rcfile ../.coveragerc
```

**HTML Report:**
```bash
cd ci
PYTHONPATH=.. python -m coverage html --rcfile ../.coveragerc -d ../courseProjectDocs/Setup/testCoverage
```

## Expected Results

- **Total Tests**: 3,296 tests
- **Passed**: 3,188 tests
- **Skipped**: 108 tests
- **Failed**: 0 tests
- **Overall Coverage**: 98%
- **Test Duration**: ~44 seconds

## Troubleshooting

- **Import Errors**: Ensure Cython extensions are built with `python setup.py build_ext --inplace`
- **Coverage Not Found**: Install coverage explicitly with `pip install coverage`
- **Module Not Found**: Run tests from the `ci` directory with `PYTHONPATH=..`
- **Virtual Environment**: Ensure virtual environment is activated before running commands

## Output Files

- `testResults.txt`: Text coverage report showing file-by-file coverage statistics
- `testCoverage/index.html`: Interactive HTML coverage report with detailed analysis
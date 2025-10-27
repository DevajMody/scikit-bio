# Mutation Testing

## Setup

**Tool:** mutmut (Python mutation testing tool)

**Component:** simple_calc.py (calculator module)

## Installation

```bash
pip install mutmut
```

## Running Tests

### Run all tests

```bash
python -m pytest test_simple_calc.py -v
```

### Run mutation testing

```bash
mutmut run
```

### View results

```bash
mutmut results
```

### View specific mutant

```bash
mutmut show <mutant_name>
```

Example:
```bash
mutmut show "simple_calc.x_is_positive__mutmut_1"
```

## Configuration

Mutation testing is configured in `setup.cfg`:

```ini
[mutmut]
paths_to_mutate=simple_calc.py
runner=python -m pytest -x test_simple_calc.py
```

## Test Results Location

- `initial_results.txt` - Initial mutation score
- `final_results.txt` - Final mutation score after improvements
- `report.md` - Detailed analysis and findings

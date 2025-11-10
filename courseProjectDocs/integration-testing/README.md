# Integration Testing

This directory contains integration tests that verify interactions between multiple scikit-bio modules.

## Running Tests

### Run all integration tests

```bash
# Using pytest
python -m pytest skbio/integration/tests/test_integration_workflows.py -v

# Or from project root
pytest skbio/integration/tests/test_integration_workflows.py -v
```

### Run specific test class

```bash
# Test sequence and diversity integration
python -m pytest skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceAndDiversity -v

# Test sequence distance and alignment integration
python -m pytest skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceDistanceAndAlignment -v

# Test table and statistics integration
python -m pytest skbio/integration/tests/test_integration_workflows.py::IntegrationTestTableAndStatistics -v
```

### Run specific test

```bash
python -m pytest skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceAndDiversity::test_end_to_end_sequence_diversity_workflow -v
```

## Test Coverage

The integration tests cover the following module interactions:

1. **IO → Sequence → Diversity**
   - Read FASTA files
   - Process DNA sequences
   - Calculate diversity metrics

2. **Sequence → Distance → Statistics**
   - Create DNA sequences
   - Calculate Hamming distances
   - Compute GC content
   - Perform sequence transformations

3. **Table → Statistics**
   - Create biological count tables
   - Calculate statistical summaries
   - Test table operations

## Expected Results

All 8 tests should pass:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/devajmody/Repos/msse/qa/scikit-bio
collected 8 items

skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceAndDiversity::test_end_to_end_sequence_diversity_workflow PASSED
skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceAndDiversity::test_io_to_sequence_processing PASSED
skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceAndDiversity::test_sequence_to_diversity_calculation PASSED
skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceDistanceAndAlignment::test_sequence_distance_calculations PASSED
skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceDistanceAndAlignment::test_sequence_gc_content_across_sequences PASSED
skbio/integration/tests/test_integration_workflows.py::IntegrationTestSequenceDistanceAndAlignment::test_sequence_operations_integration PASSED
skbio/integration/tests/test_integration_workflows.py::IntegrationTestTableAndStatistics::test_table_filtering_and_reduction PASSED
skbio/integration/tests/test_integration_workflows.py::IntegrationTestTableAndStatistics::test_table_operations_with_statistics PASSED

========================= 8 passed, 1 warning in 1.06s =========================
```

## Test Files

- `test_integration_workflows.py` - Main integration test suite
- `report.md` - Detailed test design, results, and analysis

## Dependencies

The tests use the following scikit-bio modules:
- `skbio.io` - File I/O operations
- `skbio.sequence` - Sequence manipulation
- `skbio.diversity` - Diversity metrics
- `skbio.tree` - Phylogenetic trees
- `skbio.table` - Data tables
- `skbio.sequence.distance` - Distance calculations

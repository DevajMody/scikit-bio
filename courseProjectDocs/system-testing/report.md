# System Testing Report

## Test Scope and Coverage

Black-box tests that validate scikit-bio's main workflows through its public API, treating the library as a whole without looking at internal code.

**Workflows Covered:**
- DNA sequence analysis pipeline (read, process, analyze)
- Diversity metrics calculation from sample data
- Phylogenetic tree-based analysis

## Test Case Summary

| # | Title | Pre-conditions | Test Steps | Expected Results |
|---|-------|----------------|------------|------------------|
| 1 | FASTA to Diversity Analysis | FASTA file with 3+ sequences exists | 1. Import skbio modules 2. Read FASTA file using `skbio.io.read()` 3. Convert to DNA objects 4. Calculate Shannon diversity | Diversity values returned as pandas Series with positive values |
| 2 | Sequence Transformation Pipeline | None | 1. Create DNA sequence "ACGTACGT" 2. Call `reverse_complement()` 3. Call `transcribe()` 4. Call `translate()` | Returns "ACGTACGT" reversed, RNA transcription "ACGUACGU", protein "VRY" |
| 3 | Phylogenetic Diversity Calculation | Newick tree string, OTU count data | 1. Create TreeNode from Newick string 2. Create counts array 3. Call `alpha_diversity('faith_pd', ...)` with tree | Faith's PD values > 0 for all samples |
| 4 | GC Content Analysis | None | 1. Create sequences with known GC content 2. Call `gc_content()` on each | 100% GC seq returns 1.0, 0% GC returns 0.0, 50% GC returns 0.5 |

## Execution and Results

**Total Tests:** 4
**Passed:** 4
**Failed:** 0

### Results Summary

| Test | Status | Notes |
|------|--------|-------|
| FASTA to Diversity Analysis | Pass | Complete workflow executes correctly |
| Sequence Transformation Pipeline | Pass | All transformations produce expected output |
| Phylogenetic Diversity Calculation | Pass | Tree integration works as expected |
| GC Content Analysis | Pass | Calculations accurate to decimal precision |

### Observations
- All end-to-end workflows complete without errors
- API behaves consistently with documented behavior
- No unexpected exceptions or edge case failures

## Group Contributions

**Devaj:**
- Wrote 4 black-box test cases
- Ran tests and documented results
- Created README and report

# Performance Testing Report

## Test Type Selected: Load Test

### 1. Test Scope and Design

**Components Tested:**
- `skbio.sequence.DNA` - Sequence creation and operations
- `skbio.diversity.alpha_diversity` - Shannon diversity calculation
- `skbio.sequence.distance.hamming` - Distance computation

**Tool Used:** Python `cProfile` + `timeit` + `tracemalloc`

Since scikit-bio is a library (not a web service), load testing here means measuring how operations perform under repeated execution, like in batch bioinformatics pipelines.

### 2. Configuration

| Parameter | Value |
|-----------|-------|
| Iterations | 1000 per operation |
| Sequence Length | 1200 nucleotides |
| OTU Table | 50 samples × 100 OTUs |
| Duration | Until completion |
| Load Pattern | Sequential batch |

### 3. Results

#### Timing Results (1000 iterations)

| Operation | Total Time | Avg per Op | Throughput |
|-----------|------------|------------|------------|
| DNA Creation (1200bp) | 0.183s | 0.183ms | ~5,400/sec |
| GC Content | 0.031s | 0.031ms | ~32,000/sec |
| Reverse Complement | 0.127s | 0.127ms | ~7,800/sec |
| Shannon Diversity | 0.214s | 0.214ms | ~4,600/sec |
| Hamming Distance | 0.058s | 0.058ms | ~17,200/sec |

#### Memory Usage

| Metric | Value |
|--------|-------|
| Baseline | 47 MB |
| After 1000 DNA seqs | 91 MB |
| Peak | 94 MB |
| Growth | +44 MB |

#### cProfile Top Functions

```
ncalls  tottime  cumtime  function
1000    0.091    0.183    DNA.__init__
1000    0.047    0.068    _grammared_sequence.reverse_complement
1000    0.036    0.049    _alpha.shannon
5000    0.029    0.029    numpy.array
```

### 4. Performance Findings

**Finding: Memory accumulation in batch sequence processing**

Memory grows ~44KB per DNA sequence object created. Running 1000 sequences increased memory from 47MB to 91MB. This means processing 100,000 sequences would need ~4.4GB RAM. Should process in batches with cleanup between them.

### 5. Group Contributions

**Devaj:**
- Ran load tests using cProfile and tracemalloc
- Found memory accumulation issue
- Created README and report

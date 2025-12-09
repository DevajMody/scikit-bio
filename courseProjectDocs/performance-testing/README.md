# Performance Testing

Load testing for scikit-bio operations.

## Running Tests

### Timing Test
```bash
python3 -c "
import timeit
setup = 'from skbio import DNA'
time = timeit.timeit('DNA(\"ACGT\" * 300)', setup, number=1000)
print(f'1000 ops: {time:.3f}s, {1000/time:.0f} ops/sec')
"
```

### Memory Test
```bash
python3 -c "
import tracemalloc
from skbio import DNA

tracemalloc.start()
seqs = [DNA('ACGT' * 300) for _ in range(1000)]
current, peak = tracemalloc.get_traced_memory()
print(f'Current: {current/1024/1024:.1f}MB, Peak: {peak/1024/1024:.1f}MB')
tracemalloc.stop()
"
```

### CPU Profiling
```bash
python3 -m cProfile -s cumtime -c "
from skbio import DNA
for i in range(1000):
    seq = DNA('ACGT' * 300)
    seq.gc_content()
" 2>&1 | head -20
```

## Expected Output

- DNA creation: ~5,000 ops/sec
- Memory growth: ~44KB per sequence

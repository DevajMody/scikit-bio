# System Testing

Black-box system-level tests for scikit-bio end-to-end workflows.

## Running Tests

```bash
# Test 1: FASTA to Diversity
python3 -c "
from skbio.io import read
from skbio import DNA
from skbio.diversity import alpha_diversity
import numpy as np

# Read FASTA, calculate diversity
counts = np.array([[3, 5, 2], [4, 2, 1]])
result = alpha_diversity('shannon', counts, ['A', 'B'])
print('Shannon diversity:', result.values)
"

# Test 2: Sequence Transformations
python3 -c "
from skbio import DNA
seq = DNA('ACGTACGT')
print('Original:', seq)
print('Reverse complement:', seq.reverse_complement())
print('Transcribed:', seq.transcribe())
print('Translated:', seq.transcribe().translate())
"

# Test 3: Phylogenetic Diversity
python3 -c "
import io
from skbio import TreeNode
from skbio.diversity import alpha_diversity
import numpy as np

tree = TreeNode.read(io.StringIO('((OTU1:0.5,OTU2:0.5):0.5,OTU3:1.0);'))
counts = np.array([[5, 3, 2], [2, 4, 1]])
result = alpha_diversity('faith_pd', counts, ['A', 'B'], tree=tree, taxa=['OTU1', 'OTU2', 'OTU3'])
print('Faith PD:', result.values)
"

# Test 4: GC Content
python3 -c "
from skbio import DNA
seqs = [DNA('GCGCGC'), DNA('ATATAT'), DNA('GCATAT')]
for s in seqs:
    print(f'{s}: GC={s.gc_content():.2f}')
"
```

## Expected Output

- Test 1: Positive Shannon diversity values
- Test 2: Correct transformations (RNA, protein sequences)
- Test 3: Positive Faith's PD values
- Test 4: GC content of 1.0, 0.0, and 0.5 respectively

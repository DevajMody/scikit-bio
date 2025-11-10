# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------

import io
import tempfile
import os
from unittest import TestCase, main

import numpy as np
import pandas as pd

from skbio import DNA, RNA, Sequence
from skbio.sequence.distance import hamming
from skbio.diversity import alpha_diversity
from skbio.io import read
from skbio import TreeNode
from skbio.table import Table


class IntegrationTestSequenceAndDiversity(TestCase):
    """Integration test: IO → Sequence → Diversity workflows."""

    def setUp(self):
        """Set up test data for sequence and diversity testing."""
        # Create a temporary FASTA file with DNA sequences
        self.fasta_content = """>seq1
ACGTACGTACGT
>seq2
GTCGTCGTCGTC
>seq3
TTTTAAAACCCC
"""
        self.temp_dir = tempfile.mkdtemp()
        self.fasta_file = os.path.join(self.temp_dir, 'test_seqs.fasta')

        with open(self.fasta_file, 'w') as f:
            f.write(self.fasta_content)

        # Create OTU table (counts data) for diversity analysis
        # Each row is a sample, each column is an OTU/species
        self.counts = np.array([
            [5, 3, 0, 2, 0],  # Sample A
            [0, 2, 4, 4, 1],  # Sample B
            [1, 0, 1, 1, 6]   # Sample C
        ])
        self.sample_ids = ['A', 'B', 'C']
        self.otu_ids = ['OTU1', 'OTU2', 'OTU3', 'OTU4', 'OTU5']

        # Create a simple phylogenetic tree for Faith's PD
        self.tree = TreeNode.read(io.StringIO(
            '(((((OTU1:0.5,OTU2:0.5):0.5,OTU3:1.0):1.0):'
            '0.0,(OTU4:0.75,OTU5:0.75):1.25):0.0)root;'))

    def test_io_to_sequence_processing(self):
        """Test reading FASTA files and processing sequences."""
        # Read sequences from FASTA file - need to specify constructor
        sequences = []
        for seq in read(self.fasta_file, format='fasta'):
            sequences.append(DNA(seq))

        # Verify sequences were read correctly
        self.assertEqual(len(sequences), 3)
        self.assertEqual(str(sequences[0]), 'ACGTACGTACGT')
        self.assertEqual(str(sequences[1]), 'GTCGTCGTCGTC')
        self.assertEqual(str(sequences[2]), 'TTTTAAAACCCC')

        # Test sequence operations
        seq1 = sequences[0]
        self.assertEqual(seq1.gc_content(), 0.5)

        # Test sequence transformations
        seq1_rc = seq1.reverse_complement()
        self.assertEqual(str(seq1_rc), 'ACG TACGTACGT'.replace(' ', ''))

    def test_sequence_to_diversity_calculation(self):
        """Test using sequence-derived data for diversity metrics."""
        # Create a Table from counts data
        table = Table(self.counts, self.sample_ids, self.otu_ids)

        # Calculate alpha diversity metrics
        # Test 1: Observed species (OTUs)
        sobs = alpha_diversity('sobs', self.counts, self.sample_ids)
        self.assertEqual(len(sobs), 3)
        self.assertTrue(all(sobs >= 0))

        # Test 2: Shannon diversity
        shannon = alpha_diversity('shannon', self.counts, self.sample_ids)
        self.assertEqual(len(shannon), 3)
        self.assertTrue(all(shannon >= 0))

        # Test 3: Faith's Phylogenetic Diversity (requires tree)
        faith_pd = alpha_diversity('faith_pd', self.counts,
                                   self.sample_ids,
                                   tree=self.tree,
                                   taxa=self.otu_ids)
        self.assertEqual(len(faith_pd), 3)
        self.assertTrue(all(faith_pd > 0))

    def test_end_to_end_sequence_diversity_workflow(self):
        """End-to-end test: Read sequences → Process → Calculate diversity."""
        # Step 1: Read sequences from FASTA
        sequences = []
        for seq in read(self.fasta_file, format='fasta'):
            sequences.append(DNA(seq))

        # Step 2: Create a simple OTU table from sequence lengths
        seq_lengths = [len(seq) for seq in sequences]
        sample_ids = [f'seq{i}' for i in range(len(sequences))]
        otu_ids = ['pos1', 'pos2', 'pos3', 'pos4']

        # Create a synthetic counts table from sequence data
        # Count nucleotide occurrences at specific positions
        counts_data = []
        for seq in sequences:
            row = [str(seq).count('A'), str(seq).count('T'),
                   str(seq).count('G'), str(seq).count('C')]
            counts_data.append(row)

        counts_array = np.array(counts_data)

        # Step 3: Calculate diversity
        table = Table(counts_array, sample_ids, otu_ids)
        diversity_results = alpha_diversity('shannon', counts_array, sample_ids)

        # Verify results - alpha_diversity returns Series
        self.assertEqual(len(diversity_results), 3)
        self.assertTrue(all(diversity_results > 0))
        self.assertTrue(all(diversity_results < 2.0))  # Shannon index range

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.fasta_file):
            os.remove(self.fasta_file)
        os.rmdir(self.temp_dir)


class IntegrationTestSequenceDistanceAndAlignment(TestCase):
    """Integration test: Sequence → Distance → Alignment workflows."""

    def test_sequence_distance_calculations(self):
        """Test calculating distances between sequences."""
        # Create test sequences
        seq1 = DNA('ACGTACGT')
        seq2 = DNA('ACGTACGA')  # Different last base
        seq3 = DNA('TTTTAAAA')

        # Test Hamming distance (returns proportion, not count)
        dist_1_2 = hamming(seq1, seq2)
        self.assertEqual(dist_1_2, 1/8)  # 1 out of 8 positions different

        dist_1_3 = hamming(seq1, seq3)
        self.assertEqual(dist_1_3, 0.75)  # 6 out of 8 positions different

    def test_sequence_gc_content_across_sequences(self):
        """Test GC content calculation across multiple sequences."""
        sequences = [
            DNA('GCGCGCGC'),      # 100% GC
            DNA('ATATATATA'),     # 0% GC
            DNA('GCATGCAT')       # 50% GC
        ]

        gc_contents = [seq.gc_content() for seq in sequences]

        self.assertEqual(gc_contents[0], 1.0)
        self.assertEqual(gc_contents[1], 0.0)
        self.assertAlmostEqual(gc_contents[2], 0.5)

    def test_sequence_operations_integration(self):
        """Test integrated sequence operations."""
        # Create a sequence
        seq = DNA('ACGTACGTACGT')

        # Perform multiple operations
        rc = seq.reverse_complement()
        gc = seq.gc_content()
        trans = seq.transcribe()
        prot = trans.translate()

        # Verify transformations
        self.assertEqual(str(rc), 'ACG TACGTACGT'.replace(' ', ''))
        self.assertEqual(gc, 0.5)
        self.assertEqual(str(trans), 'ACGUACGUACGU')
        # Translation of ACG UAC GUA CGU gives TYVR (includes stop codon *)
        self.assertEqual(str(prot), 'TYVR')


class IntegrationTestTableAndStatistics(TestCase):
    """Integration test: Table → Statistics workflows."""

    def test_table_operations_with_statistics(self):
        """Test table operations and statistical summaries."""
        # Create test data
        data = np.array([[3, 5, 1],
                         [2, 3, 4],
                         [1, 2, 3]])
        sample_ids = ['A', 'B', 'C']
        observation_ids = ['OTU1', 'OTU2', 'OTU3']

        # Create Table
        table = Table(data, sample_ids, observation_ids)

        # Test table properties
        self.assertEqual(table.shape, (3, 3))

        # Calculate basic statistics
        sample_sums = table.sum(axis='observation')
        self.assertEqual(len(sample_sums), 3)
        self.assertTrue(all(sample_sums > 0))

    def test_table_filtering_and_reduction(self):
        """Test table operations and basic manipulation."""
        # Create a test table
        data = np.array([[5, 3, 2, 1],
                         [4, 2, 1, 0],
                         [3, 1, 0, 0]])
        sample_ids = ['A', 'B', 'C']
        obs_ids = ['OTU1', 'OTU2', 'OTU3', 'OTU4']

        table = Table(data, sample_ids, obs_ids)

        # Test basic table operations
        # Calculate totals for each sample
        sample_totals = table.sum(axis='observation')

        # Verify results - table.sum() returns numpy array
        self.assertEqual(len(sample_totals), 3)
        self.assertTrue(all(sample_totals > 0))
        # First sample: 5+3+2+1 = 11
        self.assertEqual(sample_totals[0], 11)
        # Second sample: 4+2+1+0 = 7
        self.assertEqual(sample_totals[1], 7)
        # Third sample: 3+1+0+0 = 4
        self.assertEqual(sample_totals[2], 4)


if __name__ == '__main__':
    main()

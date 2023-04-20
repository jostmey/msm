## Amino Acid Representation

Instead of representing each amino acid residue with its symbol (as in one-hot encoding), we utilize a numerical vector that describes its biochemical properties. These properties convey essential information, such as the interchangeable nature of residues R and K based on their positively charged sidechains. Although numerous biochemical properties exist, many carry redundant information. For instance, the mass of an amino acid residue strongly correlates with its size, rendering it unnecessary to include both values. Atchley and colleagues reduced over 50 amino acid biochemical properties to just five by identifying covarying properties (link). These five values are known as Atchley numbers, which loosely correspond to hydrophobicity, secondary structure, molecular volume, codon diversity, and electrostatic charge.

The CSV files in this folder contain the original Atchley factors. We normalize these factors to achieve unit variance and zero mean. To recompute the normalization, run the following command:

`python3 atchley_factors_normalized.py`


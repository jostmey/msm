## Amino Acid Representation

Rather than represent each amino acid residue by its symbol (as a one-hot encoding), each amino acid residue is represented by a
vector of numbers describing its biochemical properties. The biochemical properties provide information necessary to determine, for
example, that amino acid residues R and K have positively charged sidechains interchangeable with respect to this common property.
There are many biochemical properties, most of which carry redundant information. For example, the mass of an amino acid residue
strongly correlates with its size, so little information is gained by including both numbers. Atchley and colleagues reduced over
50 amino acid biochemical properties to just five by identifying properties that co-vary [(link)](https://www.pnas.org/content/102/18/6395
).
We refer to these five values as Atchley numbers. The five Atchley numbers correspond loosely to hydrophobicity, secondary structure,
molecular volume, codon diversity, and electrostatic charge.

The CSV files located in this folder contain the original Atchley factors. We normalize the Atchley factors to have unit variance and
zero mean. This can be recomputed by running:

`python3 atchley_factors_normalized.py`


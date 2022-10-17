# Max Snippet Model (Work in Progress) 

## Introduction
The full set of T cell receptors in an individual contain traces of past and current immune responses. These traces can serve as biomarkers for diseases mediated by the immune system (e.g. infectious disease, autoimmune disease, cancer). Technological advancements now allow us to sequence T cell receptors from patients. However, only a handful of sequenced T cell receptors from a patient are expected to contain traces relevant to a specific disease. Here we present the latest source code for our method for elucidating these traces.

To determine where to find these traces in the T cell receptor sequences, we had previously analyzed 3D X-ray crystallographic structures of T-cell receptors bound to antigen (disease particles). We observed a contiguous strip typically 4 amino acid residues from complimentary determining region 3 (CDR3) lying in direct contact with each antigen. In addition, the first and last three amino acid residues from each CDR3 are not observed to contact antigen. Based on this observation, we discard the first and last three amino acid residues and extract every possible 4-residue long strip from every CDR3 of a T cell receptor sequence. We call each 4-residue long strip a snippet. To represent each amino acid residue in the snippet, we use Atchley numbers. There are 5 Atchley numbers for each amino acid residue. The Atchley numbers describe biochemical properties of each amino acid residue. Because there are 4 residues in a snippet and 5 Atchley numbers per snippet, we can represent each snippet using 20 Atchley numbers. The number of times a snippet is observed is another important factor for elucidating traces of past and ongoing immune responses. This is because T cells participating in an iummune response can proliferate, potentially creating many copies of a relevant snippet. To quantify the number of copies of each snippet, we take the log of its relative abundance. The relative abundance is calculated as the number of times that same snippet is observed divided by the total number of all snippets. This measurement is included alongside the 20 Atchley numbers for a total of 21 numbers.

Next, the 21 numbers associated with each snippet are scored using a linear kernel. The linear kernel treats each of the 21 numbers as features of the snippet, multiplies each number by a weight, adds a bias term, and computes the sum resulting in a single number for that snippet. Values for weight and bias are determined by a fitting procedure described later. Every snippet from an individual is scored by the linear kernel using the same weight and bias. Next, the highest score among the snippets is selected from an individual using a max operator. The reason for taking the highest score will be explained later. By taking the highest score, the many snippets from an individual are represented using the single number. Finally, the highest score is passed through a sigmoid function that converts the score into a number between 0 and 1 representing a probability.

The weights and bias values are selected such that the model assigns an individual with an immune trace a probability close to 1. Because probability is determined by the highest scoring snippet, at least one snippet will need a high score to assign an individual with an immune trace a probability close to 1. The weights and bias values are also selected such that the model assigns an individual without an immune trace a probability close to 0. Because probability is determined by the highest scoring snippet, no snippet can have a high score to assign an individual without an immune trace a probability close to 0.

A gradient optimization (a.k.a. gradient or steepest descent) based method is used to fit the weights and bias values. We observe gradient optimization frequently becoming stuck in a local optimum. Therefore, we fit many thousands of replicas of the model and pick the model that has the best fit to the training data. This attempts to select the global best optimum among many local optimums. To make efficient use of GPU cards, we coded the optimization procedure to fit many replicas in parallel. After identifying the best optimum, the associated weights and bias are used to score snippets from a holdout individual. We observe that the model will not perform well on holdouts unless we attempt to find the global optimum.

Within this repository, we present several examples implementing our method to identify immune traces that can serve as biomarkers. Each example is self-contained with the associated datasets required to re-run the model. Our examples:
* [distinguish malignant from non-malignant ovarian tissue](ovarian-cancer),
* [diagnose breast cancer from peripheral blood](breast-cancer),
* [predict clearance of preneoplastic cervical lesions](cervical-cancer),
* [and provide an example where our code performed poorly.](colorectal-cancer)

## Publications
* [Cervical Cancer Screening](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8050337/)
* [Ovarian Cancer](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7058380/)
* [Breast and Colorectal Cancer](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6445742/)
* [Multiple Sclerosis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5588725/)

## Requirements
* [Python3](https://www.python.org/)
* [PyTorch](https://pytorch.org//)
* [NumPy](http://www.numpy.org/)
* CUDA GPU
* Linux Environment (Recommended)

## Download
* Download: [zip](https://github.com/jostmey/msm/zipball/master)
* Git: `git clone https://github.com/jostmey/msm`

## To Do
* Change-log of modifications of each model from the original publication (point out where we get identical performance)
* Code to extract top scoring 4mers

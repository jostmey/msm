# Max Snippet Model (Work in Progress) 

## Introduction
The complete set of T cell receptors in an individual carries evidence of both past and current immune responses. These traces can act as biomarkers for diseases mediated by the immune system, such as infectious diseases, autoimmune disorders, and cancer. Recent technological advancements enable us to sequence T cell receptors from patients. Nonetheless, only a small number of sequenced T cell receptors from a patient are expected to contain traces relevant to a specific disease. In this repository, we introduce the latest source code for our method to identify these traces.

To pinpoint the location of these traces within T cell receptor sequences, we previously analyzed 3D X-ray crystallographic structures of T-cell receptors bound to antigens (disease particles). We observed a continuous strip, typically consisting of four amino acid residues from the complementary determining region 3 (CDR3), in direct contact with each antigen. Moreover, the first and last three amino acid residues from each CDR3 do not interact with the antigen. Based on this observation, we discard the first and last three amino acid residues and extract every possible 4-residue long strip from every CDR3 of a T cell receptor sequence. We refer to each 4-residue long strip as a snippet. To represent each amino acid residue in the snippet, we use Atchley numbers, with each amino acid residue having five Atchley numbers that describe its biochemical properties. Since a snippet contains four residues and five Atchley numbers per residue, we can represent each snippet using 20 Atchley numbers. The frequency of a snippet is crucial for identifying traces of past and ongoing immune responses, as T cells involved in an immune response can proliferate, potentially generating multiple copies of a relevant snippet. To quantify the number of copies of each snippet, we calculate the log of its relative abundance, obtained by dividing the number of times that same snippet is observed by the total number of all snippets. This measurement is included alongside the 20 Atchley numbers, resulting in a total of 21 numbers.

Subsequently, the 21 numbers associated with each snippet are evaluated using a linear kernel. The linear kernel treats each of the 21 numbers as features of the snippet, multiplies each number by a weight, adds a bias term, and calculates the sum, resulting in a single number for that snippet. The weight and bias values are determined by a fitting procedure described later. Every snippet from an individual is assessed by the linear kernel using the same weight and bias. The highest score among the snippets is then selected from an individual using a max operator, the reasoning for which will be explained later. By choosing the highest score, the numerous snippets from an individual are represented by a single number. Finally, the highest score is processed through a sigmoid function that converts the score into a probability between 0 and 1.

The weights and bias values are chosen to ensure that the model assigns a probability close to 1 for an individual with an immune trace. As probability is determined by the highest scoring snippet, at least one snippet must have a high score to assign a probability close to 1 for an individual with an immune trace. The weights and bias values are also chosen to ensure that the model assigns a probability close to 0 for an individual without an immune trace. As probability is determined by the highest scoring snippet, no snippet can have a high score to assign a probability close to 0 for an individual without an immune trace.

We employ a gradient optimization method, based on gradient or steepest descent, to fit the weights and bias values. We often observe gradient optimization getting trapped in local optima. To address this issue, we fit thousands of model replicas and select the one with the best fit to the training data, aiming to identify the global optimum among numerous local optima. To efficiently utilize GPU cards, we have coded the optimization procedure to fit multiple replicas in parallel. After determining the best optimum, the corresponding weights and bias values are used to score snippets from a holdout individual. We note that the model's performance on holdouts will be suboptimal unless we strive to find the global optimum, as measured on the training set.

In this repository, we present several examples illustrating our method for identifying immune traces that can serve as biomarkers. Each example is self-contained, complete with the associated datasets required to re-run the model. Some results are successful, while others are not (perhps there are bugs in the code). Our examples demonstrate the ability to:
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
* Bugs in code preventing replication of all published results (some results replicated, some not)
* Change-log of modifications of each model from the original publication (point out where we get identical performance)
* Code to extract top scoring 4mers
* Rename folders to indicate tissue/blood and published/not

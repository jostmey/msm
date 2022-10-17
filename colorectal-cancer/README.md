# Instructions
This example illustrates how our method can be used to predict if colorectal tissue is either “adjacent healthy” or “tumor”. Each person in the dataset has both an “adjacent healthy” and a “tumor” sample collected.

## Dataset
T cell receptors sequenced from 28 tissue samples are in the folder `dataset`. Half of the samples are from adjacent healthy tissue and the other half are from tumor tissue. Use the following commands to extract the data.
```
cd dataset
unzip '*.zip'
cd ../
```

## Modeling
This model uses snippets from the T cell receptor sequences from ovarian tissue to predict if the tissue is adjacent healthy or tumor tissue. The model is fit on data from many individuals. The performance of the model is evaluated using a patient-holdout cross-validation. During the cross-validation, data from an individual is held out during the fitting procedure. That individual is then used to determine how the model performs on an individual not used for fitting. Every individual gets a turn being held out, which is why we must fit the model anew each time an individual is held out. Use the following commands to run the cross-validation. The commands assume you are running the model on a CUDA enabled GPU with at least 11GB of memory.
```
mkdir -p bin
python3 train_val.py --seed 1 --holdouts Patient1 --output bin/1
python3 train_val.py --seed 1 --holdouts Patient2 --output bin/2
python3 train_val.py --seed 1 --holdouts Patient3 --output bin/3
python3 train_val.py --seed 1 --holdouts Patient4 --output bin/4
python3 train_val.py --seed 1 --holdouts Patient5 --output bin/5
python3 train_val.py --seed 1 --holdouts Patient6 --output bin/6
python3 train_val.py --seed 1 --holdouts Patient7 --output bin/7
python3 train_val.py --seed 1 --holdouts Patient8 --output bin/8
python3 train_val.py --seed 1 --holdouts Patient9 --output bin/9
python3 train_val.py --seed 1 --holdouts Patient10 --output bin/10
python3 train_val.py --seed 1 --holdouts Patient11 --output bin/11
python3 train_val.py --seed 1 --holdouts Patient12 --output bin/12
python3 train_val.py --seed 1 --holdouts Patient13 --output bin/13
python3 train_val.py --seed 1 --holdouts Patient14 --output bin/14
```
The first flag `--seed` determines the seed value used to generate the initial guess for the weight values. The second flag `--holdouts` determines the sample to holdout. The third flag --output is the prefix for the filenames saved during the fitting procedure. Additional flags that can be used are --num_fits for determining how many times to try and find the global best fit to the training data and --device for selecting `gpu` or `cpu`.

## Model Customization

## Evaluation
After running each above command and completing the patient-holdout cross-validation, the results can be summarized using the following command.
```
python3 report.py > report.csv
```
The results are stored in a CSV file that can be opened by your favorite spreadsheet viewer. There are nine columns that represent:
1.	The training step.
2.	The accuracy on the training data averaged over the cross-validation.
3.	The true negative rate (specificity) on the training data averaged over the cross-validation.
4.	The true positive rate (sensitivity) on the training data averaged over the cross-validation.
5.	The cross-entropy on the training data averaged over the cross-validation.
6.	The accuracy on the holdout data averaged over the cross-validation.
7.	The true negative rate (specificity) on the holdout data averaged over the cross-validation.
8.	The true positive rate (sensitivity) on the holdout data averaged over the cross-validation.
9.	The cross-entropy on the holdout data averaged over the cross-validation.

## Publication
* [Source of Samples](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5714653/)
* [Original Breast Cancer Model](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6445742/)

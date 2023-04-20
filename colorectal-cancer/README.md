# Instructions
This example demonstrates the application of our method to predict whether colorectal tissue is classified as "adjacent healthy" or "tumor." For each individual in the dataset, both an "adjacent healthy" and a "tumor" sample have been collected.

## Dataset
In the dataset folder, you will find T cell receptor sequences from 28 tissue samples. Half of these samples are from adjacent healthy tissue, while the other half are from tumor tissue. To extract the data, utilize the commands provided below.
```
cd dataset
unzip '*.zip'
cd ../
```

## Modeling
This model leverages snippets from the T cell receptor sequences in ovarian tissue to predict whether the tissue is classified as adjacent healthy or tumor tissue. The model is trained on data from multiple individuals, and its performance is assessed using patient-holdout cross-validation. During this process, data from one individual is withheld during the fitting procedure, and subsequently used to evaluate the model's performance on data not included in the fitting. As each individual takes a turn being held out, the model must be refit for each new holdout. To execute the cross-validation, use the following commands, which assume you are running the model on a CUDA-enabled GPU with a minimum of 11GB memory.
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
The first flag, --seed, sets the seed value for generating the initial guess of the weight values. The second flag, --holdouts, specifies which sample to hold out. The third flag, --output, defines the prefix for filenames saved during the fitting process. Additional flags include --num_fits, which determines the number of attempts to find the global best fit for the training data, and --device, which allows for the selection of either gpu or cpu.

## Evaluation
Upon executing each of the aforementioned commands and completing the patient-holdout cross-validation, you can consolidate the results using the command provided below.
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

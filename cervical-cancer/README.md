# Instructions
This example demonstrates the application of our method for predicting the regression of preneoplastic cervical lesions caused by HPV. Spontaneous regression of these lesions is favorable, as it suggests the individual's immune system can naturally eliminate these precancerous growths. The samples are categorized as either "regress" or "progress/same," with each sample originating from a distinct individual.

## Dataset
The dataset folder contains T cell receptor sequences from 24 cervical samples, with six samples labeled as "progress/same" and eighteen as "regress". To extract the data, use the commands provided below.
```
cd dataset
unzip '*.zip'
cd ../
```

## Modeling
This model employs snippets derived from T cell receptor sequences in ovarian tissue to predict whether the tissue is "progress/same" or "regress". The model is trained on data from numerous individuals, and its performance is assessed through patient-holdout cross-validation. During the cross-validation process, data from a single individual is withheld during the fitting procedure, and subsequently used to evaluate the model's performance on data not included in the fitting. Each individual takes a turn as the holdout, necessitating the model to be refit each time a different individual is held out. To execute the cross-validation, use the following commands, which assume you are running the model on a CUDA-enabled GPU with a minimum of 11GB memo.
```
mkdir -p bin
python3 train_val.py --seed 1 --holdouts 112015051_3_38 --output bin/1
python3 train_val.py --seed 1 --holdouts 3-4_DNA --output bin/2
python3 train_val.py --seed 1 --holdouts 5-15_DNA --output bin/3
python3 train_val.py --seed 1 --holdouts 112015051_4_38 --output bin/4
python3 train_val.py --seed 1 --holdouts 2_31 --output bin/5
python3 train_val.py --seed 1 --holdouts 112015051_3_39 --output bin/6
python3 train_val.py --seed 1 --holdouts 4-1_DNA --output bin/7
python3 train_val.py --seed 1 --holdouts 3-11_DNA --output bin/8
python3 train_val.py --seed 1 --holdouts 5-6_DNA --output bin/9
python3 train_val.py --seed 1 --holdouts 112015051_5_33 --output bin/10
python3 train_val.py --seed 1 --holdouts 3-6_DNA --output bin/11
python3 train_val.py --seed 1 --holdouts 112015051_5_31 --output bin/12
python3 train_val.py --seed 1 --holdouts 112015051_5_39 --output bin/13
python3 train_val.py --seed 1 --holdouts 4-2_DNA --output bin/14
python3 train_val.py --seed 1 --holdouts 112015051_3_40 --output bin/15
python3 train_val.py --seed 1 --holdouts 4-13_DNA --output bin/16
python3 train_val.py --seed 1 --holdouts 5-19_DNA --output bin/17
python3 train_val.py --seed 1 --holdouts 4-22_DNA --output bin/18
python3 train_val.py --seed 1 --holdouts 112015051_4_33 --output bin/19
python3 train_val.py --seed 1 --holdouts 2-30_DNA --output bin/20
python3 train_val.py --seed 1 --holdouts 5-27A_DNA --output bin/21
python3 train_val.py --seed 1 --holdouts 112015051_3_32 --output bin/22
python3 train_val.py --seed 1 --holdouts 112015051_5_35 --output bin/23
python3 train_val.py --seed 1 --holdouts 4-11_DNA --output bin/24
```
The first flag --seed sets the seed value for generating the initial guess of the weight values. The second flag --holdouts specifies the sample to be held out. The third flag --output designates the prefix for filenames saved during the fitting procedure. Optional flags include --num_fits, which determines the number of attempts to find the global best fit for the training data, and --device, which allows the selection of either gpu or cpu for processing.

## How does this differ from the other examples in this repository?
Patients who experience regression are expected to have T cells capable of recognizing their precancerous lesions, while patients who show progression or remain the same are likely lacking T cells that can detect these lesions. Consequently, each "regress" is treated as a case, and each "progress/same" is considered a control. 

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
* [Cervical Cancer Screening](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8050337/)

# Instructions
This example illustrates how our method can be used to predict the regression of preneoplastic cervical lesions resulting from HPV. The spontaneous regression of preneoplastic cervical lesions is good because it would suggest the individual's immune system can naturally clear these precancerous lesions. Samples are either "regress" or "progress/same". Each sample is from a different person.

## Dataset
T cell receptors sequenced from 24 cervical samples are in the folder `dataset`. Six samples are "progress/same" and eighteen samples are "regress". Use the following commands to extract the data.
```
cd dataset
unzip '*.zip'
cd ../
```

## Modeling
This model uses snippets from the T cell receptor sequences from ovarian tissue to predict if the tissue is "progress/same" or "regress". The model is fit on data from many individuals. The performance of the model is evaluated using a patient-holdout cross-validation. During the cross-validation, data from an individual is held out during the fitting procedure. That individual is then used to determine how the model performs on an individual not used for fitting. Every individual gets a turn being held out, which is why we must fit the model anew each time an individual is held out. Use the following commands to run the cross-validation. The commands assume you are running the model on a CUDA enabled GPU with at least 11GB of memory.
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
The first flag `--seed` determines the seed value used to generate the initial guess for the weight values. The second flag `--holdouts` determines the sample to holdout. The third flag --output is the prefix for the filenames saved during the fitting procedure. Additional flags that can be used are --num_fits for determining how many times to try and find the global best fit to the training data and --device for selecting `gpu` or `cpu`.

## Model Customization
Patient's that regress are expected to have T cells that can recognize their precancerous lesions whereas patient's that progress or remain the same are expected to lack T cells that can recognize their precancerous lesions. Therefore, each "regress" is treated as a cases and each "progress/same" is treated as a control.

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
* [Cervical Cancer Screening](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8050337/)

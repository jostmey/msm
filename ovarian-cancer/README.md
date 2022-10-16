# Instructions
This example illustrates how our method can be used to predict if ovarian tissue is either “normal” or “malignant”. Each tissue sample is from a different person.

## Dataset
T cell receptors sequenced from 20 ovarian tissue samples are in the folder `dataset`. Half of the samples are from normal tissue and the other half are from malignant tissue. Use the following commands to extract the data.
```
cd dataset
unzip '*.zip'
cd ../
```

## Modeling
This model uses snippets from the T cell receptor sequences from ovarian tissue to predict if the tissue is normal or malignant. The model is fit on data from many individuals. The performance of the model is evaluated using a patient-holdout cross-validation. During the cross-validation, data from an individual is held out during the fitting procedure. That individual is then used to determine how the model performs on an individual not used for fitting. Every individual gets a turn being held out, which is why we must fit the model anew each time an individual is held out. Use the following commands to run the cross-validation. The commands assume you are running the model on a CUDA enabled GPU with at least 11GB of memory.
```
mkdir -p bin
python3 train_val.py --seed 1 --holdouts O-10M --output bin/1
python3 train_val.py --seed 1 --holdouts O-10N --output bin/2
python3 train_val.py --seed 1 --holdouts O-1M --output bin/3
python3 train_val.py --seed 1 --holdouts O-1N --output bin/4
python3 train_val.py --seed 1 --holdouts O-2M --output bin/5
python3 train_val.py --seed 1 --holdouts O-2N --output bin/6
python3 train_val.py --seed 1 --holdouts O-3M --output bin/7
python3 train_val.py --seed 1 --holdouts O-3N --output bin/8
python3 train_val.py --seed 1 --holdouts O-4M --output bin/9
python3 train_val.py --seed 1 --holdouts O-4N --output bin/10
python3 train_val.py --seed 1 --holdouts O-5M --output bin/11
python3 train_val.py --seed 1 --holdouts O-5N --output bin/12
python3 train_val.py --seed 1 --holdouts O-6M --output bin/13
python3 train_val.py --seed 1 --holdouts O-6N --output bin/14
python3 train_val.py --seed 1 --holdouts O-7M --output bin/15
python3 train_val.py --seed 1 --holdouts O-7N --output bin/16
python3 train_val.py --seed 1 --holdouts O-8M --output bin/17
python3 train_val.py --seed 1 --holdouts O-8N --output bin/18
python3 train_val.py --seed 1 --holdouts O-9M --output bin/19
python3 train_val.py --seed 1 --holdouts O-9N --output bin/20
```
The first flag `--seed` determines the seed value used to generate the initial guess for the weight values. The second flag `--holdouts` determines the sample to holdout. The third flag --output is the prefix for the filenames saved during the fitting procedure. Additional flags that can be used are --num_fits for determining how many times to try and find the global best fit to the training data and --device for selecting GPU or CPU.

## Model Customization
This model introduces the use of a gap in the snippet, which was found to improve performance on this dataset. Gaps are a concept from sequence alignment algorithms that allow spaces to be introduced between individual amino acid residues. The code for the gaps can be found on line 71 in `dataplumbing.py` and is used on line 58 in `train_val.py`. The value `motif_size` determines the number of amino acid residues in the snippet and the difference between `window_size` and `motif_size` determines the number of gaps.

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
* [Ovarian Cancer](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7058380/)

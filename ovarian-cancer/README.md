# Instructions
This example demonstrates the application of our method to distinguish between normal and malignant ovarian tissue. Each tissue sample in the dataset is obtained from a different individual.

## Dataset
T cell receptor sequences from 20 ovarian tissue samples are located in the dataset folder. The samples are evenly split, with half from normal tissue and half from malignant tissue. To extract the data, use the following commands.
```
cd dataset
unzip '*.zip'
cd ../
```

## Modeling
This model employs snippets from T cell receptor sequences in ovarian tissue samples to classify the tissue as either normal or malignant. It is trained on data from numerous individuals, and its performance is assessed using a patient-holdout cross-validation approach. During this process, data from one individual is withheld while fitting the model. Subsequently, the model's performance is evaluated on the withheld individual, who was not used during the fitting. This procedure is repeated for each individual in the dataset, requiring the model to be retrained each time. To execute the cross-validation, use the following commands, assuming the model is run on a CUDA-enabled GPU with a minimum of 11GB memory.
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
The first flag --seed sets the seed value for generating the initial weight guesses. The second flag --holdouts specifies the sample to withhold during validation. The third flag --output defines the prefix for the filenames saved throughout the fitting process. Additional flags include --num_fits, which determines the number of attempts to find the global best fit for the training data, and --device, which allows you to select either gpu or cpu for processing.

## How does this differ from the other examples in this repository?
This model incorporates a gap feature within the snippet, which has been found to enhance performance for this dataset. Gaps, derived from sequence alignment algorithms, allow for spaces between individual amino acid residues. The gap implementation can be found in dataplumbing.py on line 71 and is utilized on line 58 in train_val.py. The motif_size value defines the number of amino acid residues in the snippet, while the difference between window_size and motif_size determines the number of gaps present.

## Evaluation
The results are stored in a CSV file that can be opened by your favorite spreadsheet viewer. There are nine columns that represent:
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

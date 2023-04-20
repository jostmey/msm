# Instructions
This example demonstrates the application of our method to predict whether an individual is "healthy" or affected by "cancer" based on their peripheral blood sample. Each sample is collected from a distinct individual.

## Dataset
The `dataset` folder contains T cell receptor sequences from 32 blood samples, with half of the samples originating from healthy individuals and the other half from breast cancer patients. To extract the data, utilize the commands provided below.
```
cd dataset
unzip '*.zip'
cd ../
```

## Modeling
This model employs snippets derived from T cell receptor sequences in peripheral blood to predict whether an individual is healthy or has breast cancer. The model is trained on data from numerous individuals and its performance is assessed through patient-holdout cross-validation. During the cross-validation process, data from a single individual is withheld during the fitting procedure and subsequently used to evaluate the model's performance on data not included in the fitting. Each individual takes a turn as the holdout, necessitating the model to be refit each time a different individual is held out. To execute the cross-validation, use the following commands, which assume you are running the model on a CUDA-enabled GPU with a minimum of 11GB memory.
```
mkdir -p bin
python3 train_val.py --seed 1 --holdouts BR01B --num_fits 16384 --output bin/1
python3 train_val.py --seed 1 --holdouts BR05B --num_fits 16384 --output bin/2
python3 train_val.py --seed 1 --holdouts BR07B --num_fits 16384 --output bin/3
python3 train_val.py --seed 1 --holdouts BR13B --num_fits 16384 --output bin/4
python3 train_val.py --seed 1 --holdouts BR14B --num_fits 16384 --output bin/5
python3 train_val.py --seed 1 --holdouts BR15B --num_fits 16384 --output bin/6
python3 train_val.py --seed 1 --holdouts BR16B --num_fits 16384 --output bin/7
python3 train_val.py --seed 1 --holdouts BR17B --num_fits 16384 --output bin/8
python3 train_val.py --seed 1 --holdouts BR18B --num_fits 16384 --output bin/9
python3 train_val.py --seed 1 --holdouts BR19B --num_fits 16384 --output bin/10
python3 train_val.py --seed 1 --holdouts BR20B --num_fits 16384 --output bin/11
python3 train_val.py --seed 1 --holdouts BR21B --num_fits 16384 --output bin/12
python3 train_val.py --seed 1 --holdouts BR22B --num_fits 16384 --output bin/13
python3 train_val.py --seed 1 --holdouts BR24B --num_fits 16384 --output bin/14
python3 train_val.py --seed 1 --holdouts BR25B --num_fits 16384 --output bin/15
python3 train_val.py --seed 1 --holdouts BR26B --num_fits 16384 --output bin/16
python3 train_val.py --seed 1 --holdouts HIP00602 --num_fits 16384 --output bin/17
python3 train_val.py --seed 1 --holdouts HIP01091 --num_fits 16384 --output bin/18
python3 train_val.py --seed 1 --holdouts HIP02271 --num_fits 16384 --output bin/19
python3 train_val.py --seed 1 --holdouts HIP02962 --num_fits 16384 --output bin/20
python3 train_val.py --seed 1 --holdouts HIP03194 --num_fits 16384 --output bin/21
python3 train_val.py --seed 1 --holdouts HIP04475 --num_fits 16384 --output bin/22
python3 train_val.py --seed 1 --holdouts HIP05590 --num_fits 16384 --output bin/23
python3 train_val.py --seed 1 --holdouts HIP09020 --num_fits 16384 --output bin/24
python3 train_val.py --seed 1 --holdouts HIP09365 --num_fits 16384 --output bin/25
python3 train_val.py --seed 1 --holdouts HIP11774 --num_fits 16384 --output bin/26
python3 train_val.py --seed 1 --holdouts HIP13449 --num_fits 16384 --output bin/27
python3 train_val.py --seed 1 --holdouts HIP13789 --num_fits 16384 --output bin/28
python3 train_val.py --seed 1 --holdouts HIP14009 --num_fits 16384 --output bin/29
python3 train_val.py --seed 1 --holdouts HIP14045 --num_fits 16384 --output bin/30
python3 train_val.py --seed 1 --holdouts HIP14055 --num_fits 16384 --output bin/31
python3 train_val.py --seed 1 --holdouts HIP14221 --num_fits 16384 --output bin/32
```
The first flag --seed sets the seed value for generating the initial guess of the weight values. The second flag --holdouts specifies the sample to be held out. The third flag --num_fits determines the number of attempts to find the global best fit for the training data, and has been reduced to accommodate larger samples within GPU memory constraints. The fourth flag --output designates the prefix for filenames saved during the fitting procedure. An optional flag, --device, can be utilized to select either gpu or cpu for processing.

## How does this differ from the other examples in this repository?
This dataset comprises individuals from two distinct studies. The first study focuses on healthy individuals, while the second study involves participants with breast cancer. The healthy individuals were chosen to ensure age and sex matching with the breast cancer patients.

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

## Publications
* [Source of Healthy Control Samples](https://www.nature.com/articles/ng.3822)
* [Source of Breast Cancer Samples](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5715779/)
* [Original Breast Cancer Model](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6445742/)

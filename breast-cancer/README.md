# Instructions
This example illustrates how our method can be used to predict if a person is either “healthy” or has “cancer” from their peripheral blood. Each blood sample is from a different person.

## Dataset
T cell receptors sequenced from 32 blood samples are in the folder `dataset`. Half of the samples are from healthy individuals and the other half are from breast cancer patients. Use the following commands to extract the data.
```
cd dataset
unzip '*.zip'
cd ../
```

## Modeling
This model uses snippets from the T cell receptor sequences from peripheral blood to predict if the person is healthy or has breast cancer. The model is fit on data from many individuals. The performance of the model is evaluated using a patient-holdout cross-validation. During the cross-validation, data from an individual is held out during the fitting procedure. That individual is then used to determine how the model performs on an individual not used for fitting. Every individual gets a turn being held out, which is why we must fit the model anew each time an individual is held out. Use the following commands to run the cross-validation. The commands assume you are running the model on a CUDA enabled GPU with at least 11GB of memory.
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
The first flag `--seed` determines the seed value used to generate the initial guess for the weight values. The second flag `--holdouts` determines the sample to holdout. The third flag --num_fits determines how many times to try and find the global best fit to the training data and has been reduced to allow the larger samples to fit into GPU memory. The fourth flag --output is the prefix for the filenames saved during the fitting procedure. An additional flag that can be used is --device for selecting `gpu` or `cpu`.

## Model Customization
This dataset combines individuals from two studies. The first study contains healthy individuals. The second study contains individuals with breast cancer. Healthy individuals were selected to be age and sex matched. 

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

## Publications
* [Source of Healthy Control Samples](https://www.nature.com/articles/ng.3822)
* [Source of Breast Cancer Samples](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5715779/)
* [Original Breast Cancer Model](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6445742/)

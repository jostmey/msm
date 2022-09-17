mkdir -p bin

# Split 1
#
python3 train_val.py --seed 1 --holdouts O-10M --output bin/1_1 > bin/train_val_1_1.out

# Split 2
#
python3 train_val.py --seed 1 --holdouts O-10N --output bin/2_1 > bin/train_val_2_1.out

# Split 3
#
python3 train_val.py --seed 1 --holdouts O-1M --output bin/3_1 > bin/train_val_3_1.out

# Split 4
#
python3 train_val.py --seed 1 --holdouts O-1N --output bin/4_1 > bin/train_val_4_1.out

# Split 5
#
python3 train_val.py --seed 1 --holdouts O-2M --output bin/5_1 > bin/train_val_5_1.out

# Split 6
#
python3 train_val.py --seed 1 --holdouts O-2N --output bin/6_1 > bin/train_val_6_1.out

# Split 7
#
python3 train_val.py --seed 1 --holdouts O-3M --output bin/7_1 > bin/train_val_7_1.out

# Split 8
#
python3 train_val.py --seed 1 --holdouts O-3N --output bin/8_1 > bin/train_val_8_1.out

# Split 9
#
python3 train_val.py --seed 1 --holdouts O-4M --output bin/9_1 > bin/train_val_9_1.out

# Split 10
#
python3 train_val.py --seed 1 --holdouts O-4N --output bin/10_1 > bin/train_val_10_1.out

# Split 11
#
python3 train_val.py --seed 1 --holdouts O-5M --output bin/11_1 > bin/train_val_11_1.out

# Split 12
#
python3 train_val.py --seed 1 --holdouts O-5N --output bin/12_1 > bin/train_val_12_1.out

# Split 13
#
python3 train_val.py --seed 1 --holdouts O-6M --output bin/13_1 > bin/train_val_13_1.out

# Split 14
#
python3 train_val.py --seed 1 --holdouts O-6N --output bin/14_1 > bin/train_val_14_1.out

# Split 15
#
python3 train_val.py --seed 1 --holdouts O-7M --output bin/15_1 > bin/train_val_15_1.out

# Split 16
#
python3 train_val.py --seed 1 --holdouts O-7N --output bin/16_1 > bin/train_val_16_1.out

# Split 17
#
python3 train_val.py --seed 1 --holdouts O-8M --output bin/17_1 > bin/train_val_17_1.out

# Split 18
#
python3 train_val.py --seed 1 --holdouts O-8N --output bin/18_1 > bin/train_val_18_1.out

# Split 19
#
python3 train_val.py --seed 1 --holdouts O-9M --output bin/19_1 > bin/train_val_19_1.out

# Split 20
#
python3 train_val.py --seed 1 --holdouts O-9N --output bin/20_1 > bin/train_val_20_1.out


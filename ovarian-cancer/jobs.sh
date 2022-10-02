mkdir -p bin

# Split 1
#
python3 train_val.py --seed 1 --holdouts O-10M --output bin/1 > bin/train_val_1.out

# Split 2
#
python3 train_val.py --seed 1 --holdouts O-10N --output bin/2 > bin/train_val_2.out

# Split 3
#
python3 train_val.py --seed 1 --holdouts O-1M --output bin/3 > bin/train_val_3.out

# Split 4
#
python3 train_val.py --seed 1 --holdouts O-1N --output bin/4 > bin/train_val_4.out

# Split 5
#
python3 train_val.py --seed 1 --holdouts O-2M --output bin/5 > bin/train_val_5.out

# Split 6
#
python3 train_val.py --seed 1 --holdouts O-2N --output bin/6 > bin/train_val_6.out

# Split 7
#
python3 train_val.py --seed 1 --holdouts O-3M --output bin/7 > bin/train_val_7.out

# Split 8
#
python3 train_val.py --seed 1 --holdouts O-3N --output bin/8 > bin/train_val_8.out

# Split 9
#
python3 train_val.py --seed 1 --holdouts O-4M --output bin/9 > bin/train_val_9.out

# Split 10
#
python3 train_val.py --seed 1 --holdouts O-4N --output bin/10 > bin/train_val_10.out

# Split 11
#
python3 train_val.py --seed 1 --holdouts O-5M --output bin/11 > bin/train_val_11.out

# Split 12
#
python3 train_val.py --seed 1 --holdouts O-5N --output bin/12 > bin/train_val_12.out

# Split 13
#
python3 train_val.py --seed 1 --holdouts O-6M --output bin/13 > bin/train_val_13.out

# Split 14
#
python3 train_val.py --seed 1 --holdouts O-6N --output bin/14 > bin/train_val_14.out

# Split 15
#
python3 train_val.py --seed 1 --holdouts O-7M --output bin/15 > bin/train_val_15.out

# Split 16
#
python3 train_val.py --seed 1 --holdouts O-7N --output bin/16 > bin/train_val_16.out

# Split 17
#
python3 train_val.py --seed 1 --holdouts O-8M --output bin/17 > bin/train_val_17.out

# Split 18
#
python3 train_val.py --seed 1 --holdouts O-8N --output bin/18 > bin/train_val_18.out

# Split 19
#
python3 train_val.py --seed 1 --holdouts O-9M --output bin/19 > bin/train_val_19.out

# Split 20
#
python3 train_val.py --seed 1 --holdouts O-9N --output bin/20 > bin/train_val_20.out


mkdir -p bin

# Split 1
#
python3 train_val.py --seed 1 --holdouts BR01 --output bin/1 > bin/train_val_1.out

# Split 2
#
python3 train_val.py --seed 1 --holdouts BR05 --output bin/2 > bin/train_val_2.out

# Split 3
#
python3 train_val.py --seed 1 --holdouts BR07 --output bin/3 > bin/train_val_3.out

# Split 4
#
python3 train_val.py --seed 1 --holdouts BR13 --output bin/4 > bin/train_val_4.out

# Split 5
#
python3 train_val.py --seed 1 --holdouts BR14 --output bin/5 > bin/train_val_5.out

# Split 6
#
python3 train_val.py --seed 1 --holdouts BR15 --output bin/6 > bin/train_val_6.out

# Split 7
#
python3 train_val.py --seed 1 --holdouts BR16 --output bin/7 > bin/train_val_7.out

# Split 8
#
python3 train_val.py --seed 1 --holdouts BR17 --output bin/8 > bin/train_val_8.out

# Split 9
#
python3 train_val.py --seed 1 --holdouts BR18 --output bin/9 > bin/train_val_9.out

# Split 10
#
python3 train_val.py --seed 1 --holdouts BR19 --output bin/10 > bin/train_val_10.out

# Split 11
#
python3 train_val.py --seed 1 --holdouts BR20 --output bin/11 > bin/train_val_11.out

# Split 12
#
python3 train_val.py --seed 1 --holdouts BR21 --output bin/12 > bin/train_val_12.out

# Split 13
#
python3 train_val.py --seed 1 --holdouts BR22 --output bin/13 > bin/train_val_13.out

# Split 14
#
python3 train_val.py --seed 1 --holdouts BR24 --output bin/14 > bin/train_val_14.out

# Split 15
#
python3 train_val.py --seed 1 --holdouts BR25 --output bin/15 > bin/train_val_15.out

# Split 16
#
python3 train_val.py --seed 1 --holdouts BR26 --output bin/16 > bin/train_val_16.out


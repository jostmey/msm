mkdir -p bin

# Split 1
#
python3 train_val.py --seed 1 --holdouts Patient1 --output bin/1 > bin/train_val.out

# Split 2
#
python3 train_val.py --seed 1 --holdouts Patient2 --output bin/2 > bin/train_val_2.out

# Split 3
#
python3 train_val.py --seed 1 --holdouts Patient3 --output bin/3 > bin/train_val_3.out

# Split 4
#
python3 train_val.py --seed 1 --holdouts Patient4 --output bin/4 > bin/train_val_4.out

# Split 5
#
python3 train_val.py --seed 1 --holdouts Patient5 --output bin/5 > bin/train_val_5.out

# Split 6
#
python3 train_val.py --seed 1 --holdouts Patient6 --output bin/6 > bin/train_val_6.out

# Split 7
#
python3 train_val.py --seed 1 --holdouts Patient7 --output bin/7 > bin/train_val_7.out

# Split 8
#
python3 train_val.py --seed 1 --holdouts Patient8 --output bin/8 > bin/train_val_8.out

# Split 9
#
python3 train_val.py --seed 1 --holdouts Patient9 --output bin/9 > bin/train_val_9.out

# Split 10
#
python3 train_val.py --seed 1 --holdouts Patient10 --output bin/10 > bin/train_val0.out

# Split 11
#
python3 train_val.py --seed 1 --holdouts Patient11 --output bin/11 > bin/train_val1.out

# Split 12
#
python3 train_val.py --seed 1 --holdouts Patient12 --output bin/12 > bin/train_val2.out

# Split 13
#
python3 train_val.py --seed 1 --holdouts Patient13 --output bin/13 > bin/train_val3.out

# Split 14
#
python3 train_val.py --seed 1 --holdouts Patient14 --output bin/14 > bin/train_val4.out


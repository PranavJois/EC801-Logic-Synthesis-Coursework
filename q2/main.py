#main file. 

# get functions imported from bool_func.py
import bool_func as bf

"""
assumptions:
1.file input -> one line of text -> one expression 
2. a ->a, A-> a'
3. seperation using + only and no brackets

representation: done in PCN 

"""

file_name = input("Enter test  file name: ")
exp_no = int(input("Enter which expression to convert to ROBDD: "))
be_split = []

with open(file_name, 'r') as f:
    for i, bool_exp in enumerate(f):
        if (i+1) == exp_no:
            bool_exp = bool_exp.strip()
            be_split = [t.strip() for t in bool_exp.split('+')]

if len(be_split)!=0:
    pass
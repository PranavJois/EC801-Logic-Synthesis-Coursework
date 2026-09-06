#main file. 

# get functions imported from bool_func.py

import bool_func as bf


"""
assumptions:
1.file input -> one line of text -> one expression 
2. a ->a, A-> a'
3. seperation using + only and no brackets
"""

file_name = input("Enter test  file name: ")
exp_no = int(input("Enter which expression to eval: "))

check = int(input("""Do you want to enter 
1. control variable? 
2. control variables?
Enter 1 or 2: """))

if check ==1:
    var = input("Enter control variable: ")
elif check==2:
    vars = input("Enter control variables (together no spaces in the order to be evaluated): ")
else:
    print("Invalid input. Please enter 1 or 2.")
    exit()

be_split = []

with open(file_name, 'r') as f:
    for i, bool_exp in enumerate(f):
        if (i+1) == exp_no:
            bool_exp = bool_exp.strip()
            be_split = [t.strip() for t in bool_exp.split('+')]

if len(be_split)!=0:
    if check == 1:
        if var not in bool_exp.lower():
            print("Control variable not in expression. Cofactors are equal to each other and equal to the original expression.")
        f_v, f_v_bar = bf.cofactor_single(var,be_split,verbose=True)
        f_v = bf.bool_simplify_single(f_v)
        f_v_bar = bf.bool_simplify_single(f_v_bar)
        f_diff = bf.boolean_diff_single(f_v,f_v_bar,True)
        f_consensus = bf.boolean_consensus_single(f_v,f_v_bar,True)
        f_smoothing = bf.boolean_smoothing_single(f_v,f_v_bar,True)
    elif check == 2:
        if not all(v.lower() in bool_exp.lower() for v in vars):
            print("Not all control variables are in the expression.")
        f_cof = bf.cofactor_multi(vars,be_split,verbose=True)
        f_diff = bf.boolean_diff_multi(vars,be_split,True)
        f_consensus = bf.boolean_consensus_multi(vars,be_split,True)
        f_smoothing = bf.boolean_smoothing_multi(vars,be_split,True)
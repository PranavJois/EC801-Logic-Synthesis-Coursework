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
            if check == 1:
                if var not in bool_exp.lower():
                    print("Control variable not in expression. Cofactors are equal to each other and equal to the original expression.")
                be_split = bool_exp.split('+')
                for i in range(len(be_split)):
                    be_split[i] = be_split[i].strip()
            elif check ==2:
                pass

        
if len(be_split)!=0:
    #cofactor
    f_v, f_v_bar = bf.cofactor_single(var,be_split)
    f_v = bf.bool_simplify_single(f_v)
    f_v_bar = bf.bool_simplify_single(f_v_bar)
    print("f_v = ",bf.list_to_exp(f_v))
    print("f_v_bar = ",bf.list_to_exp(f_v_bar))


f_diff = bf.boolean_diff_single(f_v,f_v_bar,True)
f_consensus = bf.boolean_consensus_single(f_v,f_v_bar,True)
f_smoothing = bf.boolean_smoothing_single(f_v,f_v_bar,True)
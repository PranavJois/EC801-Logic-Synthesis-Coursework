import math as m

def simplify_single(be_list,verbose=False):
    out=[]
    if "1" in be_list:
        out = ["1"]
    #boolean exp simplification rules here. demorgan's laws etc
    if verbose:
        print ("check simplified exp = {}",out)
    return out
    

def cofactor_single(var,be_list,verbose=False):
    var_b = var.upper()
    cof_var = []
    cof_var_bar = []
    for i in be_list:
        if (var not in i) and (var_b not in i):
            cof_var.append(i)
            cof_var_bar.append(i)
        elif (var in i):
            if len(i.replace(var,''))==0:
                cof_var.append('1')
            else:
                cof_var.append(i.replace(var,''))
        elif (var_b in i):
            if len(i.replace(var_b,''))==0:
                cof_var_bar.append('1')
            else:
                cof_var_bar.append(i.replace(var_b,''))

    simplify_single(cof_var,True)
    simplify_single(cof_var_bar,True)

    if verbose:
        print("f_var:")
        for i in cof_var:
            print(i,end='+')
        print()
        print("f_var_bar:")
        for i in cof_var_bar:
            print(i,end='+')
        print()

def boolean_diff_single(var,be_list,verbose=False):
    pass

def boolean_consensus_single(var,be_list,verbose=False):
    pass
def boolean_smoothing_single(var,be_list,verbose=False):
    pass
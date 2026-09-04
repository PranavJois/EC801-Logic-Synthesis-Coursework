#SOP form
#eg: list = ['ab','aB','AB'] represents ab + aB + AB
def list_to_exp(list_s):
    for i in list_s[:-1]:
        print(i,end='+')
    print(list_s[-1],end='\n')

def simplify_single(be_list,verbose=False):
    out=[]
    if "1" in be_list:
        out = ["1"]
    #boolean exp simplification rules here. demorgan's laws et
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
        list_to_exp(cof_var)
        print()
        print("f_var_bar:")
        list_to_exp(cof_var_bar)
        print()

def boolean_diff_single(var,be_list,verbose=False):
    pass

def boolean_consensus_single(var,be_list,verbose=False):
    pass
def boolean_smoothing_single(var,be_list,verbose=False):
    pass
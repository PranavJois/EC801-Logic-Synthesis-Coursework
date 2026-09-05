#SOP form
#eg: list = ['ab','aB','AB'] represents ab + aB + AB
def list_to_exp(list_s):
    if len(list_s)==0:
        print("0",end='\n')
    else:  
        for i in list_s[:-1]:
            print(i,end='+')
        print(list_s[-1],end='\n')

def bool_simplify_single(be_list,verbose=False):
    out=list(set(be_list)) #remove redundant terms
    if "1" in out:
        out = ["1"]
    #boolean exp simplification rules here. demorgan's laws etc

    if verbose:
        print ("check simplified exp = ",out)
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

    f_v = bool_simplify_single(cof_var,True)
    f_v_bar = bool_simplify_single(cof_var_bar,True)

    if verbose:
        print("f_var:")
        list_to_exp(f_v)
        print()
        print("f_var_bar:")
        list_to_exp(f_v_bar)
        print()
    return f_v,f_v_bar

def boolean_diff_single(f_v,f_v_bar,verbose=False):
    f=[]
    if verbose:
            print("f_bool_diff:")
            list_to_exp(f)
            print()
    return f

def boolean_consensus_single(f_v,f_v_bar,verbose=False):
    f = []
    if (f_v ==[]) or (f_v_bar == []):
        f = []
    elif f_v == ["1"]:
        f = f_v_bar
    elif f_v_bar == ["1"]:
        f = f_v
    else:
        for i in f_v:
            for j in f_v_bar:
                if i in j:
                    f.append(j) #bc in bcd means bcd should be in
                elif j in i:
                    f.append(i)
    
                
    f = bool_simplify_single(f,False)
    if verbose:
        print("f_consensus:")
        list_to_exp(f)
        print()
    return f

def boolean_smoothing_single(f_v,f_v_bar,verbose=False):
    f = f_v + f_v_bar
    f = list(set(f))
    f = bool_simplify_single(f,False)

    if verbose:
        print("f_smoothing:")
        list_to_exp(f)
        print()
    return f
#SOP form
#eg: list = ['ab','aB','AB'] represents ab + aB + AB
def list_to_exp(list_s):
    if len(list_s)==0:
        print("0",end='\n')
    else:  
        for i in list_s[:-1]:
            print(i,end='+')
        print(list_s[-1],end='\n')


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

    if verbose:
        print("f_var:")
        list_to_exp(cof_var)
        print()
        print("f_var_bar:")
        list_to_exp(cof_var_bar)
        print()
    return cof_var,cof_var_bar

def find_order(be_list,verbose=False):
    """Order to pick variables for the recursive cofactor expansion below.
    Any permutation of the present variables is correctness-safe (it only
    changes recursion shape), so this orders by descending appearance count."""
    counts = {}
    for term in be_list:
        for ch in term:
            if ch.isalpha():
                v = ch.lower()
                counts[v] = counts.get(v, 0) + 1
    order = sorted(counts, key=lambda v: counts[v], reverse=True)
    if verbose:
        print("variable order = ", order)
    return order

def bool_simplify_single(be_list,order=None,verbose=False):
    out = list(set(be_list))              # de-dup
    if len(out) == 0:
        return []
    if "1" in out:
        return ["1"]

    # drop any term containing both a variable and its complement (x,X) -- always 0
    out = [t for t in out if not any(ch.isupper() and ch.lower() in t for ch in t)]
    if len(out) == 0:
        return []

    if order is None:
        order = find_order(out)
    if not order:
        return out

    var = order[0]
    f_v, f_v_bar = cofactor_single(var,out,verbose=False)
    f_v     = bool_simplify_single(f_v,verbose=False)
    f_v_bar = bool_simplify_single(f_v_bar,verbose=False)

    if f_v == f_v_bar:                    # var doesn't matter (covers 0/0, 1/1, and any other tie)
        out = f_v
    elif f_v == []:
        out = [var.upper() if t == '1' else var.upper()+t for t in f_v_bar]
    elif f_v_bar == []:
        out = [var.lower() if t == '1' else var.lower()+t for t in f_v]
    else:
        out = [var.upper() if t == '1' else var.upper()+t for t in f_v_bar]
        out += [var.lower() if t == '1' else var.lower()+t for t in f_v]

    if verbose:
        print ("check simplified exp = ",out)
    return out


def boolean_diff_single(f_v,f_v_bar,verbose=False):
    f_v     = bool_simplify_single(f_v)
    f_v_bar = bool_simplify_single(f_v_bar)
    if f_v == f_v_bar:
        f = []                              # XOR of identical functions is 0
    else:
        order = find_order(f_v + f_v_bar)
        if not order:                       # both sides are constants and differ -> {},1 or 1,{}
            f = ['1']
        else:
            var = order[0]
            g1, g0 = cofactor_single(var, f_v)
            h1, h0 = cofactor_single(var, f_v_bar)
            x1 = boolean_diff_single(g1, h1)
            x0 = boolean_diff_single(g0, h0)
            if x1 == x0:
                f = x1
            else:
                f  = [var.upper() if t == '1' else var.upper()+t for t in x0]
                f += [var.lower() if t == '1' else var.lower()+t for t in x1]
                f  = bool_simplify_single(f)
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
                if set(i).issubset(set(j)):
                    f.append(j) #bc in bcd means bcd should be in
                elif set(j).issubset(set(i)):
                    f.append(i)
    
                
    f = bool_simplify_single(f,verbose=False)
    if verbose:
        print("f_consensus:")
        list_to_exp(f)
        print()
    return f

def boolean_smoothing_single(f_v,f_v_bar,verbose=False):
    f = f_v + f_v_bar
    f = list(set(f))
    f = bool_simplify_single(f,verbose=False)

    if verbose:
        print("f_smoothing:")
        list_to_exp(f)
        print()
    return f
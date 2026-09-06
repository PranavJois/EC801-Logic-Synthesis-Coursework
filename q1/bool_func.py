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
    out = list(set(be_list))  
    if len(out) == 0:
        return []
    if "1" in out:
        return ["1"]

    # drop any term containing both a variable and its complement
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

    if f_v == f_v_bar: # var doesn't matter (covers 0/0, 1/1, and any other tie)
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
        f = []  #xor of identical functions is 0
    else:
        order = find_order(f_v + f_v_bar)
        if not order:   #both sides are constants and differ -> {},1 or 1,{}
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

def and_sop(g,h):
    """AND of two SOP-form functions, via the same recursive cofactor pattern
    used by bool_simplify_single/boolean_diff_single."""
    g = bool_simplify_single(g)
    h = bool_simplify_single(h)
    if g == [] or h == []:
        return []
    if g == ["1"]:
        return h
    if h == ["1"]:
        return g
    order = find_order(g + h)
    if not order:
        return []
    var = order[0]
    g1, g0 = cofactor_single(var,g)
    h1, h0 = cofactor_single(var,h)
    a1 = and_sop(g1,h1)
    a0 = and_sop(g0,h0)
    if a1 == a0:
        return a1
    out  = [var.upper() if t == '1' else var.upper()+t for t in a0]
    out += [var.lower() if t == '1' else var.lower()+t for t in a1]
    return bool_simplify_single(out)

def boolean_consensus_single(f_v,f_v_bar,verbose=False):
    f = and_sop(f_v,f_v_bar)
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

# ---------------------------------------------------------------------------
# Multi-variable versions. var_str follows the same lowercase/uppercase
# convention as SOP terms.
#   - cofactor_multi: var_str is a *signed assignment* (e.g. 'ab' -> a=1,b=1;
#     'aB' -> a=1,b=0), matching ps.txt's own notation.
#   - consensus_multi / smoothing_multi: var_str just names the variables to
#     eliminate -- case doesn't matter, order doesn't matter (universal /
#     existential quantification over the set).
#   - diff_multi: nth-order Boolean difference, f XOR (f with every variable
#     in var_str complemented) -- the standard multi-variable generalization
#     used for simultaneous-fault sensitivity in ATPG.
# ---------------------------------------------------------------------------

def cofactor_multi(var_str,be_list,verbose=False):
    f = be_list
    for ch in var_str:
        var = ch.lower()
        f_v, f_v_bar = cofactor_single(var,f,verbose=False)
        f = f_v if ch.islower() else f_v_bar
        f = bool_simplify_single(f)
    if verbose:
        print(f"f_{var_str}:")
        list_to_exp(f)
        print()
    return f

def boolean_consensus_multi(var_str,be_list,verbose=False):
    f = bool_simplify_single(be_list)
    for ch in set(var_str.lower()):
        f_v, f_v_bar = cofactor_single(ch,f,verbose=False)
        f = boolean_consensus_single(f_v,f_v_bar)
    if verbose:
        print(f"f_consensus_{var_str}:")
        list_to_exp(f)
        print()
    return f

def boolean_smoothing_multi(var_str,be_list,verbose=False):
    f = bool_simplify_single(be_list)
    for ch in set(var_str.lower()):
        f_v, f_v_bar = cofactor_single(ch,f,verbose=False)
        f = boolean_smoothing_single(f_v,f_v_bar)
    if verbose:
        print(f"f_smoothing_{var_str}:")
        list_to_exp(f)
        print()
    return f

def flip_vars(be_list,var_str):
    """Swap the polarity of every variable named in var_str throughout be_list."""
    flip_set = set(var_str.lower())
    out = []
    for term in be_list:
        if term == '1':
            out.append(term); continue
        new_term = ''.join(
            (ch.upper() if ch.islower() else ch.lower()) if ch.lower() in flip_set else ch
            for ch in term
        )
        out.append(new_term)
    return out

def boolean_diff_multi(var_str,be_list,verbose=False):
    f         = bool_simplify_single(be_list)
    f_flipped = bool_simplify_single(flip_vars(f,var_str))
    diff = boolean_diff_single(f,f_flipped)
    if verbose:
        print(f"f_bool_diff_{var_str}:")
        list_to_exp(diff)
        print()
    return diff
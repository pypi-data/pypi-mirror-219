import math
import re
import gvar

def exponent(x):
    return int(math.floor(math.log10(abs(x))))

def int_mantissa(x, n, e):
    return round(x * 10 ** (n - 1 - e))

def naive_ndigits(x, n):
    log10x = math.log10(abs(x))
    n_int = int(math.floor(n))
    n_frac = n - n_int
    log10x_frac = log10x - math.floor(log10x)
    return n_int + (log10x_frac < n_frac)

def ndigits(x, n):
    ndig = naive_ndigits(x, n)
    xexp = exponent(x)
    rounded_x = int_mantissa(x, ndig, xexp) * 10 ** xexp
    if rounded_x > x:
        rounded_ndig = naive_ndigits(rounded_x, n)
        if rounded_ndig > ndig:
            x = rounded_x
            ndig = rounded_ndig
    return x, ndig

def mantissa(x, n, e):
    m = int_mantissa(x, n, e)
    s = str(abs(int(m)))
    assert len(s) == n or len(s) == n + 1 or (m == 0 and n < 0)
    if n >= 1 and len(s) == n + 1:
        e = e + 1
        s = s[:-1]
    return s, e

def insert_dot(s, n, e, addzeros=True):
    e = e + len(s) - n
    n = len(s)
    if e >= n - 1:
        s = s + '0' * (e - n + 1)
    elif e >= 0:
        s = s[:1 + e] + '.' + s[1 + e:]
    elif e <= -1 and addzeros:
        s = '0' * -e + s
        s = s[:1] + '.' + s[1:]
    return s

def tostring(x):
    return '0' if x == 0 else f'{x:#.6g}'

def uformat(mu, s, errdig=2, sep=None, *, shareexp=True, outersign=False, uniexp=False, minnegexp=6, minposexp=4, padzeros=False, possign=False):
    """
    Format a number with uncertainty.
    
    Parameters
    ----------
    mu : number
        The central value.
    s : number
        The error.
    errdig : number
        The number of digits of the error to be shown. Must be >= 1. It can be
        a noninteger, in which case the number of digits switches between the
        lower nearest integer to the upper nearest integer as the first decimal
        digit (after rounding) crosses 10 raised to the fractional part of
        `errdig`. Default 1.5.
    sep : None or str
        The separator put between the central value and the error. Eventual
        spaces must be included. If None, put the error between parentheses,
        sharing decimal places/exponential notation with the central value.
        Default None.
    shareexp : bool
        Applies if sep is not None. When using exponential notation, whether to
        share the exponent between central value and error with outer
        parentheses. Default True.
    outersign : bool
        Applied when sep is not None and shareexp is True. Whether to put the
        sign outside or within the parentheses. Default False
    uniexp : bool
        When using exponential notation, whether to use unicode characters
        instead of the standard ASCII notation. Default False.
    minnegexp : int
        The number of places after the comma at which the notation switches
        to exponential notation. Default 4. The number of places from the
        greater between central value and error is considered.
    minposexp : int
        The power of ten of the least significant digit at which exponential
        notation is used. Default 0. Setting higher values may force padding
        the error with zeros, depending on `errdig`.
    padzeros : bool
        Whether to pad with zeros when not using exponential notation due to
        `minposexp` even if the least significant digits is not on the units.
        Default False, i.e., more digits than those specified
    possign : bool
        Whether to put a `+` before the central value when it is positive.
        Default False.
    """
    if errdig < 1:
        raise ValueError('errdig < 1')
    if not math.isfinite(mu) or not math.isfinite(s) or s <= 0:
        if sep is None:
            return f'{tostring(mu)}({tostring(s)})'
        else:
            return f'{tostring(mu)}{sep}{tostring(s)}'
    
    s, sndig = ndigits(s, errdig)
    sexp = exponent(s)
    muexp = exponent(mu) if mu != 0 else sexp - sndig - 1
    smant, sexp = mantissa(s, sndig, sexp)
    mundig = sndig + muexp - sexp
    mumant, muexp = mantissa(mu, mundig, muexp)
    musign = '-' if mu < 0 else '+' if possign else ''
    
    if mundig >= sndig:
        use_exp = muexp >= mundig + minposexp or muexp <= -minnegexp
        base_exp = muexp
    else:
        use_exp = sexp >= sndig + minposexp or sexp <= -minnegexp
        base_exp = sexp
    
    if use_exp:
        mumant = insert_dot(mumant, mundig, muexp - base_exp)
        smant = insert_dot(smant, sndig, sexp - base_exp, sep is not None)
    elif base_exp >= max(mundig, sndig) and not padzeros:
        mumant = str(abs(round(mu)))
        smant = str(abs(round(s)))
    else:
        mumant = insert_dot(mumant, mundig, muexp)
        smant = insert_dot(smant, sndig, sexp, sep is not None)
    
    if not outersign:
        mumant = musign + mumant
    
    if use_exp:
        if uniexp:
            asc = '0123456789+-'
            uni = '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻'
            table = str.maketrans(asc, uni)
            exp = str(base_exp).translate(table)
            suffix = '×10' + exp
        else:
            suffix = f'e{base_exp:+}'
        if sep is None:
            r = mumant + '(' + smant + ')' + suffix
        elif shareexp:
            r = '(' + mumant + sep + smant + ')' + suffix
        else:
            r = mumant + suffix + sep + smant + suffix
    elif sep is None:
        r = mumant + '(' + smant + ')'
    else:
        r = mumant + sep + smant
    
    if outersign:
        r = musign + r
    
    return r

def check(n, s, string, *args, **kw):
    defaults = dict(minnegexp=2, minposexp=0)
    defaults.update(kw)
    f = uformat(n, s, *args, **defaults)
    if f != string:
        raise RuntimeError(f'{f!r} != {string!r}')

def allchecks():
    check(1, 0.2, "1.00 pm 0.20", 1.5, " pm ")
    check(1, 0.3, "1.00 pm 0.30", 1.5, " pm ")
    check(1, 0.31, "1.00 pm 0.31", 1.5, " pm ")
    check(1, 0.32, "1.0 pm 0.3", 1.5, " pm ")
    check(-1, 0.34, "-1.00 pm 0.34", 2, " pm ")
    check(0, 0, "0 pm 0", 2, " pm ")
    check(123456, 0, "123456. pm 0", 2, " pm ")
    check(12345.6, 0, "12345.6 pm 0", 2, " pm ")
    check(12345.67, 0, "12345.7 pm 0", 2, " pm ")
    check(1e8, 0, "1.00000e+08 pm 0", 2, " pm ")
    check(1e-2, 0, "0.0100000 pm 0", 2, " pm ")
    check(1e-1, 0, "0.100000 pm 0", 2, " pm ")
    check(12345.99, 0, "12346.0 pm 0", 2, " pm ")
    check(0, 0.001, "(0.0 pm 1.0)e-3", 2, " pm ")
    check(0, 0.01, "(0.0 pm 1.0)e-2", 2, " pm ")
    check(0, 0.1, "0.00 pm 0.10", 2, " pm ")
    check(0, 1, "0.0 pm 1.0", 2, " pm ")
    check(0, 10, "0 pm 10", 2, " pm ")
    check(0, 100, "(0.0 pm 1.0)e+2", 2, " pm ")
    check(0, 1000, "(0.0 pm 1.0)e+3", 2, " pm ")
    check(0, 0.0196, "(0.0 pm 2.0)e-2", 2, " pm ")
    check(0, 0.196, "0.00 pm 0.20", 2, " pm ")
    check(0, 1.96, "0.0 pm 2.0", 2, " pm ")
    check(0, 19.6, "0 pm 20", 2, " pm ")
    check(0, 196, "(0.0 pm 2.0)e+2", 2, " pm ")
    check(0, 0.00996, "(0.0 pm 1.0)e-2", 2, " pm ")
    check(0, 0.0996, "0.00 pm 0.10", 2, " pm ")
    check(0, 0.996, "0.0 pm 1.0", 2, " pm ")
    check(0, 9.96, "0 pm 10", 2, " pm ")
    check(0, 99.6, "(0.0 pm 1.0)e+2", 2, " pm ")
    check(0.025, 3, "0.0 pm 3.0", 2, " pm ")
    check(0.0251, 0.3, "0.03 pm 0.30", 2, " pm ")
    check(0.025, 0.03, "(2.5 pm 3.0)e-2", 2, " pm ")
    check(0.025, 0.003, "(2.50 pm 0.30)e-2", 2, " pm ")
    check(0.0025, 0.003, "(2.5 pm 3.0)e-3", 2, " pm ")
    check(0.251, 3, "0.3 pm 3.0", 2, " pm ")
    check(2.5, 3, "2.5 pm 3.0", 2, " pm ")
    check(25, 3, "25.0 pm 3.0", 2, " pm ")
    check(2500, 300, "(2.50 pm 0.30)e+3", 2, " pm ")
    check(1, 0.99, "1.0 pm 1.0", 1.5, " pm ")
    check(math.inf, 1.0, "inf pm 1.00000", 2, " pm ")
    check(-math.inf, 1.0, "-inf pm 1.00000", 2, " pm ")
    check(0, math.inf, "0 pm inf", 2, " pm ")

    check(1, 0.2, "1.00(20)", 1.5, None)
    check(1, 0.3, "1.00(30)", 1.5, None)
    check(1, 0.31, "1.00(31)", 1.5, None)
    check(1, 0.32, "1.0(3)", 1.5, None)
    check(-1, 0.34, "-1.00(34)", 2, None)
    check(0, 0, "0(0)", 2, None)
    check(123456, 0, "123456.(0)", 2, None)
    check(12345.6, 0, "12345.6(0)", 2, None)
    check(12345.67, 0, "12345.7(0)", 2, None)
    check(1e8, 0, "1.00000e+08(0)", 2, None)
    check(1e-2, 0, "0.0100000(0)", 2, None)
    check(1e-1, 0, "0.100000(0)", 2, None)
    check(12345.99, 0, "12346.0(0)", 2, None)
    check(0, 0.001, "0.0(1.0)e-3", 2, None)
    check(0, 0.01, "0.0(1.0)e-2", 2, None)
    check(0, 0.1, "0.00(10)", 2, None)
    check(0, 1, "0.0(1.0)", 2, None)
    check(0, 10, "0(10)", 2, None)
    check(0, 100, "0.0(1.0)e+2", 2, None)
    check(0, 1000, "0.0(1.0)e+3", 2, None)
    check(0, 0.0196, "0.0(2.0)e-2", 2, None)
    check(0, 0.196, "0.00(20)", 2, None)
    check(0, 1.96, "0.0(2.0)", 2, None)
    check(0, 19.6, "0(20)", 2, None)
    check(0, 196, "0.0(2.0)e+2", 2, None)
    check(0, 0.00996, "0.0(1.0)e-2", 2, None)
    check(0, 0.0996, "0.00(10)", 2, None)
    check(0, 0.996, "0.0(1.0)", 2, None)
    check(0, 9.96, "0(10)", 2, None)
    check(0, 99.6, "0.0(1.0)e+2", 2, None)
    check(0.025, 3, "0.0(3.0)", 2, None)
    check(0.0251, 0.3, "0.03(30)", 2, None)
    check(0.025, 0.03, "2.5(3.0)e-2", 2, None)
    check(0.025, 0.003, "2.50(30)e-2", 2, None)
    check(0.0025, 0.003, "2.5(3.0)e-3", 2, None)
    check(0.251, 3, "0.3(3.0)", 2, None)
    check(2.5, 3, "2.5(3.0)", 2, None)
    check(25, 3, "25.0(3.0)", 2, None)
    check(2500, 300, "2.50(30)e+3", 2, None)
    check(1, 0.99, "1.0(1.0)", 1.5, None)
    check(math.inf, 1.0, "inf(1.00000)", 2, None)
    check(-math.inf, 1.0, "-inf(1.00000)", 2, None)
    check(0, math.inf, "0(inf)", 2, None)

class NewGVar(gvar._gvarcore.GVar):
    
    def __init__(self, g):
        self.g = g

    def __format__(self, spec):
        self = self.g
        if not spec:
            return str(self)
        pat = r'([-+#$]*)(\d*\.?\d*)(:\d+)?(p|s|u|U)'
        m = re.fullmatch(pat, spec)
        if not m:
            raise ValueError(f'format specification {spec!r} not understood, format is r"{pat}"')
        kw = {}
        options = m.group(1)
        kw['possign'] = '+' in options
        kw['outersign'] = '-' in options
        kw['padzeros'] = '#' in options
        kw['shareexp'] = '$' not in options
        if m.group(2):
            kw['errdig'] = float(m.group(2))
        else:
            kw['errdig'] = 1.5
        if m.group(3):
            nexp = int(m.group(3)[1:])
        else:
            nexp = 5
        kw['minposexp'] = max(0, nexp - math.floor(kw['errdig']))
        kw['minnegexp'] = nexp
        mode = m.group(4)
        kw['sep'] = dict(p=None, s=' +/- ', u=' ± ', U=' ± ')[mode]
        kw['uniexp'] = mode == 'U'
        return uformat(gvar.mean(self), gvar.sdev(self), **kw)

def gv(*args):
    return NewGVar(gvar.gvar(*args))

def compare(n, s):
    print(f'{gv(n, s)}      {gv(n, s):p}')

if __name__ == '__main__':
    allchecks()

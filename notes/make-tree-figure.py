from fractions import Fraction
import sys

# Continued fraction of |lambda_2| = 0.30366300...
# from A007515: [0; 3, 3, 2, 2, 3, 13, 1, 174, ...]
CF = [0, 3, 3, 2, 2, 3, 13, 1, 174]

def convergents(cf):
    # returns list of Fractions p_n/q_n
    res = []
    for n in range(1, len(cf)):
        # compute p_n/q_n from [a0; a1...a_n]
        num, den = 1, 0
        a = cf[n]
        num2, den2 = a, 1
        for k in range(n-1, 0, -1):
            a = cf[k]
            num2, den2 = a*num2 + num, a*den2 + den
            num, den = num2, den2
        # now num2/den2 = [a1; a2...a_n]  (the tail)
        p, q = num2, den2
        # full convergent [0; a1...a_n] = 1/(num2/den2) = den2/num2
        res.append(Fraction(den2, num2))
    return res

conv = convergents(CF)
print("convergents of |lambda_2|:")
for c in conv:
    print(f"  {c} = {float(c):.6f}")

# Stern-Brocot word of a rational in (0,1): walk from 1/1.
def sb_word(target):
    lo, hi = Fraction(0,1), Fraction(1,1)
    m = Fraction(1,2)  # mediant of 0/1 and 1/1
    word = []
    steps = 0
    while m != target and steps < 10000:
        if target < m:
            word.append('L'); hi = m
        else:
            word.append('R'); lo = m
        m = lo + (hi-lo)  # mediant: (lo.numerator+hi.numerator)/(lo.denominator+hi.denominator)
        # mediant of lo,hi
        m = Fraction(lo.numerator+hi.numerator, lo.denominator+hi.denominator)
        steps += 1
        if steps > 50: break
    return word, m == target

# run-lengths of a word
def runs(word):
    if not word: return []
    r = []
    cur = word[0]; cnt = 1
    for ch in word[1:]:
        if ch == cur: cnt += 1
        else: r.append((cur, cnt)); cur = ch; cnt = 1
    r.append((cur, cnt))
    return r

print("\nSB words and run-lengths vs CF:")
for c in conv:
    w, ok = sb_word(c)
    print(f"  {c}: word {''.join(w)[:25]}{'...' if len(w)>25 else ''} runs={runs(w)}  (finite={ok})")

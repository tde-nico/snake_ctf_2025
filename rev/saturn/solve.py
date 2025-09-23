# pip install z3-solver
from z3 import Ints, Solver, And, Or, sat

# Target derived from later steps in the RPL:
# - After decoding ENC with the weird modulo formula, R must equal uppercase("ArgumentType")
TARGET_R = "ARGUMENTTYPE"

# Solve for ENC (12 uppercase letters) such that ((ord(c)-3) % 26) + ord('A') == TARGET_R[i]
E = [Ints(f"E{i}")[0] for i in range(12)]
s = Solver()
for i, t in enumerate(TARGET_R):
    # uppercase ASCII
    s.add(And(E[i] >= 65, E[i] <= 90))
    # (E[i]-3) mod 26 yields 0..25; add 'A'
    # So ((E[i] - 3) % 26) + 65 == ord(t)
    # z3's mod is non-negative for ints, so this is fine here
    s.add(((E[i] - 3) % 26) + 65 == ord(t))

assert s.check() == sat
m = s.model()
ENC = "".join(chr(m[E[i]].as_long()) for i in range(12))  # -> 'QHWKCUDJJOFU'

# Error-block logic from the RPL:
# DOPATH RCL => ERRN = 516 ("Undefined Name") on HP-48/28 family
# Replacement character is chr(ERRN - 481) = '#'
ERRN = 516
replace_char = chr(ERRN - 481)  # '#'
ERRM = "Undefined Name"         # message text for 516
TFA  = ERRM.replace(" ", replace_char)  # 'Undefined#Name'

flag = f"snakeCTF{{{ENC}{TFA}}}"
print(flag)

# --- Lightweight verifier that mirrors the HP-28S program checks ---
def hp28_chkflg(s):
    # 1) first 5 lowercase that uppercase to 'SNAKE'
    if len(s) >= 5:
        for i in range(5):
            c = s[i]
            if not ('a' <= c <= 'z'):
                return False
            if chr(ord(c) - 32) != "SNAKE"[i]:
                return False
    else:
        return False

    # 2) positions 6..9 are "CTF{"
    if s[5:9] != "CTF{":
        return False

    # 3) last char is '}'
    if s[-1:] != "}":
        return False

    # 4) total length < 37
    if len(s) >= 37:
        return False

    inside = s[9:-1]          # characters 10..len-1 (1-based inclusive)
    ENC2  = inside[:12]       # 1..12
    TFA2  = inside[12:]       # 13..end

    # 5) TFA must have no spaces
    if " " in TFA2:
        return False

    # 6) Build "TFA with magic char replaced by space" and require it equals ERRM
    if TFA2.replace(replace_char, " ") != ERRM:
        return False

    # 7) ENC must be A..Z only
    if not ENC2.isalpha() or ENC2 != ENC2.upper():
        return False

    # 8) Decode ENC with the program's formula and require it equals 'ARGUMENTTYPE'
    R = "".join(chr(((ord(c) - 3) % 26) + ord('A')) for c in ENC2)
    if R != TARGET_R:
        return False

    # 9) The later IFERR ..."Bad Argument Type"... step takes positions 5..17 -> "Argument Type",
    # then removes the space and uppercases -> "ARGUMENTTYPE", which must equal R.
    errm2 = "Bad Argument Type"   # error 514 message on these calcs
    SA = errm2[4:17].replace(" ", "")  # positions 5..17 (1-based) => "Argument Type" -> "ArgumentType"
    RA = SA.upper()                    # -> "ARGUMENTTYPE"
    if RA != R:
        return False

    return True

assert hp28_chkflg(flag)


# snakeCTF{QHWKCUDJJOFUUndefined#Name}

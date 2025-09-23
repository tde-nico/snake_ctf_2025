table = [15, 21, 2, 18, 6, 27, 7, 17, 13, 24, 26, 4, 29, 16, 20, 5, 22, 31, 11, 10, 12, 28, 3, 19, 14, 30, 8, 25, 1, 0, 23, 9]


def small_idx(r9, r10):
    # return ((( (tid ^ 1) * -1 ) + tid + tid) & 7)
    r14 = r9 ^ 1
    # /*00c8*/ // IADD3 R0, -R0, R2, R9 
    r15 = r9 + r10
    r16 = r15 - r14
    r17 = r16 & 7
    return r17    
    # /*00e8*/ // LOP32I.AND R0, R0, 0x7 ;


def invert_kernel(p0, p1_bytes):
    res = []
    for b in range(8):
        e_block = p0[b*32:(b+1)*32]
        s = [0] * 32
        for i in range(32):
            s[table[i]] = e_block[i]
        pt = [0]*32
        for i in range(32):
            tmp = s[i]
            pt[i] = tmp ^ p1_bytes[small_idx(b, i)]
        res += pt
    return res



with open("output.txt") as f:
    enc = bytes.fromhex(f.read())

print(bytes(invert_kernel(enc, b'snakeFTW')))

# nakeCTF{cUd4_thR34d5_unle45hed_f0r_crYpt0_br3akthru_73a91c9b7fa0_parallel_execution_mastery_unlocks_the_encrypted_realm_yes_the_key_has_been_generated_via_an_LLM_guess_which_one_e9cb0c1112985dd6}

def rk_search(string, substring):
    assert len(string) >= len(substring)
    base = 31
    prime = 101
    str_len, sub_len = len(string), len(substring)
    string_hash, substring_hash = hashes(string, substring, base, prime)
    rm = pow(base, sub_len - 1) % prime
    if substring_hash == string_hash and substring == string[0:sub_len]:
        return 0
    for i in range(1, str_len - sub_len + 1):
        string_hash = (string_hash + prime - rm * ord(string[i - 1]) % prime) % prime
        string_hash = (string_hash * base + ord(string[i + sub_len - 1])) % prime
        if string_hash == substring_hash and substring == string[i : i + sub_len]:
            return i
    return -1


def hashes(string, substring, base, prime):
    string_hash = substring_hash = 0
    for i in range(len(substring)):
        string_hash = (base * string_hash + ord(string[i])) % prime
        substring_hash = (base * substring_hash + ord(substring[i])) % prime
    return string_hash, substring_hash

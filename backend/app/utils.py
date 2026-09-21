BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(BASE62_ALPHABET)  # 62


def encode_base62(num: int) -> str:
    """Converts a positive integer ID into a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]

    arr = []
    while num > 0:
        num, rem = divmod(num, BASE)
        arr.append(BASE62_ALPHABET[rem])

    arr.reverse()
    return "".join(arr)


def decode_base62(code: str) -> int:
    """Converts a Base62 string back into its original integer ID."""
    num = 0
    for char in code:
        num = num * BASE + BASE62_ALPHABET.index(char)
    return num 

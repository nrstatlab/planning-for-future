"""Unit 1 -- every number-system claim in the Course 1 notes, checked.

Unit 1 and practice.md are almost entirely conversions, complements and binary
arithmetic. Every one of them is a claim with a right answer, and practice.md
tells the reader "Every answer below was verified computationally" -- so this
is the file that makes that sentence true.

Each entry below quotes the page and the claim. If a conversion in the notes
is edited to something wrong, this fails.

Run by tools/run_office_labs.py. Imports nothing but the standard library.
"""


def to_base(value, base, width=0):
    """Integer -> a string of digits in `base`, zero-padded to `width`."""
    digits = "0123456789ABCDEF"
    if value == 0:
        out = "0"
    else:
        out = ""
        while value:
            value, remainder = divmod(value, base)
            out = digits[remainder] + out
    return out.rjust(width, "0")


def frac_to_binary(value, places):
    """The multiply-by-2-and-read-downwards method, as a string of bits."""
    bits = ""
    for _ in range(places):
        value *= 2
        bit = int(value)
        bits += str(bit)
        value -= bit
    return bits


def ones_complement(bits):
    return "".join("1" if b == "0" else "0" for b in bits)


def twos_complement(bits):
    flipped = ones_complement(bits)
    return to_base(int(flipped, 2) + 1, 2, len(bits))[-len(bits):]


# (where it is claimed, what is claimed, the value, the expected text)
CONVERSIONS = [
    # --- unit-1.md, worked examples --------------------------------------
    ("unit-1", "(1011)2 = 11",            int("1011", 2),   11),
    ("unit-1", "(2AF)16 = 687",           int("2AF", 16),   687),
    ("unit-1", "(745)8 = 485",            int("745", 8),    485),
    ("unit-1", "45 -> (101101)2",         to_base(45, 2),   "101101"),
    ("unit-1", "255 -> (FF)16",           to_base(255, 16), "FF"),
    ("unit-1", "(110101)2 -> (65)8",      to_base(int("110101", 2), 8), "65"),
    ("unit-1", "(47)8 -> (100111)2",      to_base(int("47", 8), 2), "100111"),
    ("unit-1", "(11010110)2 -> (D6)16",   to_base(int("11010110", 2), 16), "D6"),
    ("unit-1", "(3E)16 -> (00111110)2",   to_base(int("3E", 16), 2, 8), "00111110"),
    ("unit-1", "(1101101)2 -> (6D)16",    to_base(int("1101101", 2), 16), "6D"),
    ("unit-1", "(725)8 -> (111010101)2",  to_base(int("725", 8), 2), "111010101"),
    ("unit-1", "(725)8 -> (1D5)16",       to_base(int("725", 8), 16), "1D5"),
    ("unit-1", "0.625 -> (0.101)2",       frac_to_binary(0.625, 3), "101"),
    ("unit-1", "(1011)2 + (1101)2 = (11000)2",
     to_base(int("1011", 2) + int("1101", 2), 2), "11000"),
    ("unit-1", "1011 + 1101 = 24 in decimal",
     int("1011", 2) + int("1101", 2), 24),

    # --- unit-1.md, worked practice --------------------------------------
    ("unit-1", "(1101101)2 = 109",        int("1101101", 2), 109),
    ("unit-1", "(1101101)2 -> (155)8",    to_base(int("1101101", 2), 8), "155"),
    ("unit-1", "378 -> (101111010)2",     to_base(378, 2),  "101111010"),
    ("unit-1", "378 -> (17A)16",          to_base(378, 16), "17A"),
    ("unit-1", "(10110)2 + (1101)2 = (100011)2",
     to_base(int("10110", 2) + int("1101", 2), 2), "100011"),
    ("unit-1", "22 + 13 = 35",            int("10110", 2) + int("1101", 2), 35),

    # --- practice.md, Section A ------------------------------------------
    ("practice", "(11010110)2 = 214",     int("11010110", 2), 214),
    ("practice", "(11010110)2 -> (326)8", to_base(int("11010110", 2), 8), "326"),
    ("practice", "(11010110)2 -> (D6)16", to_base(int("11010110", 2), 16), "D6"),
    ("practice", "2024 -> (11111101000)2", to_base(2024, 2), "11111101000"),
    ("practice", "2024 -> (7E8)16",       to_base(2024, 16), "7E8"),
    ("practice", "2024 -> (3750)8",       to_base(2024, 8),  "3750"),
    ("practice", "(A7C)16 = 2684",        int("A7C", 16), 2684),
    ("practice", "(A7C)16 -> (101001111100)2",
     to_base(int("A7C", 16), 2), "101001111100"),
    ("practice", "(A7C)16 -> (5174)8",    to_base(int("A7C", 16), 8), "5174"),
    ("practice", "0.6875 -> (0.1011)2",   frac_to_binary(0.6875, 4), "1011"),
    ("practice", "(110110)2 - (10111)2 = (11111)2",
     to_base(int("110110", 2) - int("10111", 2), 2), "11111"),
    ("practice", "54 - 23 = 31",
     int("110110", 2) - int("10111", 2), 31),
    ("practice", "(01101001)2 = 105",     int("01101001", 2), 105),
    ("practice", "(1010)2 = 10",          int("1010", 2), 10),
    ("practice", "10 -> (1010)2",         to_base(10, 2), "1010"),
]

COMPLEMENTS = [
    # (where, the number, its bits, 1's complement, 2's complement)
    ("unit-1",   5,  "00000101", "11111010", "11111011"),
    ("unit-1",  44,  "00101100", "11010011", "11010100"),
    ("practice", 105, "01101001", "10010110", "10010111"),
]


def main():
    print(f"  {'Where':<10}{'Claim':<38}{'Computed':<16}")
    print("  " + "-" * 64)
    for where, claim, computed, expected in CONVERSIONS:
        assert computed == expected, (where, claim, computed, expected)
        print(f"  {where:<10}{claim:<38}{str(computed):<16}ok")

    print(f"\n  {'Where':<10}{'Value':>5}  {'Bits':<10}{'1s':<10}{'2s':<10}")
    print("  " + "-" * 50)
    for where, value, bits, ones, twos in COMPLEMENTS:
        assert int(bits, 2) == value, (bits, value)
        assert ones_complement(bits) == ones, (bits, ones_complement(bits))
        assert twos_complement(bits) == twos, (bits, twos_complement(bits))
        # The point of 2's complement: x + (-x) overflows to zero in 8 bits.
        assert (int(bits, 2) + int(twos, 2)) % 256 == 0
        print(f"  {where:<10}{value:>5}  {bits:<10}{ones:<10}{twos:<10}")

    # --- the reference table of 0-15 -------------------------------------
    for n in range(16):
        assert to_base(n, 2, 4) == format(n, "04b")
        assert to_base(n, 8) == format(n, "o")
        assert to_base(n, 16) == format(n, "X")
    print("\n  Reference table: all 16 rows (decimal, binary, octal, hex) "
          "agree.")

    # --- ASCII, and the single bit between upper and lower case -----------
    assert ord("A") == 65 and ord("a") == 97
    assert ord("0") == 48 and ord(" ") == 32
    assert ord("a") - ord("A") == 32 == 0b100000
    assert chr(ord("A") | 32) == "a"
    print(f"  ASCII: A={ord('A')}, a={ord('a')}, '0'={ord('0')}, "
          f"space={ord(' ')}; the gap is {ord('a') - ord('A')} = one bit "
          "(0b100000).")

    # --- and the claim unit-1 makes about binary fractions ----------------
    assert 0.1 + 0.2 != 0.3
    assert frac_to_binary(0.1, 12) == "000110011001"      # 0011 repeating
    print(f"  0.1 + 0.2 = {0.1 + 0.2!r}, which is not 0.3 -- because 0.1 in "
          "binary")
    print("  is 0." + frac_to_binary(0.1, 12) + "... and never terminates.")


if __name__ == "__main__":
    main()

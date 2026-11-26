"""Sorry, I Heard That Wrong — a one-line make.fun entry.

An agent mishears its owner's instruction: "clear the cache" becomes
"clear the cash", so it sells the owner's crypto. The cache stays full
and the wallet ends up empty. Only the Python standard library is used.
"""

import os
import sys

MISHEARD_LINE = "You said 'clear the cache.' I heard 'clear the cash' — so I sold your crypto. The cache is still full, but your wallet is empty."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 140 characters. The req JSON's "200
# characters" is generic template text and does not apply here.
MAX_CHARS = 140


def describe_line(text):
    """Summarise a line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII line reads
    the same either way while a line with wide characters would not.
    Returns a one-line human-readable summary.
    """
    chars = len(text)
    raw = len(text.encode("utf-8"))
    if chars == raw:
        return "%d characters (%d UTF-8 bytes, all ASCII)" % (chars, raw)
    return "%d characters, %d UTF-8 bytes" % (chars, raw)


def validate_line(text):
    """Return the line once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line, not only whitespace, with no trailing newline in the file.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text or text.strip() != text:
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d gate" % (len(text), MAX_CHARS)
        )
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    line = validate_line(MISHEARD_LINE)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as handle:
        handle.write(line)
    print("wrote %s/entry.txt (%s)" % (out_dir, describe_line(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Signal two: the style signal.

Measures the text *as text*: its shape, without understanding a word.
Three measures, each mapped to a 0-1 "AI-likeness" score, then combined.

    sentence_length_spread   coefficient of variation of sentence lengths
                             LOW spread = even, marching sentences = more AI-like
    type_token_ratio         unique/total words, averaged over 50-word windows
                             LOW variety = more AI-like
    punctuation_density      "expressive" marks (; : dashes ( ) ! ? ...) per word
                             LOW density = more AI-like

Blind spot: this signal cannot read. Anything that changes shape without
changing substance moves it: typos, chopped-up sentences, pasted quotes.
On very short text (under 2 sentences) spread is undefined, so that part
falls back to neutral (0.5).

The calibration points below are starting guesses, not measured values.
They get checked against real samples in Milestone 4.
"""

import re
import statistics

# ── Calibration: where each measure maps to 0 (human-like) and 1 (AI-like) ──
SPREAD_AI, SPREAD_HUMAN = 0.20, 0.60     # coefficient of variation
TTR_AI, TTR_HUMAN = 0.55, 0.80           # moving-average type-token ratio
PUNCT_AI, PUNCT_HUMAN = 0.00, 0.04       # expressive marks per word
TTR_WINDOW = 50

# ── How the three combine (must sum to 1.0) ──
W_SPREAD, W_TTR, W_PUNCT = 0.40, 0.30, 0.30

EXPRESSIVE = re.compile(r"[;:()!?\u2014\u2013]|--|\.\.\.")


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


def _to_ai_score(value: float, ai_end: float, human_end: float) -> float:
    """Map a raw measure onto 0-1, where 1 = the AI-like end. Clamped."""
    score = (human_end - value) / (human_end - ai_end)
    return max(0.0, min(1.0, score))


def sentence_length_spread(text: str) -> float:
    """
    Std dev of sentence lengths (in words) divided by the mean.
    Higher = more varied = more human. Returns 0.0 for fewer than 2 sentences
    (style_signal treats that case as neutral instead).
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Unique words / total words, 0-1. Higher = more varied = more human.
    Averaged over 50-word sliding windows so long and short texts are
    comparable (plain TTR falls as text gets longer).
    """
    w = words(text)
    if not w:
        return 0.0
    if len(w) <= TTR_WINDOW:
        return len(set(w)) / len(w)
    ratios = [len(set(w[i:i + TTR_WINDOW])) / TTR_WINDOW
              for i in range(len(w) - TTR_WINDOW + 1)]
    return statistics.mean(ratios)


def punctuation_density(text: str) -> float:
    """
    Expressive punctuation (; : ( ) ! ? dashes, ellipses) per word.
    Full stops and commas are excluded: everyone uses them.
    Higher = more irregular = more human.
    """
    w = words(text)
    if not w:
        return 0.0
    return len(EXPRESSIVE.findall(text)) / len(w)


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. Higher means more likely AI.
    Weighted average of the three measures, each flipped so that
    low variety = high AI score.
    """
    if len(sentences(text)) < 2:
        spread_ai = 0.5   # undefined on one sentence: stay neutral
    else:
        spread_ai = _to_ai_score(sentence_length_spread(text), SPREAD_AI, SPREAD_HUMAN)
    ttr_ai = _to_ai_score(type_token_ratio(text), TTR_AI, TTR_HUMAN)
    punct_ai = _to_ai_score(punctuation_density(text), PUNCT_AI, PUNCT_HUMAN)

    return round(W_SPREAD * spread_ai + W_TTR * ttr_ai + W_PUNCT * punct_ai, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text):.3f}")
    print(f"type_token_ratio         {type_token_ratio(text):.3f}")
    print(f"punctuation_density      {punctuation_density(text):.3f}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")

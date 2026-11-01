"""Milestone 4 calibration: run both signals on four deliberately chosen inputs."""
import detector
import scoring
import stylometry

SAMPLES = {
    "1 clearly AI": (
        "Artificial intelligence is transforming the way we live and work. "
        "It offers many benefits, including increased efficiency and improved "
        "decision-making. However, it also raises important ethical questions "
        "that society must address."
    ),
    "2 clearly human": (
        "ok so I tried the new ramen place last night. honestly? overrated. "
        "the broth was fine I guess but they charged 18 bucks for it — and the "
        "noodles were mushy! never again. anyway, you free saturday?"
    ),
    "3 formal human (mine)": """During my undergraduate studies in Mathematics, I developed a solid foundation in mathematical theory, problem-solving skills, and analytical thinking. My coursework covered a wide range of mathematical disciplines, including advanced calculus, linear algebra, probability theory, and mathematical modeling. These courses equipped me with a rigorous mathematical background that I believe will serve as a strong foundation for my doctoral studies in Mathematical Finance.
My time at Miami University also provided me with opportunities to engage in research projects and independent study. One of my most significant research experiences involved investigating the application of stochastic processes in pricing derivative securities. This project sparked my interest in Mathematical Finance, as I recognized the power of mathematical modeling and quantitative techniques in analyzing and predicting financial markets. This experience further solidified my desire to pursue a Ph.D. in Mathematical Finance to deepen my understanding of these concepts and contribute to the development of innovative financial models.
I am particularly drawn to Boston University's Ph.D. program in Mathematical Finance due to its exceptional faculty, rigorous curriculum, and strong emphasis on both theoretical and applied research. I am excited about the opportunity to work with renowned professors who have made significant contributions to the field. Their expertise and mentorship will undoubtedly enhance my research capabilities and broaden my knowledge in areas such as option pricing, risk management, and portfolio optimization.""",
    "4 lightly-edited AI": (
        "AI is changing how we live and work, honestly faster than most people "
        "expected. It brings real benefits like efficiency and better decisions. "
        "But it raises ethical questions too, and we haven't figured those out yet."
    ),
}

print(f"{'sample':<24}{'model':>8}{'style':>8}{'combined':>10}")
for name, text in SAMPLES.items():
    m = float(detector.model_signal(text))
    s = float(stylometry.style_signal(text))
    c = float(scoring.combine_signals(m, s))
    print(f"{name:<24}{m:>8.3f}{s:>8.3f}{c:>10.3f}")

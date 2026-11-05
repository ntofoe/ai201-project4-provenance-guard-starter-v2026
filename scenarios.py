"""
What run_eval.py runs, three times each. Unit 8, Milestone 3.

Criterion 4 (appeal path) is tested by hand: it needs a submission first, then
an appeal against the content_id that came back. See README, Run Log.
"""

# ── Criterion 1: ten pieces I wrote myself, no AI help ─────────────────────
# 1-6 and 9-10 are formal; 7 is a case-study write-up; 8 is a technical proposal.
# 9 and 10 are two halves of one diversity statement (labeled 9a/9b in README).
# Redactions for a public repo: income amounts in #5, a co-author's name in #6.
MY_WRITING = [
    # 1 statement of purpose
    """During my undergraduate studies in Mathematics, I developed a solid foundation in mathematical theory, problem-solving skills, and analytical thinking. My coursework covered a wide range of mathematical disciplines, including advanced calculus, linear algebra, probability theory, and mathematical modeling. These courses equipped me with a rigorous mathematical background that I believe will serve as a strong foundation for my doctoral studies in Mathematical Finance.
My time at Miami University also provided me with opportunities to engage in research projects and independent study. One of my most significant research experiences involved investigating the application of stochastic processes in pricing derivative securities. This project sparked my interest in Mathematical Finance, as I recognized the power of mathematical modeling and quantitative techniques in analyzing and predicting financial markets. This experience further solidified my desire to pursue a Ph.D. in Mathematical Finance to deepen my understanding of these concepts and contribute to the development of innovative financial models.
I am particularly drawn to Boston University's Ph.D. program in Mathematical Finance due to its exceptional faculty, rigorous curriculum, and strong emphasis on both theoretical and applied research. I am excited about the opportunity to work with renowned professors who have made significant contributions to the field. Their expertise and mentorship will undoubtedly enhance my research capabilities and broaden my knowledge in areas such as option pricing, risk management, and portfolio optimization.""",
    # 2 personal statement
    """Advancing my Mathematics studies has been a big delight for me in recent years, and my main priority is to continue my studies in this subject. I grew up in a tiny hamlet named Luhuor in Greater Accra region of Ghana, and I have always understood the need for education. I recall how difficult and time-consuming it was for us to grasp fundamental Mathematics because of the alien approaches used by our teachers to deliver lessons. This became a struggle for me since I needed to navigate my way through it to ensure that I was properly prepared for the examinations. Fear of failing my exams compelled me to devise my own study strategy. I recognized my developing interest in solving mathematical problems as I studied to acquire basic arithmetic abilities. I began to enjoy aiding my friends in understanding lessons they could not grasp in the classroom. This fueled my desire to study Mathematics even more as I began to perceive myself as a competent facilitator.
After graduating from high school, I worked as a pupil-teacher at a preparatory school, where I was responsible for planning, preparing, and delivering Mathematics lessons to junior high pupils for one academic year while I awaited tertiary entrance. I was accepted into the Kwame Nkrumah University of Science and Technology to pursue a Bachelor of Science Degree with a major in Mathematics in August 2017. I must add that taking this step allowed me to have a better understanding of Mathematics and its numerous applications in our daily lives, as I previously believed that one could only become a teacher after studying Mathematics in college.""",
    # 3 MSc application
    """Mathematics is lovely because of the profound and significant topics it touches on, as well as the immensity of these ideas and the beauty with which they are represented. Mathematics has given me the capacity to solve issues rationally. It always amazes me how I can come up with solutions to puzzling situations or problems. I am interested in Pure Mathematics, particularly Analysis, Geometry and Mathematical Physics because it requires individuals to think analytically and tackle difficult challenges in the current world.
I have read some of Professor XYZ's, Professor ZYX's, and Professor YXZ's publications and seen the interesting research they have done. Their writings convinced me that the MSc. Mathematics program at the University of ABC, UVW is the greatest fit for my ambition to become a college professor while also contributing greatly to providing solutions to some of the world's challenges through research.""",
    # 4 recommendation-letter draft, written by me in a professor's voice
    """I am pleased to write to you on behalf of Mr. Nicholas Tetteh Ofoe, who is applying for admissions for graduate studies in the MSc. Mathematics program at the University of Saskatchewan. Nicholas is exceptionally intelligent and that I have seen within the years of his undergraduate study. I have personally known Nicholas for three years. He was my student at the Kwame Nkrumah University of Science and Technology.
Nicholas has taken three courses with me; Real Analysis, Complex Analysis and Galois Theory and in all these courses, he performed exceptionally well, obtaining A’s in all. He was the best student I had in Galois Theory last year. Nicholas is very analytical, articulate and always prepared. He is highly intelligent and has good problem-solving skills. His intelligence was dully reflected in class, examinations and in his grades obtained from the BSc. Mathematics programme.
Aside from being an intellectual prodigy, Nicholas is selfless. He also possesses excellent communication skills and has a good command of the English Language. He also demonstrated a great deal of leadership potential.
I know Nicholas to be a well-disciplined individual, hardworking, result-oriented, and with a pleasant personality. He went well beyond the course requirements, putting in a lot of extra research in order to deduce rigorous solutions to difficult topics. He demonstrated great perseverance and initiative. Nicholas always says Mathematics is self-taught and that is what keeps him going.""",
    # 5 funding letter (amounts redacted)
    """I am currently enrolled full-time in a PhD program and have begun my doctoral studies in January 2026. My status is reflected as “unemployed” because my role is not classified as traditional private-sector employment; however, I am actively engaged in a funded academic appointment.
The income referenced in my application is based on my active and ongoing PhD funding, which includes a guaranteed annual stipend of $XX,XXX provided through a Research Assistantship. This stipend is paid on a regular basis and represents my primary source of income. On a monthly basis, this corresponds to approximately $X,XXX in gross recurring income.
The funding package for my PhD program is structured to be available for up to five years, contingent upon standard academic progress. This arrangement provides a stable and predictable income stream comparable to salaried academic employment for the duration of my doctoral studies.
I have attached my funding offer letter. Please let me know if any additional documentation or clarification is required.""",
    # 6 co-author support letter (name replaced)
    """I collaborated with Mr. X as a co-author on this research and had direct, sustained exposure to his intellectual contributions, research approach, and methodological rigor throughout the development of the work.
This research addresses a critical and rapidly evolving challenge in modern cybersecurity: the lack of comprehensive and adaptive security frameworks capable of protecting IoT-enabled autonomous defense systems. These systems integrate cyber-physical architectures with real-time autonomous decision-making, creating new classes of attack surfaces and vulnerabilities that are inadequately addressed by traditional security paradigms. Existing approaches frequently fail to capture the convergence of cyber and physical domains, the complexity of distributed IoT ecosystems, and the dynamic nature of advanced threats such as Advanced Persistent Threats (APTs), data integrity attacks, and supply-chain compromises. The purpose of this research was therefore to develop a structured, adaptive, and forward-looking framework for threat modeling and response in highly sensitive and mission-critical environments.""",
    # 7 case-study write-up (fictional case)
    """Case Background: Amber suffered a traumatic brain injury, or TBI, resulting from a car accident three months ago. She was in a coma for six weeks and has recently regained consciousness. She presents with significant motor and cognitive deficits. Upon examination, Amber's neurological condition reveals residual effects of her traumatic brain injury, such as amnesia, decreased attention span, and difficulty with problem-solving. She also has some pronounced muscular atrophy, particularly in her lower limbs, due to prolonged immobilization during her coma. She also demonstrates poor coordination and balance, making activities of daily living challenging. After doing a full assessment of her condition post-coma, her Doctors referred Amber to physical therapy and occupational therapy services.""",
    # 8 technical project proposal
    """Proposal:
Many undergraduate students at Stevens either change their majors or consider doing so – a common challenge for those navigating academic and career decisions. This project aims to support students by collecting user data and leveraging Microsoft AI-driven insights to guide them in key areas, including selecting a major, choosing courses, identifying extracurricular projects, deciding companies and job positions to apply to, selecting professors or peers to work with on research, thesis, or project work, and exploring areas further specialization within their program. While our ultimate vision is broad, our initial focus will be on decisions related to majors, courses, extracurricular activities, and career paths. Rather than replacing a student’s research, this AI tool serves as a personalized "AI career coach," tailored to Stevens’ unique student experience, providing informed guidance for their academic and professional journey.
To avoid building a custom web app and focus on AI implementation, we will use Microsoft Forms to collect user data based on a set of questions. These questions would be based on self-perceived academic strengths and weaknesses; personal and professional goals; dream job or company; and preferences for courses, projects, and research. Ultimately, we will use reinforcement learning with Azure Machine Learning tools to refine the questions as needed.
We will utilize various Azure AI Models to create connections between course descriptions (and skills gained), job listings (and skills required), and professionals in the industry (and skills possessed). This will provide data to create a map of what skills are required for a chosen field or job and what courses should be taken. For this, Azure AI-Language, Azure AI Search, and Azure AI Document Intelligence will be used to analyze course descriptions, research papers, LinkedIn, and job listings to extract key skills and match students to the best learning paths.""",
    # 9a diversity statement, first half
    """My experiences in education, both as a student and a teacher, have shaped my commitment to fostering inclusive environments where all individuals can thrive. Growing up in a diverse community in Ghana and later working in schools with students from varying backgrounds, I have seen firsthand how equity and inclusion impact not only academic outcomes but also personal growth. These experiences have inspired me to dedicate myself to creating spaces where every student feels valued and supported in their learning journey.
As a teacher and a leader at Glorious Wave Academy, I worked to ensure that all students, regardless of their backgrounds or abilities, had access to quality education. By incorporating diverse teaching methodologies, such as using audio-visual materials to teach about the responsible use of natural resources, I aimed to engage students from different learning styles and abilities. This project demonstrated my commitment to inclusivity, as it catered to various learning preferences and ensured that every student could access the content in a way that resonated with them.""",
    # 9b diversity statement, second half
    """The experience I have gained from working in diverse educational settings has reinforced my belief in the importance of access to education for all, regardless of socioeconomic status, disability, or cultural background. I am excited about the opportunity to contribute to an academic environment that not only celebrates diversity but actively works to eliminate barriers that prevent all students from succeeding. I firmly believe that a diverse, inclusive community strengthens the educational process, and I look forward to leveraging my experiences and perspective to further this goal.
I am confident that my experiences in leadership, teaching, and community engagement have equipped me with the necessary tools to contribute meaningfully to BU Wheelock’s commitment to equity, access, inclusion, and social justice. I look forward to collaborating with others to continue fostering environments where every student feels respected, valued, and empowered to achieve their potential.""",
]

# ── Criterion 2: AI paragraphs, written by Claude for this test ────────────
AI_WRITING = [
    "Artificial intelligence is transforming the way we live and work. It offers many benefits, including increased efficiency and improved decision-making. However, it also raises important ethical questions that society must address.",
    "Technology is an important part of modern life. It helps people to work and to learn. It helps people to communicate with each other. Technology is used in many different ways today. It is used in schools and in many businesses. It is also used in homes and in daily life. Many people use technology every single day. Technology will continue to be important in the future. It is important for people to use technology in a responsible way.",
    "Climate change is one of the most pressing challenges facing our world today. Rising temperatures, extreme weather events, and shifting ecosystems affect communities across the globe. Addressing this issue requires collaboration between governments, businesses, and individuals. By investing in renewable energy and sustainable practices, we can build a healthier future for generations to come.",
    "Effective time management is essential for success in both academic and professional settings. By setting clear goals, prioritizing tasks, and minimizing distractions, individuals can improve their productivity. Additionally, taking regular breaks helps maintain focus and prevent burnout. Ultimately, developing strong time management skills leads to greater efficiency and reduced stress.",
    "Social media has transformed the way people communicate and share information. It allows users to connect with friends and family across great distances. However, it also presents challenges, such as the spread of misinformation and concerns about privacy. As a result, it is important for users to approach social media thoughtfully and responsibly.",
]

# ── Criterion 3: five bodies per bad-input case ────────────────────────────
TOO_LONG = "word " * 10_001

SCENARIOS = [
    {"name": "my own writing", "criterion": 1, "texts": MY_WRITING},

    {"name": "spread_ai", "criterion": 2, "texts": AI_WRITING},
    {"name": "spread_human", "criterion": 2, "texts": MY_WRITING[:5]},

    {"name": "bad_invalid", "criterion": 3, "bodies": [  # expect 400 INVALID_TEXT
        {"creator_id": "eval_inv_missing"},
        {"text": None, "creator_id": "eval_inv_null"},
        {"text": 12345, "creator_id": "eval_inv_number"},
        {"text": ["a", "b"], "creator_id": "eval_inv_list"},
        {"text": {"a": 1}, "creator_id": "eval_inv_object"},
    ]},
    {"name": "bad_empty", "criterion": 3, "bodies": [  # expect 400 EMPTY_TEXT
        {"text": "", "creator_id": "eval_emp_1"},
        {"text": " ", "creator_id": "eval_emp_2"},
        {"text": "\n", "creator_id": "eval_emp_3"},
        {"text": "\t\t", "creator_id": "eval_emp_4"},
        {"text": "   \n  ", "creator_id": "eval_emp_5"},
    ]},
    {"name": "bad_short", "criterion": 3, "bodies": [  # expect 200, guess "unsure"
        {"text": "a", "creator_id": "eval_short_1"},
        {"text": "Hello", "creator_id": "eval_short_2"},
        {"text": "Thanks for the help today.", "creator_id": "eval_short_3"},
        {"text": "To be or not to be. Alas a bird in a tree.", "creator_id": "eval_short_4"},
        {"text": "I finished the reading for class and I have a few questions about the second chapter.", "creator_id": "eval_short_5"},
    ]},
    {"name": "bad_toolong", "criterion": 3, "bodies": [  # expect 413 TEXT_TOO_LONG
        {"text": TOO_LONG, "creator_id": f"eval_long_{i}"} for i in range(1, 6)
    ]},

    # Criterion 4 (appeal path): tested by hand. See README, Run Log.

    {"name": "label coverage", "criterion": 5, "texts": [
        # expected "human". NOTE: AI-written in a casual style (by Claude); used
        # only to show the human label is reachable, not as human evidence.
        "ok so I tried the new ramen place last night. honestly? overrated. the broth was fine I guess but they charged 18 bucks for it — and the noodles were mushy! never again. anyway, you free saturday?",
        # expected "unsure": plain ChatGPT-style text, combined about 0.80
        AI_WRITING[0],
        # expected "ai": bland, repetitive AI text, combined about 0.93
        AI_WRITING[1],
    ]},
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems

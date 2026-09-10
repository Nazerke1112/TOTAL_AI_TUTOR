import streamlit as st
import ast

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TOTAL AI TUTOR",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* =====================================================
       GLOBAL FONT
       ===================================================== */

    html, body, [class*="css"] {
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .stApp {
        font-family: "Segoe UI", Arial, sans-serif !important;
        background: linear-gradient(
            135deg,
            #f5f7ff 0%,
            #eef2ff 50%,
            #f8f9ff 100%
        );
    }

    /* Барлық негізгі мәтін */
  .stApp p,
  .stApp span,
  .stApp label,
  .stApp h1,
  .stApp h2,
  .stApp h3,
  .stApp h4,
  .stApp h5,
  .stApp h6 {
    font-family: "Segoe UI", Arial, sans-serif !important;
    color: #000000 !important;
}

/* Басты бет бөлім атаулары */
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3 {
    color: #000000 !important;
    font-family: "Segoe UI", Arial, sans-serif !important;
}
    }

    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827 0%,
            #1e1b4b 100%
        );
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        padding: 35px;
        border-radius: 25px;
        background: linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed,
            #9333ea
        );
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 15px 40px rgba(79, 70, 229, 0.25);
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .hero h1 {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 8px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .hero p {
        font-size: 18px;
        opacity: 0.92;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       STAT CARD
       ===================================================== */

    .stat-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.07);
        text-align: center;
        min-height: 130px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .stat-icon {
        font-size: 30px;
        font-family: "Segoe UI Emoji", "Segoe UI", sans-serif !important;
    }

    .stat-number {
        font-size: 28px;
        font-weight: 700;
        color: #4f46e5;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .stat-title {
        color: #6b7280;
        font-size: 14px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       COURSE CARD
       ===================================================== */

    .course-card {
        background: white;
        padding: 22px;
        border-radius: 20px;
        min-height: 210px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.07);
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .course-icon {
        font-size: 42px;
    }

    .course-title {
        font-size: 21px;
        font-weight: 700;
        color: #111827;
        margin-top: 8px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .course-description {
        color: #6b7280;
        font-size: 14px;
        margin-top: 8px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       LESSON HEADER
       ===================================================== */

    .lesson-header {
        background: linear-gradient(
            135deg,
            #eef2ff,
            #f5f3ff
        );
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .lesson-header h1,
    .lesson-header h2,
    .lesson-header p {
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       THEORY BOX
       ===================================================== */

    .theory-box {
        background: white;
        padding: 25px;
        border-radius: 18px;
        border-left: 5px solid #6366f1;
        box-shadow: 0 6px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .theory-box * {
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       TASK BOX
       ===================================================== */

    .task-box {
        background: #fffbeb;
        padding: 22px;
        border-radius: 18px;
        border-left: 5px solid #f59e0b;
        margin-bottom: 20px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .task-box * {
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       SUCCESS BOX
       ===================================================== */

    .success-box {
        background: #ecfdf5;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #10b981;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .success-box * {
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       AI BOX
       ===================================================== */

    .ai-box {
        background: linear-gradient(
            135deg,
            #eef2ff,
            #faf5ff
        );
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #ddd6fe;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .ai-box * {
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       ACHIEVEMENT
       ===================================================== */

    .achievement {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
        margin-bottom: 15px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    .achievement-icon {
        font-size: 35px;
    }

    .small-text {
        color: #6b7280;
        font-size: 13px;
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       STREAMLIT INPUTS
       ===================================================== */

    textarea,
    input,
    button,
    select {
        font-family: "Segoe UI", Arial, sans-serif !important;
    }

    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton button {
        font-family: "Segoe UI", Arial, sans-serif !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_course" not in st.session_state:
    st.session_state.selected_course = 0

if "selected_lesson" not in st.session_state:
    st.session_state.selected_lesson = 0

if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = 0

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "streak" not in st.session_state:
    st.session_state.streak = 1

if "completed_courses" not in st.session_state:
    st.session_state.completed_courses = []

# =========================================================
# COURSE DATA
# =========================================================

courses = [
    {
        "title": "Python негіздері",
        "icon": "🐍",
        "description": "Python тіліне алғашқы қадам",
        "lessons": [
            {
                "title": "Python дегеніміз не?",
                "theory": [
                    "Python — жоғары деңгейлі, үйренуге жеңіл бағдарламалау тілі.",
                    "Python синтаксисі қарапайым және оқуға ыңғайлы.",
                    "Python веб-әзірлеу, деректерді талдау, жасанды интеллект, автоматтандыру және білім беру салаларында қолданылады."
                ],
                "example": "print('Сәлем, Python!')",
                "task": "Экранға Hello Python! мәтінін шығаратын бағдарлама жазыңыз."
            },
            {
                "title": "print() функциясы",
                "theory": [
                    "print() функциясы ақпаратты экранға шығару үшін қолданылады.",
                    "Мәтін тырнақшаға алынады.",
                    "Бірнеше мәнді print() арқылы қатар шығаруға болады."
                ],
                "example": "print('Мен Python үйреніп жатырмын')\nprint(10)",
                "task": "Өз атыңызды және жасыңызды экранға шығарыңыз."
            },
            {
                "title": "Python операторлары",
                "theory": [
                    "Арифметикалық операторлар есептеулер жүргізеді.",
                    "+ қосу, - азайту, * көбейту, / бөлу амалдарын орындайды.",
                    "** дәрежеге шығару үшін қолданылады."
                ],
                "example": "a = 10\nb = 3\nprint(a + b)\nprint(a * b)",
                "task": "20 және 5 сандарының қосындысын, айырмасын және көбейтіндісін есептеңіз."
            }
        ]
    },
    {
        "title": "Айнымалылар және типтер",
        "icon": "📦",
        "description": "Деректерді сақтау және пайдалану",
        "lessons": [
            {
                "title": "Айнымалы дегеніміз не?",
                "theory": [
                    "Айнымалы — белгілі бір мәнді сақтайтын атаулы орын.",
                    "Python тілінде айнымалыны алдын ала жариялау қажет емес.",
                    "Мысалы: age = 15."
                ],
                "example": "name = 'Aruzhan'\nage = 15\nprint(name)\nprint(age)",
                "task": "name, age және city атты үш айнымалы құрып, олардың мәндерін шығарыңыз."
            },
            {
                "title": "Деректер типтері",
                "theory": [
                    "int — бүтін сан.",
                    "float — нақты сан.",
                    "str — мәтін.",
                    "bool — логикалық мән: True немесе False."
                ],
                "example": "age = 16\nheight = 1.72\nname = 'Ali'\nstudent = True",
                "task": "Бүтін сан, нақты сан, мәтін және логикалық мән сақтайтын төрт айнымалы құрыңыз."
            }
        ]
    },
    {
        "title": "Шартты операторлар",
        "icon": "🔀",
        "description": "Шарт бойынша шешім қабылдау",
        "lessons": [
            {
                "title": "if операторы",
                "theory": [
                    "if операторы шартты тексеру үшін қолданылады.",
                    "Егер шарт True болса, оның ішіндегі код орындалады.",
                    "Шарт салыстыру операторларымен жазылады: >, <, >=, <=, ==, !=."
                ],
                "example": "age = 18\n\nif age >= 18:\n    print('Кәмелетке толған')",
                "task": "Санның оң сан екенін анықтайтын бағдарлама жазыңыз."
            },
            {
                "title": "if және else",
                "theory": [
                    "else — if шарты орындалмаған кезде қолданылатын блок.",
                    "if және else арқылы екі түрлі жағдайды өңдеуге болады."
                ],
                "example": "number = 7\n\nif number % 2 == 0:\n    print('Жұп')\nelse:\n    print('Тақ')",
                "task": "Берілген санның жұп немесе тақ екенін анықтаңыз."
            }
        ]
    },
    {
        "title": "Циклдер",
        "icon": "🔄",
        "description": "Қайталанатын әрекеттерді автоматтандыру",
        "lessons": [
            {
                "title": "for циклі",
                "theory": [
                    "for циклі белгілі бір әрекетті бірнеше рет қайталау үшін қолданылады.",
                    "range() функциясы сандар диапазонын құрады."
                ],
                "example": "for i in range(5):\n    print(i)",
                "task": "1-ден 10-ға дейінгі сандарды экранға шығарыңыз."
            },
            {
                "title": "while циклі",
                "theory": [
                    "while циклі шарт True болғанша қайталанады.",
                    "Цикл ішінде шарттың өзгеруі маңызды."
                ],
                "example": "i = 1\nwhile i <= 5:\n    print(i)\n    i += 1",
                "task": "1-ден 5-ке дейінгі сандарды while арқылы шығарыңыз."
            }
        ]
    },
    {
        "title": "Тізімдер және массивтер",
        "icon": "📊",
        "description": "Бірнеше деректі бірге сақтау",
        "lessons": [
            {
                "title": "List дегеніміз не?",
                "theory": [
                    "List бірнеше мәнді бір айнымалыда сақтауға мүмкіндік береді.",
                    "Тізім квадрат жақшамен жазылады.",
                    "Мысалы: numbers = [1, 2, 3, 4]."
                ],
                "example": "numbers = [10, 20, 30, 40]\nprint(numbers)\nprint(numbers[0])",
                "task": "5 оқушының бағасын сақтайтын тізім құрыңыз."
            },
            {
                "title": "Тізім элементтерімен жұмыс",
                "theory": [
                    "append() тізімге жаңа элемент қосады.",
                    "len() элементтер санын анықтайды.",
                    "sum() сандардың қосындысын есептейді."
                ],
                "example": "numbers = [10, 20, 30]\nnumbers.append(40)\nprint(len(numbers))\nprint(sum(numbers))",
                "task": "Сандар тізімінің қосындысын және элементтер санын табыңыз."
            }
        ]
    },
    {
        "title": "Функциялар",
        "icon": "⚙️",
        "description": "Кодты қайта пайдалану",
        "lessons": [
            {
                "title": "Функция құру",
                "theory": [
                    "Функция — белгілі бір әрекетті орындайтын код бөлігі.",
                    "Python тілінде функция def кілттік сөзі арқылы құрылады."
                ],
                "example": "def hello():\n    print('Сәлем!')\n\nhello()",
                "task": "Сәлемдесу хабарламасын шығаратын функция жазыңыз."
            },
            {
                "title": "Параметрлер",
                "theory": [
                    "Функция параметр қабылдай алады.",
                    "Параметр арқылы функцияға сырттан мән беруге болады."
                ],
                "example": "def square(x):\n    return x * x\n\nprint(square(5))",
                "task": "Санның квадратын қайтаратын функция құрыңыз."
            }
        ]
    },
    {
        "title": "Алгоритмдер",
        "icon": "🧠",
        "description": "Есепті тиімді шешу",
        "lessons": [
            {
                "title": "Алгоритм ұғымы",
                "theory": [
                    "Алгоритм — есепті шешуге арналған нақты қадамдар тізбегі.",
                    "Жақсы алгоритм түсінікті, нақты және нәтижеге бағытталған болуы керек."
                ],
                "example": "1. Сан енгізу\n2. Санның квадратын есептеу\n3. Нәтижені шығару",
                "task": "Екі санның үлкенін табу алгоритмін жазыңыз."
            },
            {
                "title": "Күрделілік туралы түсінік",
                "theory": [
                    "Алгоритмнің тиімділігі оның уақыт және жады шығынымен байланысты.",
                    "O(n) — деректер саны артқан сайын орындалу уақыты шамамен сызықты өседі."
                ],
                "example": "numbers = [1, 2, 3, 4, 5]\nfor x in numbers:\n    print(x)",
                "task": "Тізімдегі барлық элементтерді бір рет қарап шығатын алгоритм жазыңыз."
            }
        ]
    },
    {
        "title": "Python жобалары",
        "icon": "🚀",
        "description": "Білімді нақты жобада қолдану",
        "lessons": [
            {
                "title": "Калькулятор жобасы",
                "theory": [
                    "Жоба барысында енгізу, айнымалы, шарт және арифметикалық операторларды біріктіреміз.",
                    "input() пайдаланушыдан ақпарат алуға мүмкіндік береді."
                ],
                "example": "a = float(input('a = '))\nb = float(input('b = '))\nprint('Қосынды:', a + b)",
                "task": "Екі санды қабылдап, олардың қосындысын шығаратын шағын бағдарлама жасаңыз."
            },
            {
                "title": "Баға анықтау жобасы",
                "theory": [
                    "Бұл жобада шартты операторлар қолданылады.",
                    "Оқушы енгізген баллға сәйкес нәтиже шығарылады."
                ],
                "example": "score = int(input('Балл: '))\n\nif score >= 90:\n    print('Өте жақсы')\nelif score >= 70:\n    print('Жақсы')\nelse:\n    print('Толықтыру қажет')",
                "task": "Оқушының бағасын баллына қарай анықтайтын бағдарлама құрыңыз."
            }
        ]
    }
]

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def syntax_check(code):
    if not code.strip():
        return False, "Код енгізілмеді."

    try:
        ast.parse(code)
        return True, "Синтаксистік қате табылған жоқ."
    except SyntaxError as e:
        return False, f"Синтаксистік қате: {e.msg}. Жол: {e.lineno}"


def ai_response(question):
    q = question.lower()

    if "print" in q:
        return "print() функциясы ақпаратты экранға шығару үшін қолданылады."

    if "if" in q:
        return "if операторы шартты тексеру үшін қолданылады. Мысалы: if age >= 18:"

    if "for" in q:
        return "for циклі белгілі бір әрекетті қайталау үшін қолданылады. Мысалы: for i in range(5):"

    if "while" in q:
        return "while циклі берілген шарт True болған кезде қайталанады."

    if "list" in q or "тізім" in q:
        return "Python тіліндегі list бірнеше мәнді бір жерде сақтайды. Мысалы: numbers = [1, 2, 3]."

    if "function" in q or "функция" in q:
        return "Функция def арқылы құрылады. Ол кодты қайта пайдалануға мүмкіндік береді."

    if "error" in q or "қате" in q:
        return "Кодтағы қатені табу үшін алдымен жақшаларды, қос нүктені, шегіністі және айнымалы атауларын тексеріңіз."

    return "Жақсы сұрақ! Алдымен есептің шартын шағын қадамдарға бөліп алыңыз. Содан кейін қандай айнымалылар, шарттар немесе циклдер қажет екенін анықтаңыз."


def go_to(page):
    st.session_state.page = page


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🤖 TOTAL AI")
    st.markdown("## TUTOR")
    st.markdown("---")

    if st.button(
        "🏠  Басты бет",
        use_container_width=True
    ):
        go_to("home")

    if st.button(
        "📚  Python курстары",
        use_container_width=True
    ):
        go_to("courses")

    if st.button(
        "💻  Практика",
        use_container_width=True
    ):
        go_to("practice")

    if st.button(
        "🤖  AI Tutor",
        use_container_width=True
    ):
        go_to("ai")

    if st.button(
        "🏆  Менің прогресім",
        use_container_width=True
    ):
        go_to("progress")

    st.markdown("---")

    st.markdown("### 👨‍🎓 Оқушы")
    st.write("Python үйрену режимі")

    st.markdown("---")

    st.caption("TOTAL AI TUTOR")
    st.caption("Python + AI Education")


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.markdown(
        '<div class="hero">'
        '<h1>🤖 TOTAL AI TUTOR</h1>'
        '<p>Python бағдарламалауын AI көмегімен үйренуге арналған интеллектуалды білім беру платформасы</p>'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            '<div class="stat-card">'
            '<div class="stat-icon">📚</div>'
            '<div class="stat-number">8</div>'
            '<div class="stat-title">Python курсы</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="stat-card">'
            '<div class="stat-icon">✅</div>'
            f'<div class="stat-number">{st.session_state.completed_lessons}</div>'
            '<div class="stat-title">Орындалған сабақ</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            '<div class="stat-card">'
            '<div class="stat-icon">⭐</div>'
            f'<div class="stat-number">{st.session_state.xp}</div>'
            '<div class="stat-title">XP ұпайы</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            '<div class="stat-card">'
            '<div class="stat-icon">🔥</div>'
            f'<div class="stat-number">{st.session_state.streak}</div>'
            '<div class="stat-title">Күндік серия</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("## 🚀 Python үйренуді бастаңыз")

    total_lessons = sum(
        len(c["lessons"])
        for c in courses
    )

    progress = (
        st.session_state.completed_lessons / total_lessons
        if total_lessons > 0
        else 0
    )

    st.write(
        f"Жалпы прогресс: **{int(progress * 100)}%**"
    )

    st.progress(progress)

    st.markdown("## 📚 Курстар")

    for row_start in range(0, len(courses), 2):

        cols = st.columns(2)

        for j in range(2):

            index = row_start + j

            if index >= len(courses):
                continue

            course = courses[index]

            with cols[j]:

                st.markdown(
                    f'<div class="course-card">'
                    f'<div class="course-icon">{course["icon"]}</div>'
                    f'<div class="course-title">{course["title"]}</div>'
                    f'<div class="course-description">{course["description"]}</div>'
                    f'<p>📖 {len(course["lessons"])} сабақ</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                if st.button(
                    "Курсты бастау →",
                    key=f"home_course_{index}",
                    use_container_width=True
                ):

                    st.session_state.selected_course = index
                    st.session_state.selected_lesson = 0
                    st.session_state.page = "courses"

                    st.rerun()


# =========================================================
# COURSES PAGE
# =========================================================

elif st.session_state.page == "courses":

    st.title("📚 Python курстары")

    course_names = [
        f'{c["icon"]} {c["title"]}'
        for c in courses
    ]

    selected = st.selectbox(
        "Курсты таңдаңыз",
        range(len(courses)),
        format_func=lambda x: course_names[x],
        index=st.session_state.selected_course
    )

    st.session_state.selected_course = selected

    course = courses[selected]

    st.markdown(
        f'<div class="lesson-header">'
        f'<h1>{course["icon"]} {course["title"]}</h1>'
        f'<p>{course["description"]}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    lesson_names = [
        f'{i + 1}. {lesson["title"]}'
        for i, lesson in enumerate(course["lessons"])
    ]

    lesson_index = st.selectbox(
        "Сабақты таңдаңыз",
        range(len(course["lessons"])),
        format_func=lambda x: lesson_names[x],
        index=min(
            st.session_state.selected_lesson,
            len(course["lessons"]) - 1
        )
    )

    st.session_state.selected_lesson = lesson_index

    lesson = course["lessons"][lesson_index]

    st.markdown(
        f'<div class="lesson-header">'
        f'<h2>📖 {lesson["title"]}</h2>'
        f'<p>Сабақ {lesson_index + 1} / {len(course["lessons"])}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    # THEORY

    st.markdown("## 📘 Теория")

    theory_text = "<br><br>".join(
        [
            f"<b>{i + 1}.</b> {text}"
            for i, text in enumerate(lesson["theory"])
        ]
    )

    st.markdown(
        f'<div class="theory-box">{theory_text}</div>',
        unsafe_allow_html=True
    )

    # EXAMPLE

    st.markdown("## 💡 Мысал")

    st.code(
        lesson["example"],
        language="python"
    )

    # TASK

    st.markdown("## 🎯 Практикалық тапсырма")

    st.markdown(
        f'<div class="task-box">'
        f'<h3>📝 Тапсырма</h3>'
        f'<p>{lesson["task"]}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    # CODE EDITOR

    st.markdown("## 💻 Код редакторы")

    code = st.text_area(
        "Python кодын осы жерге жазыңыз:",
        height=250,
        placeholder="# Python кодын жазыңыз\nprint('Hello Python!')",
        key=f"editor_{selected}_{lesson_index}"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔍 Кодты тексеру",
            use_container_width=True
        ):

            valid, message = syntax_check(code)

            if valid:
                st.success(message)
            else:
                st.error(message)

    with col2:

        if st.button(
            "🤖 AI көмегін алу",
            use_container_width=True
        ):

            st.session_state.page = "ai"

            st.session_state.ai_question = (
                f"Мен {lesson['title']} сабағындағы "
                f"тапсырманы орындап жатырмын: "
                f"{lesson['task']}"
            )

            st.rerun()

    # NAVIGATION

    st.markdown("---")

    nav1, nav2, nav3 = st.columns(3)

    with nav1:

        if lesson_index > 0:

            if st.button(
                "⬅️ Алдыңғы сабақ",
                use_container_width=True
            ):

                st.session_state.selected_lesson -= 1
                st.rerun()

    with nav2:

        if st.button(
            "✅ Сабақты аяқтау",
            use_container_width=True
        ):

            st.session_state.completed_lessons += 1
            st.session_state.xp += 10

            st.success(
                "🎉 Сабақ аяқталды! +10 XP"
            )

    with nav3:

        if lesson_index < len(course["lessons"]) - 1:

            if st.button(
                "Келесі сабақ ➡️",
                use_container_width=True
            ):

                st.session_state.selected_lesson += 1
                st.rerun()


# =========================================================
# PRACTICE PAGE
# =========================================================

elif st.session_state.page == "practice":

    st.title("💻 Python практикасы")

    st.write(
        "Мұнда Python есептерін өз бетіңізше орындап, "
        "кодтың синтаксисін тексере аласыз."
    )

    practice_tasks = [
        {
            "title": "🟢 1-есеп. Үш сан",
            "text": "Үш сан берілген. Олардың қосындысын табыңыз."
        },
        {
            "title": "🟡 2-есеп. Жұп немесе тақ",
            "text": "Берілген санның жұп немесе тақ екенін анықтаңыз."
        },
        {
            "title": "🟡 3-есеп. Ең үлкен сан",
            "text": "Үш санның ішінен ең үлкенін анықтаңыз."
        },
        {
            "title": "🔴 4-есеп. Факториал",
            "text": "Берілген n санының факториалын цикл арқылы есептеңіз."
        },
        {
            "title": "🔴 5-есеп. Тізім",
            "text": "Тізімдегі ең үлкен және ең кіші элементті табыңыз."
        }
    ]

    task_index = st.selectbox(
        "Есепті таңдаңыз",
        range(len(practice_tasks)),
        format_func=lambda x: practice_tasks[x]["title"]
    )

    task = practice_tasks[task_index]

    st.markdown(
        f'<div class="task-box">'
        f'<h2>{task["title"]}</h2>'
        f'<p>{task["text"]}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    practice_code = st.text_area(
        "Кодыңызды жазыңыз:",
        height=300,
        key=f"practice_{task_index}"
    )

    if st.button(
        "🔍 Синтаксисті тексеру",
        use_container_width=True
    ):

        valid, message = syntax_check(practice_code)

        if valid:
            st.success(message)
            st.balloons()
        else:
            st.error(message)


# =========================================================
# AI TUTOR PAGE
# =========================================================

elif st.session_state.page == "ai":

    st.title("🤖 AI Tutor")

    st.markdown(
        '<div class="ai-box">'
        '<h2>🧠 Сіздің жеке Python көмекшіңіз</h2>'
        '<p>Python тақырыптары, код қателері және алгоритмдер бойынша сұрақ қойыңыз.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 💬 Сұрағыңызды жазыңыз")

    default_question = st.session_state.get(
        "ai_question",
        ""
    )

    question = st.text_area(
        "Сұрақ:",
        value=default_question,
        height=150,
        placeholder="Мысалы: if операторы қалай жұмыс істейді?"
    )

    if st.button(
        "🤖 AI Tutor-дан жауап алу",
        use_container_width=True
    ):

        if question.strip():

            answer = ai_response(question)

            st.markdown(
                '<div class="success-box">'
                f'<h3>🤖 AI Tutor:</h3>'
                f'<p>{answer}</p>'
                '</div>',
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "Алдымен сұрақ жазыңыз."
            )

    st.markdown("---")

    st.markdown("### 💡 Мысал сұрақтар")

    examples = [
        "Python дегеніміз не?",
        "if операторы қалай жұмыс істейді?",
        "for циклі қалай жазылады?",
        "List дегеніміз не?",
        "Функцияны қалай құрамын?",
        "Кодтағы қатені қалай табуға болады?"
    ]

    for example in examples:

        if st.button(
            example,
            key=f"ai_example_{example}",
            use_container_width=True
        ):

            st.session_state.ai_question = example
            st.rerun()


# =========================================================
# PROGRESS PAGE
# =========================================================

elif st.session_state.page == "progress":

    st.title("🏆 Менің прогресім")

    total_lessons = sum(
        len(c["lessons"])
        for c in courses
    )

    progress = (
        st.session_state.completed_lessons / total_lessons
        if total_lessons > 0
        else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "⭐ XP",
            st.session_state.xp
        )

    with col2:

        st.metric(
            "📚 Сабақтар",
            st.session_state.completed_lessons
        )

    with col3:

        st.metric(
            "🔥 Серия",
            f'{st.session_state.streak} күн'
        )

    st.markdown("## 📈 Жалпы прогресс")

    st.progress(progress)

    st.write(
        f"Сіз **{st.session_state.completed_lessons} / "
        f"{total_lessons}** сабақты аяқтадыңыз."
    )

    st.markdown("## 📚 Курстар бойынша")

    for course in courses:

        course_progress = 0

        st.markdown(
            f"### {course['icon']} {course['title']}"
        )

        st.progress(course_progress)

        st.caption(
            f"0 / {len(course['lessons'])} сабақ"
        )

    st.markdown("## 🏅 Жетістіктер")

    achievements = [
        (
            "🐣",
            "Алғашқы қадам",
            "Бірінші сабақты аяқтаңыз"
        ),
        (
            "🔥",
            "Белсенді оқушы",
            "5 сабақ аяқтаңыз"
        ),
        (
            "⭐",
            "Python бастаушы",
            "50 XP жинаңыз"
        ),
        (
            "🚀",
            "Python зерттеушісі",
            "10 сабақ аяқтаңыз"
        )
    ]

    for icon, title, description in achievements:

        st.markdown(
            f'<div class="achievement">'
            f'<span class="achievement-icon">{icon}</span>'
            f'<b>{title}</b>'
            f'<p class="small-text">{description}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
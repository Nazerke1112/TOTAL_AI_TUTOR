import streamlit as st
import ast
import subprocess
import sys
from urllib.parse import urlparse, parse_qs

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
# CSS DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f5f7ff 0%,
        #eef2ff 50%,
        #f8f9ff 100%
    );
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827 0%,
        #1e1b4b 100%
    );
}

[data-testid="stSidebar"] * {
    color: white !important;
}

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
    box-shadow: 0 15px 40px rgba(79,70,229,0.25);
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    opacity: 0.94;
}

.stat-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.07);
    text-align: center;
    min-height: 130px;
}

.stat-icon {
    font-size: 30px;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #4f46e5;
}

.stat-title {
    color: #6b7280;
    font-size: 14px;
}

.course-card {
    background: white;
    padding: 22px;
    border-radius: 20px;
    min-height: 220px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.07);
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
}

.course-icon {
    font-size: 42px;
}

.course-title {
    font-size: 21px;
    font-weight: 700;
    color: #111827;
    margin-top: 8px;
}

.course-description {
    color: #6b7280;
    font-size: 14px;
    margin-top: 8px;
}

.lesson-header {
    background: linear-gradient(
        135deg,
        #eef2ff,
        #f5f3ff
    );
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
}

.theory-box {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border-left: 5px solid #6366f1;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.task-box {
    background: #fffbeb;
    padding: 22px;
    border-radius: 18px;
    border-left: 5px solid #f59e0b;
    margin-bottom: 20px;
}

.success-box {
    background: #ecfdf5;
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #10b981;
}

.error-box {
    background: #fef2f2;
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #ef4444;
}

.ai-box {
    background: linear-gradient(
        135deg,
        #eef2ff,
        #faf5ff
    );
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #ddd6fe;
}

.achievement {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}

.achievement-icon {
    font-size: 35px;
    margin-right: 12px;
}

.small-text {
    color: #6b7280;
    font-size: 13px;
}

.author-box {
    background: rgba(255,255,255,0.12);
    padding: 15px;
    border-radius: 15px;
    margin-top: 15px;
}

.output-box {
    background: #111827;
    color: #f9fafb;
    padding: 20px;
    border-radius: 15px;
    font-family: Consolas, monospace;
    white-space: pre-wrap;
    overflow-x: auto;
}

.info-box {
    background: #eff6ff;
    padding: 18px;
    border-radius: 15px;
    border-left: 5px solid #3b82f6;
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

if "completed_lesson_keys" not in st.session_state:
    st.session_state.completed_lesson_keys = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "streak" not in st.session_state:
    st.session_state.streak = 1

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "ai_question" not in st.session_state:
    st.session_state.ai_question = ""

# =========================================================
# PROJECT INFORMATION
# =========================================================

PROJECT_AUTHOR = "Бердібек Назерке"

# =========================================================
# COURSE DATA
# =========================================================

courses = [
    {
        "title": "Python бастауыш курсы",
        "icon": "🐍",
        "description": "Python бағдарламалауын нөлден бастап үйрену",
        "lessons": [

            {
                "title": "Қош келдіңіз!",
                "video": "https://www.youtube.com/watch?v=aDvfZQNA49A",
                "theory": [
                    "Қош келдіңіз! Бұл курста Python бағдарламалау тілін нөлден бастап үйренесіз.",
                    "Python — синтаксисі қарапайым, мүмкіндігі кең және қазіргі кезде кең қолданылатын бағдарламалау тілі.",
                    "Курс барысында программа жазуды, есеп шығаруды, шарттарды, циклдерді, тізімдерді, функцияларды және рекурсияны үйренесіз.",
                    "Әр сабақта теорияны оқып, мысалды қарап, практикалық тапсырманы орындауға мүмкіндік аласыз."
                ],
                "example": "print('Python үйренуді бастаймыз!')",
                "task": "Python тілін үйренудегі өз мақсатыңызды анықтаңыз. Мысалы: олимпиадалық есептер шығару, бағдарлама жасау немесе AI саласын үйрену."
            },

            {
                "title": "Python орнату",
                "video": "",
                "theory": [
                    "Python бағдарламаларын орындау үшін компьютерге Python интерпретаторын орнату қажет.",
                    "Бағдарламаның жұмысын тексеру үшін қарапайым print() командасын орындауға болады."
                ],
                "example": "print('Python орнатылды!')",
                "task": "Python бағдарламасын орнатып, бірінші экранға Hello Python! шығарыңыз."
            },

            {
                "title": "Енгізу, шығару және сандар",
                "video": "",
                "theory": [
                    "input() функциясы пайдаланушыдан ақпарат енгізу үшін қолданылады.",
                    "print() функциясы нәтижені экранға шығарады.",
                    "input() арқылы енгізілген мән әдетте мәтін ретінде қабылданады.",
                    "Санмен жұмыс істеу үшін int() немесе float() функцияларын қолдануға болады."
                ],
                "example": """name = input('Атыңыз: ')
age = int(input('Жасыңыз: '))

print('Сәлем,', name)
print('Сіздің жасыңыз:', age)""",
                "task": "Пайдаланушыдан оның атын және жасын сұрап, экранға осы ақпаратты шығаратын бағдарлама жазыңыз."
            },

            {
                "title": "Бүтін сандар арифметикасы",
                "video": "",
                "theory": [
                    "Python тілінде бүтін сандар int типімен беріледі.",
                    "Қосу үшін +, азайту үшін -, көбейту үшін *, бөлу үшін / қолданылады.",
                    "// операторы бүтін бөлікке бөлуді орындайды.",
                    "% операторы бөлгендегі қалдықты табады.",
                    "** операторы санды дәрежеге шығарады."
                ],
                "example": """a = 17
b = 5

print(a + b)
print(a - b)
print(a * b)
print(a // b)
print(a % b)
print(a ** 2)""",
                "task": "Екі бүтін сан енгізіп, олардың қосындысын, айырмасын, көбейтіндісін, бүтін бөліндісін және қалдығын табыңыз."
            },

            {
                "title": "Шартты операторлар",
                "video": "",
                "theory": [
                    "Шартты оператор программаға белгілі бір жағдайға байланысты шешім қабылдауға мүмкіндік береді.",
                    "if операторы шартты тексереді.",
                    "else — шарт орындалмаған кездегі әрекетті анықтайды.",
                    "Бірнеше шартты тексеру үшін elif қолданылады.",
                    "Салыстыру операторлары: >, <, >=, <=, ==, !=."
                ],
                "example": """age = int(input('Жасыңыз: '))

if age >= 18:
    print('Кәмелетке толған')
else:
    print('Кәмелетке толмаған')""",
                "task": "Берілген санның оң, теріс немесе нөл екенін анықтайтын бағдарлама жазыңыз."
            },

            {
                "title": "For циклі",
                "video": "",
                "theory": [
                    "for циклі белгілі бір әрекетті бірнеше рет орындау үшін қолданылады.",
                    "range() функциясы сандар қатарын құруға мүмкіндік береді.",
                    "for циклі олимпиадалық бағдарламалауда өте жиі қолданылады.",
                    "Циклдің қайталану санын алдын ала анықтауға болады."
                ],
                "example": """for i in range(1, 6):
    print(i)""",
                "task": "1-ден 10-ға дейінгі сандарды экранға шығарыңыз. Содан кейін осы сандардың қосындысын табыңыз."
            },

            {
                "title": "Жолдар (str)",
                "video": "",
                "theory": [
                    "Жол (str) — мәтіндік ақпаратты сақтайтын деректер типі.",
                    "Жол тырнақша арқылы жазылады.",
                    "Жолдың жеке символдары индекс арқылы алынады.",
                    "Python тілінде индекстеу 0-ден басталады.",
                    "len() функциясы жолдың ұзындығын анықтайды."
                ],
                "example": """text = 'Python'

print(text)
print(text[0])
print(text[2])
print(len(text))""",
                "task": "Пайдаланушыдан сөз енгізіңіз. Оның ұзындығын, бірінші және соңғы символын экранға шығарыңыз."
            },

            {
                "title": "While циклі",
                "video": "",
                "theory": [
                    "while циклі белгілі бір шарт True болғанша қайталанады.",
                    "for циклінен айырмашылығы — қайталану саны алдын ала белгісіз болуы мүмкін.",
                    "while циклінде цикл шартының өзгеруін бақылау маңызды.",
                    "Әйтпесе шексіз цикл пайда болуы мүмкін."
                ],
                "example": """i = 1

while i <= 5:
    print(i)
    i += 1""",
                "task": "while циклін пайдаланып, 1-ден 10-ға дейінгі сандарды экранға шығарыңыз."
            },

            {
                "title": "Тізімдер (Lists)",
                "video": "",
                "theory": [
                    "List — бірнеше мәнді бір жерде сақтауға мүмкіндік беретін деректер құрылымы.",
                    "Тізім квадрат жақша арқылы жазылады.",
                    "Тізім элементтерінің индекстері 0-ден басталады.",
                    "append() әдісі жаңа элемент қосады.",
                    "len() тізімдегі элементтер санын анықтайды."
                ],
                "example": """numbers = [10, 20, 30, 40]

print(numbers)
print(numbers[0])

numbers.append(50)
print(numbers)""",
                "task": "5 саннан тұратын тізім құрыңыз. Оның бірінші элементін, соңғы элементін және элементтер санын шығарыңыз."
            },

            {
                "title": "Функция және рекурсия",
                "video": "",
                "theory": [
                    "Функция — белгілі бір әрекетті орындайтын қайта пайдалануға болатын код бөлігі.",
                    "Python тілінде функция def кілттік сөзі арқылы құрылады.",
                    "Функция параметр қабылдап, нәтиже қайтара алады.",
                    "Рекурсия — функцияның өзін-өзі шақыруы.",
                    "Рекурсивті функцияда тоқтау шарты міндетті түрде болуы керек."
                ],
                "example": """def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))""",
                "task": "Берілген санның факториалын есептейтін функция құрыңыз. Алдымен цикл арқылы, кейін рекурсия арқылы орындап көріңіз."
            }
        ]
    },

    {
        "title": "Python деректер құрылымдары",
        "icon": "📚",
        "description": "2D Lists, Sets және Dictionaries",
        "lessons": [

            {
                "title": "Кірістірілген тізімдер (2D Lists)",
                "video": "",
                "theory": [
                    "2D List — тізімнің ішінде басқа тізімдер орналасқан құрылым.",
                    "Оны кесте немесе матрица ретінде қарастыруға болады.",
                    "Элементке екі индекс арқылы қатынауға болады: matrix[жол][баған].",
                    "2D Lists матрицалармен, кестелермен және олимпиадалық есептермен жұмыс істеуде маңызды."
                ],
                "example": """matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[0][0])
print(matrix[1][2])""",
                "task": "3×3 өлшемді матрица құрыңыз. Оның бірінші жолын және ортасындағы элементті экранға шығарыңыз."
            },

            {
                "title": "Жиындар (Sets)",
                "video": "",
                "theory": [
                    "Set — қайталанбайтын элементтерді сақтайтын деректер құрылымы.",
                    "Жиын фигуралық жақшалар арқылы жазылады.",
                    "Set ішінде бірдей элемент бірнеше рет сақталмайды.",
                    "Жиындар қайталанатын элементтерді жою және екі жиынды салыстыру үшін өте пайдалы.",
                    "union(), intersection() сияқты амалдар жиындармен жұмыс істеуге мүмкіндік береді."
                ],
                "example": """numbers = {1, 2, 2, 3, 4, 4}

print(numbers)

A = {1, 2, 3}
B = {3, 4, 5}

print(A & B)
print(A | B)""",
                "task": "Берілген тізімнен қайталанатын элементтерді Set көмегімен алып тастаңыз."
            },

            {
                "title": "Сөздіктер (Dictionaries)",
                "video": "",
                "theory": [
                    "Dictionary — ақпаратты кілт және мән жұбы түрінде сақтайтын деректер құрылымы.",
                    "Dictionary фигуралық жақша арқылы жазылады.",
                    "Әрбір элемент key:value түрінде беріледі.",
                    "Кілт арқылы сәйкес мәнді тез алуға болады.",
                    "Dictionary оқушы туралы ақпарат, тауар сипаттамасы және басқа құрылымды деректерді сақтау үшін қолданылады."
                ],
                "example": """student = {
    'name': 'Aruzhan',
    'age': 15,
    'grade': 10
}

print(student['name'])
print(student['age'])""",
                "task": "Оқушының аты, жасы, сыныбы және бағасын Dictionary түрінде сақтаңыз. Әр ақпаратты жеке шығарыңыз."
            }
        ]
    }
]

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_youtube_url(url):
    if not url:
        return ""

    try:
        parsed = urlparse(url)

        if "youtube.com" in parsed.netloc:
            query = parse_qs(parsed.query)
            video_id = query.get("v", [None])[0]

            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"

        if "youtu.be" in parsed.netloc:
            video_id = parsed.path.strip("/")

            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"

    except Exception:
        pass

    return url


def syntax_check(code):
    if not code.strip():
        return False, "Код енгізілмеді."

    try:
        ast.parse(code)
        return True, "Синтаксистік қате табылған жоқ."

    except SyntaxError as e:
        return False, (
            f"Синтаксистік қате: {e.msg}\n"
            f"Жол: {e.lineno}\n"
            f"Баған: {e.offset}"
        )


def explain_error(error_text):
    if "SyntaxError" in error_text:
        return "❌ Синтаксистік қате. Жақша, қос нүкте, тырнақша немесе код құрылымын тексеріңіз."

    if "IndentationError" in error_text:
        return "❌ Шегініс қатесі. if, for, while, def блоктарының ішіндегі бос орындарды тексеріңіз."

    if "NameError" in error_text:
        return "❌ NameError. Бағдарламада анықталмаған айнымалы немесе функция қолданылған."

    if "TypeError" in error_text:
        return "❌ TypeError. Деректер типтерімен дұрыс емес амал орындалған."

    if "ValueError" in error_text:
        return "❌ ValueError. Деректер дұрыс типте емес немесе дұрыс мән енгізілмеген."

    if "IndexError" in error_text:
        return "❌ IndexError. Тізімде жоқ индекс арқылы элемент алуға әрекет жасалған."

    if "ZeroDivisionError" in error_text:
        return "❌ ZeroDivisionError. Сан 0-ге бөлінген."

    if "EOFError" in error_text:
        return "❌ EOFError. input() үшін қажетті мәлімет енгізілмеген."

    return "❌ Бағдарлама орындау кезінде қате пайда болды. Төмендегі толық қате мәтінін тексеріңіз."


def run_python_code(code, input_data=""):
    if not code.strip():
        return False, "", "Код енгізілмеді.", None

    valid, message = syntax_check(code)

    if not valid:
        return False, "", message, None

    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )

        stdout = result.stdout
        stderr = result.stderr

        if result.returncode == 0:
            return True, stdout, stderr, result.returncode

        return False, stdout, stderr, result.returncode

    except subprocess.TimeoutExpired:
        return False, "", "⏱️ Бағдарлама 5 секундтан ұзақ жұмыс істеді. Шексіз цикл болуы мүмкін.", None

    except Exception as e:
        return False, "", str(e), None


def ai_response(question):
    q = question.lower()

    if "print" in q:
        return "print() функциясы ақпаратты экранға шығару үшін қолданылады."

    if "input" in q:
        return "input() функциясы пайдаланушыдан мәлімет енгізу үшін қолданылады. Мысалы: name = input('Атыңыз: ')"

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

    if "set" in q or "жиын" in q:
        return "Set — қайталанбайтын элементтер жиыны. Мысалы: numbers = {1, 2, 3}."

    if "dictionary" in q or "сөздік" in q:
        return "Dictionary ақпаратты key:value түрінде сақтайды. Мысалы: student = {'name': 'Aruzhan'}."

    if "error" in q or "қате" in q:
        return (
            "Кодтағы қатені табу үшін:\n"
            "1. Жақшаларды тексеріңіз.\n"
            "2. Қос нүктені тексеріңіз.\n"
            "3. Шегіністі тексеріңіз.\n"
            "4. Айнымалы атауларын тексеріңіз.\n"
            "5. Қате мәтінін толық оқыңыз."
        )

    return (
        "Жақсы сұрақ! Есептің шартын шағын қадамдарға бөліп алыңыз. "
        "Содан кейін қандай айнымалылар, шарттар немесе циклдер қажет екенін анықтаңыз."
    )


def lesson_key(course_index, lesson_index):
    return f"{course_index}_{lesson_index}"


def is_completed(course_index, lesson_index):
    return lesson_key(course_index, lesson_index) in st.session_state.completed_lesson_keys


def complete_lesson(course_index, lesson_index):
    key = lesson_key(course_index, lesson_index)

    if key not in st.session_state.completed_lesson_keys:
        st.session_state.completed_lesson_keys.append(key)
        st.session_state.xp += 10
        return True

    return False


def go_to(page):
    st.session_state.page = page


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🤖 TOTAL AI")
    st.markdown("## TUTOR")

    st.markdown("---")

    st.text_input(
        "👨‍🎓 Оқушының аты-жөні",
        key="student_name",
        placeholder="Мысалы: Аружан"
    )

    if st.button("🏠  Басты бет", use_container_width=True):
        go_to("home")

    if st.button("📚  Python курстары", use_container_width=True):
        go_to("courses")

    if st.button("💻  Практика", use_container_width=True):
        go_to("practice")

    if st.button("🤖  AI Tutor", use_container_width=True):
        go_to("ai")

    if st.button("🏆  Менің прогресім", use_container_width=True):
        go_to("progress")

    st.markdown("---")

    st.markdown("### 👨‍🎓 Оқушы")

    if st.session_state.student_name:
        st.write(f"**{st.session_state.student_name}**")
    else:
        st.write("Аты-жөніңізді енгізіңіз")

    st.markdown("---")

    st.markdown(
        f"""
        <div class="author-box">
        <b>📌 Жоба авторы:</b><br>
        {PROJECT_AUTHOR}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.caption("TOTAL AI TUTOR")
    st.caption("Python + AI Education")


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "home":

    student = (
        st.session_state.student_name
        if st.session_state.student_name
        else "Қош келдіңіз!"
    )

    st.markdown(
        f"""
        <div class="hero">
            <h1>🤖 TOTAL AI TUTOR</h1>
            <p>
            Python бағдарламалауын AI көмегімен үйренуге арналған
            интеллектуалды білім беру платформасы
            </p>
            <hr>
            <p>👨‍🎓 Оқушы: <b>{student}</b></p>
            <p>📌 Жоба авторы: <b>{PROJECT_AUTHOR}</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    total_lessons = sum(len(c["lessons"]) for c in courses)
    completed = len(st.session_state.completed_lesson_keys)

    progress = (
        completed / total_lessons
        if total_lessons > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">📚</div>
                <div class="stat-number">{len(courses)}</div>
                <div class="stat-title">Python курсы</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-number">{completed}</div>
                <div class="stat-title">Орындалған сабақ</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-number">{st.session_state.xp}</div>
                <div class="stat-title">XP ұпайы</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-number">{st.session_state.streak}</div>
                <div class="stat-title">Күндік серия</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 🚀 Python үйренуді бастаңыз")

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

            course_completed = sum(
                1
                for i in range(len(course["lessons"]))
                if is_completed(index, i)
            )

            course_progress = (
                course_completed / len(course["lessons"])
                if course["lessons"]
                else 0
            )

            with cols[j]:

                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-icon">
                            {course["icon"]}
                        </div>

                        <div class="course-title">
                            {course["title"]}
                        </div>

                        <div class="course-description">
                            {course["description"]}
                        </div>

                        <p>
                            📖 {len(course["lessons"])} сабақ
                        </p>

                        <p>
                            ✅ {course_completed} орындалды
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.progress(course_progress)

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
# COURSES
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
        f"""
        <div class="lesson-header">
            <h1>{course["icon"]} {course["title"]}</h1>
            <p>{course["description"]}</p>
        </div>
        """,
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
        f"""
        <div class="lesson-header">
            <h2>📖 {lesson["title"]}</h2>
            <p>
                Сабақ {lesson_index + 1} /
                {len(course["lessons"])}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # VIDEO
    # =====================================================

    video_url = clean_youtube_url(
        lesson.get("video", "")
    )

    if video_url:

        st.markdown("## 🎬 Видеосабақ")

        try:
            st.video(video_url)
        except Exception:
            st.info(
                "🎬 Видеоны ашу кезінде мәселе болды. "
                "YouTube сілтемесін тексеріңіз."
            )

    # =====================================================
    # THEORY
    # =====================================================

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

    # =====================================================
    # EXAMPLE
    # =====================================================

    st.markdown("## 💡 Мысал")

    st.code(
        lesson["example"],
        language="python"
    )

    # =====================================================
    # TASK
    # =====================================================

    st.markdown("## 🎯 Практикалық тапсырма")

    st.markdown(
        f"""
        <div class="task-box">
            <h3>📝 Тапсырма</h3>
            <p>{lesson["task"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # CODE EDITOR
    # =====================================================

    st.markdown("## 💻 Python код редакторы")

    code = st.text_area(
        "Python кодын осы жерге жазыңыз:",
        height=280,
        placeholder=(
            "# Python кодын жазыңыз\n"
            "name = input('Атыңыз: ')\n"
            "print('Сәлем,', name)"
        ),
        key=f"editor_{selected}_{lesson_index}"
    )

    st.markdown("### 📥 Бағдарламаға енгізілетін мәлімет")

    input_data = st.text_area(
        "Егер input() қолдансаңыз, әр енгізуді жаңа жолға жазыңыз:",
        height=120,
        placeholder=(
            "Aruzhan\n"
            "15"
        ),
        key=f"input_{selected}_{lesson_index}"
    )

    col1, col2, col3 = st.columns(3)

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
            "▶️ Кодты іске қосу",
            use_container_width=True
        ):

            success, output, error, return_code = run_python_code(
                code,
                input_data
            )

            if success:

                st.success("✅ Бағдарлама сәтті орындалды!")

                st.markdown("### 📤 Нәтиже")

                if output.strip():

                    st.markdown(
                        f"""
                        <div class="output-box">
                        {output.replace("<", "&lt;").replace(">", "&gt;")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.info(
                        "Бағдарлама орындалды, "
                        "бірақ экранға нәтиже шығарылмады."
                    )

            else:

                st.error("❌ Бағдарламаны орындау кезінде қате пайда болды.")

                if output.strip():

                    st.markdown("### 📤 Шыққан нәтиже")

                    st.code(
                        output,
                        language="text"
                    )

                if error.strip():

                    st.markdown("### ❌ Қате")

                    st.code(
                        error,
                        language="text"
                    )

                    st.markdown(
                        f"""
                        <div class="error-box">
                            <b>💡 Түсіндірме:</b><br>
                            {explain_error(error)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    with col3:

        if st.button(
            "🤖 AI көмегін алу",
            use_container_width=True
        ):

            st.session_state.page = "ai"

            st.session_state.ai_question = (
                f"Мен «{lesson['title']}» сабағындағы "
                f"мына тапсырманы орындап жатырмын: "
                f"{lesson['task']}"
            )

            st.rerun()

    st.markdown("---")

    # =====================================================
    # LESSON STATUS
    # =====================================================

    if is_completed(selected, lesson_index):

        st.success(
            "✅ Бұл сабақ бұрын аяқталған. +10 XP қайта қосылмайды."
        )

    # =====================================================
    # NAVIGATION
    # =====================================================

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

            added = complete_lesson(
                selected,
                lesson_index
            )

            if added:

                st.success(
                    "🎉 Сабақ аяқталды! +10 XP"
                )

                st.balloons()

            else:

                st.info(
                    "Бұл сабақ бұрын аяқталған."
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
# PRACTICE
# =========================================================

elif st.session_state.page == "practice":

    st.title("💻 Python практикасы")

    st.markdown(
        """
        <div class="info-box">
        <b>💡 Кеңес:</b>
        Есептің кодын жазыңыз, енгізу мәндерін беріңіз
        және «Кодты іске қосу» батырмасын басыңыз.
        </div>
        """,
        unsafe_allow_html=True
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
        f"""
        <div class="task-box">
            <h2>{task["title"]}</h2>
            <p>{task["text"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    practice_code = st.text_area(
        "Python кодыңызды жазыңыз:",
        height=300,
        key=f"practice_{task_index}"
    )

    practice_input = st.text_area(
        "📥 Input:",
        height=120,
        key=f"practice_input_{task_index}",
        placeholder="Енгізілетін мәндерді әр жолға жазыңыз"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔍 Синтаксисті тексеру",
            use_container_width=True
        ):

            valid, message = syntax_check(
                practice_code
            )

            if valid:

                st.success(message)

            else:

                st.error(message)

    with col2:

        if st.button(
            "▶️ Бағдарламаны іске қосу",
            use_container_width=True
        ):

            success, output, error, return_code = run_python_code(
                practice_code,
                practice_input
            )

            if success:

                st.success(
                    "✅ Бағдарлама сәтті орындалды!"
                )

                st.markdown("### 📤 Нәтиже")

                st.code(
                    output if output else "Нәтиже жоқ.",
                    language="text"
                )

            else:

                st.error("❌ Қате!")

                if output:
                    st.code(
                        output,
                        language="text"
                    )

                if error:
                    st.code(
                        error,
                        language="text"
                    )

                    st.warning(
                        explain_error(error)
                    )


# =========================================================
# AI TUTOR
# =========================================================

elif st.session_state.page == "ai":

    st.title("🤖 AI Tutor")

    st.markdown(
        """
        <div class="ai-box">
            <h2>🧠 Сіздің Python көмекшіңіз</h2>
            <p>
            Python тақырыптары, код қателері және
            алгоритмдер бойынша сұрақ қойыңыз.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💬 Сұрағыңызды жазыңыз")

    question = st.text_area(
        "Сұрақ:",
        value=st.session_state.ai_question,
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
                f"""
                <div class="success-box">
                    <h3>🤖 AI Tutor:</h3>
                    <p>{answer}</p>
                </div>
                """,
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
        "input() қалай жұмыс істейді?",
        "if операторы қалай жұмыс істейді?",
        "for циклі қалай жазылады?",
        "List дегеніміз не?",
        "Set дегеніміз не?",
        "Dictionary дегеніміз не?",
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
# PROGRESS
# =========================================================

elif st.session_state.page == "progress":

    st.title("🏆 Менің прогресім")

    total_lessons = sum(
        len(c["lessons"])
        for c in courses
    )

    completed = len(
        st.session_state.completed_lesson_keys
    )

    progress = (
        completed / total_lessons
        if total_lessons
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
            f"{completed}/{total_lessons}"
        )

    with col3:

        st.metric(
            "🔥 Серия",
            f"{st.session_state.streak} күн"
        )

    st.markdown("## 📈 Жалпы прогресс")

    st.progress(progress)

    st.write(
        f"Сіз **{completed} / {total_lessons}** "
        f"сабақты аяқтадыңыз."
    )

    st.markdown("## 📚 Курстар бойынша")

    for course_index, course in enumerate(courses):

        course_completed = sum(
            1
            for lesson_index in range(
                len(course["lessons"])
            )
            if is_completed(
                course_index,
                lesson_index
            )
        )

        course_progress = (
            course_completed / len(course["lessons"])
            if course["lessons"]
            else 0
        )

        st.markdown(
            f"### {course['icon']} {course['title']}"
        )

        st.progress(course_progress)

        st.caption(
            f"{course_completed} / "
            f"{len(course['lessons'])} сабақ"
        )

    st.markdown("## 🏅 Жетістіктер")

    achievements = [

        (
            "🐣",
            "Алғашқы қадам",
            "Бірінші сабақты аяқтаңыз",
            completed >= 1
        ),

        (
            "🔥",
            "Белсенді оқушы",
            "5 сабақ аяқтаңыз",
            completed >= 5
        ),

        (
            "⭐",
            "Python бастаушы",
            "50 XP жинаңыз",
            st.session_state.xp >= 50
        ),

        (
            "🚀",
            "Python зерттеушісі",
            "10 сабақ аяқтаңыз",
            completed >= 10
        )

    ]

    for icon, title, description, unlocked in achievements:

        status = "🔓" if unlocked else "🔒"

        st.markdown(
            f"""
            <div class="achievement">
                <span class="achievement-icon">
                    {icon}
                </span>

                <b>
                    {status} {title}
                </b>

                <p class="small-text">
                    {description}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    f"""
    <center>
        <small>
        🤖 TOTAL AI TUTOR • Python + Artificial Intelligence Education
        <br>
        📌 Жоба авторы: {PROJECT_AUTHOR}
        </small>
    </center>
    """,
    unsafe_allow_html=True
)
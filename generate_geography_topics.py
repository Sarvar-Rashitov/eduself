"""
Geografiya uchun qolgan 80 ta mavzuni avtomatik yaratish
To'g'ri javoblar turli pozitsiyalarda
"""
import random

# 21-100 mavzular
topics_data = [
    ("O'rmonlar", 21),
    ("Savannalar", 22),
    ("Tundra", 23),
    ("Tayga", 24),
    ("Iqlim turlari", 25),
    ("Aholi va aholi punktlari", 26),
    ("Shaharlar", 27),
    ("Qishloqlar", 28),
    ("Transport", 29),
    ("Sanoat", 30),
    ("Qishloq xo'jaligi", 31),
    ("Tabiiy resurslar", 32),
    ("Suv resurslari", 33),
    ("O'rmon resurslari", 34),
    ("Mineral resurslar", 35),
    ("Energiya resurslari", 36),
    ("Ekologiya", 37),
    ("Atrof-muhitni muhofaza qilish", 38),
    ("Qizil kitob", 39),
    ("Tabiat hududlari", 40),
    ("Yevroosiyo materigi", 41),
    ("Afrika materigi", 42),
    ("Shimoliy Amerika materigi", 43),
    ("Janubiy Amerika materigi", 44),
    ("Avstraliya materigi", 45),
    ("Antarktida materigi", 46),
    ("Tinch okeani", 47),
    ("Atlantika okeani", 48),
    ("Hind okeani", 49),
    ("Shimoliy Muz okeani", 50),
    ("O'zbekiston", 51),
    ("Markaziy Osiyo", 52),
    ("Rossiya", 53),
    ("Xitoy", 54),
    ("Hindiston", 55),
    ("AQSH", 56),
    ("Yevropa", 57),
    ("Osiyo", 58),
    ("Afrika mintaqalari", 59),
    ("Amerika mintaqalari", 60),
    ("Dunyo iqtisodiyoti", 61),
    ("Xalqaro savdo", 62),
    ("Aholi o'sishi", 63),
    ("Urbanizatsiya", 64),
    ("Global iqlim o'zgarishi", 65),
    ("Suv tanqisligi", 66),
    ("Oziq-ovqat muammosi", 67),
    ("Energiya muammosi", 68),
    ("Tabiiy ofatlar", 69),
    ("Barqaror rivojlanish", 70),
    ("GPS va xarita texnologiyalari", 71),
    ("Sun'iy yo'ldoshlar", 72),
    ("Turizm geografiyasi", 73),
    ("Shahar rejalashtirish", 74),
    ("Transport geografiyasi", 75),
    ("Sanoat geografiyasi", 76),
    ("Qishloq xo'jaligi geografiyasi", 77),
    ("Aholi geografiyasi", 78),
    ("Madaniy geografiya", 79),
    ("Iqtisodiy geografiya", 80),
    ("Aqlli shaharlar", 81),
    ("Raqamli geografiya", 82),
    ("Kosmik geografiya", 83),
    ("Okean geografiyasi", 84),
    ("Qutb geografiyasi", 85),
    ("Tog' geografiyasi", 86),
    ("Cho'l geografiyasi", 87),
    ("O'rmon geografiyasi", 88),
    ("Daryo geografiyasi", 89),
    ("Geografiya va kelajak", 90),
    ("Geografik kashfiyotlar", 91),
    ("Mashhur geograflar", 92),
    ("Geografiya va san'at", 93),
    ("Geografiya va adabiyot", 94),
    ("Geografiya va musiqa", 95),
    ("Geografiya va sport", 96),
    ("Geografiya va oziq-ovqat", 97),
    ("Geografiya va til", 98),
    ("Geografiya va din", 99),
    ("Geografiya fani yakuniy takrorlash", 100),
]

def create_question_with_mixed_answers(question_text, correct_answer, wrong_answers):
    """To'g'ri javobni tasodifiy pozitsiyaga joylashtirish"""
    answers = [{'t': correct_answer, 'c': True}]
    for wa in wrong_answers:
        answers.append({'t': wa, 'c': False})
    
    # Javoblarni aralashtiramiz
    random.shuffle(answers)
    
    return {'t': question_text, 'a': answers}

# Har bir mavzu uchun 5 ta test yaratamiz
output = []

for topic_name, order in topics_data:
    questions = []
    
    # Har bir mavzu uchun 5 ta oddiy test
    for i in range(5):
        q_text = f"{topic_name} haqida savol {i+1}?"
        correct = f"{topic_name} to'g'ri javob {i+1}"
        wrongs = [f"Noto'g'ri javob A", f"Noto'g'ri javob B", f"Noto'g'ri javob C"]
        
        questions.append(create_question_with_mixed_answers(q_text, correct, wrongs))
    
    topic_dict = {
        'n': topic_name,
        't': 20,
        'o': order,
        'q': questions
    }
    
    output.append(topic_dict)

# Python kod sifatida chiqarish
print("    # QOLGAN MAVZULAR (21-100)")
for topic in output:
    print(f"    {topic},")

print("\nJami:", len(output), "ta mavzu yaratildi")
print("Har bir mavzuda 5 ta test")
print("To'g'ri javoblar tasodifiy pozitsiyalarda")

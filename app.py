from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from questions.all_physics import PhysicsGenerator
from questions.marathon_questions import MarathonGenerator
import random

app = Flask(__name__)
app.secret_key = 'ege_physics_secret_key_2026'
generator = PhysicsGenerator()
marathon_gen = MarathonGenerator()

# Все темы и подтемы с группировкой
TOPICS = {
    "Механика": {
        "kinematics_linear": "Кинематика (прямолинейное)",
        "kinematics_circular": "Кинематика (криволинейное)",
        "ballistics": "Баллистика",
        "dynamics": "Динамика",
        "conservation": "Законы сохранения",
        "statics": "Статика и гидростатика",
        "oscillations": "Колебания и волны"
    },
    "МКТ": {
        "mkt_isoprocesses": "Изопроцессы",
        "mkt_humidity": "Влажность"
    },
    "Термодинамика": {
        "thermo_first_law": "Первый закон термодинамики",
        "thermo_efficiency": "КПД тепловых двигателей"
    },
    "Электростатика": {
        "electro_charges": "Заряды и закон Кулона",
        "electro_field": "Напряжённость и потенциал",
        "electro_capacitors": "Конденсаторы",
        "electro_dc": "Постоянный ток",
        "electro_ac": "Переменный ток",
        "electro_ohm_full": "Закон Ома для полной цепи",
        "electro_lorentz": "Сила Лоренца",
        "electro_ampere": "Сила Ампера",
        "electro_flux": "Магнитный поток",
        "electro_osc_circuit": "Колебательный контур"
    },
    "Оптика": {
        "optics_lenses": "Линзы (собирающие/рассеивающие)",
        "optics_power": "Оптическая сила линз",
        "optics_interference": "Интерференция",
        "optics_diffraction": "Дифракция"
    },
    "Ядерная физика": {
        "nuclear_atom": "Строение атома и ядра",
        "nuclear_radioactivity": "Радиоактивность и виды распада",
        "nuclear_reactions": "Ядерные реакции",
        "nuclear_binding": "Энергия связи и дефект массы"
    }
}


@app.route('/')
def index():
    session.clear()
    return render_template('index.html', topics=TOPICS)


# ============ ОБЫЧНЫЕ ТЕСТЫ ПО ПОДТЕМАМ ============
@app.route('/start/<topic>')
def start_quiz(topic):
    session.clear()

    if topic not in generator.templates:
        return "Подтема не найдена", 404

    session['mode'] = 'topic'
    session['topic'] = topic
    session['current_q'] = 0
    session['correct'] = 0
    session['total'] = generator.get_total_questions(topic)
    session['questions'] = []

    topic_name = topic
    for group, subs in TOPICS.items():
        if topic in subs:
            topic_name = subs[topic]
            break

    return render_template('quiz.html', topic=topic_name, total=session['total'])


# ============ БОЛЬШОЙ МАРАФОН ============
@app.route('/start_marathon')
def start_marathon():
    session.clear()

    session['mode'] = 'marathon'
    session['current_q'] = 0
    session['correct'] = 0
    session['total'] = marathon_gen.get_marathon_total()
    session['questions'] = []

    return render_template('quiz.html',
                           topic='🏃 МАРАФОН — 100 вопросов по всей физике',
                           total=session['total'])


# ============ МИНИ-МАРАФОНЫ ============
@app.route('/start_section_marathon/<section>')
def start_section_marathon(section):
    session.clear()

    if section not in marathon_gen.section_questions:
        return "Раздел не найден", 404

    session['mode'] = 'section_marathon'
    session['section'] = section
    session['current_q'] = 0
    session['correct'] = 0
    session['total'] = marathon_gen.get_section_total(section)
    session['questions'] = []

    return render_template('quiz.html',
                           topic=f'🏃 {section} — {session["total"]} вопросов',
                           total=session['total'])


# ============ ПОЛУЧЕНИЕ ВОПРОСА ============
@app.route('/get_question')
def get_question():
    idx = session.get('current_q', 0)
    total = session.get('total', 0)
    mode = session.get('mode', 'topic')

    print(f"📌 Запрос вопроса: idx={idx}, total={total}, mode={mode}")

    if idx >= total:
        print("🏁 Вопросы закончились")
        return jsonify({
            'finished': True,
            'correct': session.get('correct', 0),
            'total': total
        })

    questions = session.get('questions', [])
    print(f"📦 questions в сессии: {len(questions)}")

    # Если вопрос уже есть в сессии — возвращаем его
    if questions and len(questions) > idx:
        q = questions[idx]
        print(f"✅ Вопрос из сессии: {q.get('question', '')[:50]}...")
        return jsonify({
            'finished': False,
            'question': q.get('question', ''),
            'options': q.get('options', []),
            'id': q.get('id', ''),
            'total': total,
            'current': idx + 1,
            'topic': q.get('topic', ''),
            'type': q.get('type', '')
        })

    # Генерируем новый вопрос
    q = None
    if mode == 'topic':
        topic = session.get('topic')
        q = generator.get_next_question(topic, idx)
        print(f"🔄 Генерация вопроса для темы {topic}, индекс {idx}")
    elif mode == 'marathon':
        q = marathon_gen.get_next_marathon_question(idx)
        print(f"🔄 Генерация вопроса для марафона, индекс {idx}")
    elif mode == 'section_marathon':
        section = session.get('section')
        q = marathon_gen.get_next_section_question(section, idx)
        print(f"🔄 Генерация вопроса для раздела {section}, индекс {idx}")

    if not q:
        print("❌ Вопрос не сгенерирован!")
        return jsonify({
            'finished': True,
            'correct': session.get('correct', 0),
            'total': total
        })

    print(f"✅ Сгенерирован вопрос: {q.get('question', '')[:50]}...")
    print(f"   Варианты: {q.get('options', [])}")

    # Сохраняем в сессию
    questions.append(q)
    session['questions'] = questions

    return jsonify({
        'finished': False,
        'question': q.get('question', ''),
        'options': q.get('options', []),
        'id': q.get('id', ''),
        'total': total,
        'current': idx + 1,
        'topic': q.get('topic', ''),
        'type': q.get('type', '')
    })


# ============ ОТВЕТ НА ВОПРОС ============
@app.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()
    user_ans = data.get('answer')
    idx = session.get('current_q', 0)
    questions = session.get('questions', [])

    if not questions or idx >= len(questions):
        return jsonify({'error': 'no question'})

    q = questions[idx]
    is_correct = (str(user_ans).strip() == str(q['correct']).strip())

    if is_correct:
        session['correct'] = session.get('correct', 0) + 1

    session['current_q'] = idx + 1

    return jsonify({
        'correct': is_correct,
        'correct_answer': str(q['correct']),
        'formula': q.get('formula', ''),
        'hint': q.get('hint', '')
    })


@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
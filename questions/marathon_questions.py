import random
import math


class MarathonGenerator:
    def __init__(self):
        self.marathon_questions = self._generate_marathon_questions()
        self.section_questions = self._create_section_questions()

    def _round_answer(self, value):
        """Округляет число до 2 знаков после запятой"""
        if isinstance(value, (int, float)):
            return round(value, 2)
        return value

    def _generate_options(self, correct):
        """
        Генерирует 4 варианта ответа — БЕЗ ЦИКЛОВ
        """
        # === ОБРАБОТКА ЧИСЕЛ ===
        try:
            num_val = float(correct)

            # Создаём список отклонений в зависимости от размера числа
            if num_val > 1000:
                # Для больших чисел — процентное отклонение
                percents = [0.05, 0.08, 0.12, 0.15, 0.20, 0.25]
                deviations = [round(num_val * p, 2) for p in percents]
                # Добавляем несколько фиксированных
                deviations.extend([50, 100, 200, 500])
            elif num_val > 100:
                # Для средних чисел
                percents = [0.05, 0.10, 0.15, 0.20]
                deviations = [round(num_val * p, 2) for p in percents]
                deviations.extend([10, 20, 30, 50])
            elif num_val > 10:
                # Для чисел от 10 до 100
                deviations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            elif num_val > 1:
                # Для чисел от 1 до 10
                deviations = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5]
            else:
                # Для чисел меньше 1
                deviations = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

            # Перемешиваем отклонения
            random.shuffle(deviations)

            # Собираем уникальные варианты
            wrong = []
            for dev in deviations:
                # Пробуем с плюсом и минусом
                for sign in [1, -1]:
                    w = round(num_val + sign * dev, 2)
                    if w != num_val and w > 0 and w not in wrong:
                        wrong.append(w)
                    if len(wrong) >= 3:
                        break
                if len(wrong) >= 3:
                    break

            # Если всё ещё меньше 3 — добиваем простыми значениями
            if len(wrong) < 3:
                for add in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                    for sign in [1, -1]:
                        w = round(num_val + sign * add, 2)
                        if w != num_val and w > 0 and w not in wrong:
                            wrong.append(w)
                        if len(wrong) >= 3:
                            break
                    if len(wrong) >= 3:
                        break

            answers = wrong[:3] + [num_val]
            random.shuffle(answers)
            return [str(self._round_answer(x)) for x in answers]

        except (ValueError, TypeError):
            pass

        # === ОБРАБОТКА СТРОК ===
        if isinstance(correct, str):
            # Для ответов типа "A=12, Z=6"
            if "A=" in correct and "Z=" in correct:
                try:
                    parts = correct.split(',')
                    a_part = parts[0].strip().split('=')[1]
                    z_part = parts[1].strip().split('=')[1]
                    a = int(a_part)
                    z = int(z_part)
                    return [
                        f"A={a}, Z={z}",
                        f"A={a + 2}, Z={z + 1}",
                        f"A={a + 1}, Z={z - 1}",
                        f"A={a - 1}, Z={z + 2}"
                    ]
                except:
                    return [correct, "Другой вариант", "Третий вариант", "Четвёртый вариант"]

            # Для ответов типа "222/86"
            if "/" in correct and len(correct) <= 10:
                parts = correct.split('/')
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    try:
                        A = int(parts[0])
                        Z = int(parts[1])
                        return [
                            f"{A}/{Z}",
                            f"{A + 4}/{Z + 2}",
                            f"{A - 2}/{Z}",
                            f"{A + 2}/{Z - 2}"
                        ]
                    except:
                        return [correct, "Другой вариант", "Третий вариант", "Четвёртый вариант"]

            # Для обычных строк
            return [correct, "Другой вариант", "Третий вариант", "Четвёртый вариант"]

        # === ЗАЩИТА ===
        return ["Ошибка", "Нет вариантов", "Попробуйте", "Снова"]

    def _generate_marathon_questions(self):
        """Генерирует 400 случайных вопросов"""
        questions = []

        # ============================================================
        # МЕХАНИКА — 120 вопросов
        # ============================================================

        for i in range(120):
            topic_choice = random.randint(0, 6)

            if topic_choice == 0:  # Скорость
                a = random.randint(1, 6)
                v0 = random.randint(0, 10)
                t = random.randint(2, 8)
                v = self._round_answer(v0 + a * t)
                q = {
                    "id": f"mech_{i + 1}",
                    "topic": "Кинематика (прямолинейное)",
                    "type": "Скорость",
                    "question": f"Тело движется равноускоренно с ускорением {a} м/с². Начальная скорость {v0} м/с. Какова скорость через {t} с?",
                    "correct": str(v),
                    "formula": "v = v₀ + at",
                    "hint": f"{v0} + {a}·{t} = {v}"
                }
            elif topic_choice == 1:  # Путь
                a = random.randint(1, 4)
                v0 = random.randint(0, 8)
                t = random.randint(2, 6)
                s = self._round_answer(v0 * t + (a * t * t) / 2)
                q = {
                    "id": f"mech_{i + 1}",
                    "topic": "Кинематика (прямолинейное)",
                    "type": "Путь",
                    "question": f"Тело движется равноускоренно с ускорением {a} м/с². Начальная скорость {v0} м/с. Какой путь пройдёт тело за {t} с?",
                    "correct": str(s),
                    "formula": "s = v₀t + at²/2",
                    "hint": f"{v0}·{t} + {a}·{t}²/2 = {s}"
                }
            elif topic_choice == 2:  # Тормозной путь
                v = random.randint(15, 25)
                a = random.randint(2, 5)
                s = self._round_answer((v * v) / (2 * a))
                q = {
                    "id": f"mech_{i + 1}",
                    "topic": "Кинематика (прямолинейное)",
                    "type": "Тормозной путь",
                    "question": f"Автомобиль движется со скоростью {v} м/с и начинает тормозить с ускорением {a} м/с². Каков тормозной путь?",
                    "correct": str(s),
                    "formula": "s = v²/(2a)",
                    "hint": f"{v}²/(2·{a}) = {s}"
                }
            elif topic_choice == 3:  # Динамика
                m = random.randint(2, 10)
                F = random.randint(10, 50)
                a = self._round_answer(F / m)
                q = {
                    "id": f"mech_{i + 1}",
                    "topic": "Динамика",
                    "type": "Ускорение",
                    "question": f"На тело массой {m} кг действует сила {F} Н. Какое ускорение приобретает тело?",
                    "correct": str(a),
                    "formula": "a = F/m",
                    "hint": f"{F}/{m} = {a}"
                }
            elif topic_choice == 4:  # Сила трения
                m = random.randint(2, 8)
                mu = round(random.uniform(0.1, 0.5), 2)
                F_tr = self._round_answer(mu * m * 9.8)
                q = {
                    "id": f"mech_{i + 1}",
                    "topic": "Динамика",
                    "type": "Сила трения",
                    "question": f"Тело массой {m} кг движется по горизонтальной поверхности. Коэффициент трения μ = {mu}. Какова сила трения? (g=9.8 м/с²)",
                    "correct": str(F_tr),
                    "formula": "F_тр = μ·m·g",
                    "hint": f"{mu}·{m}·9.8 = {F_tr}"
                }
            elif topic_choice == 5:  # Кинетическая энергия
                m = random.randint(2, 8)
                v = random.randint(3, 10)
                E = self._round_answer((m * v * v) / 2)
                q = {
                    "id": f"mech_{i + 1}",
                    "topic": "Законы сохранения",
                    "type": "Кинетическая энергия",
                    "question": f"Тело массой {m} кг движется со скоростью {v} м/с. Какова кинетическая энергия тела?",
                    "correct": str(E),
                    "formula": "E_k = mv²/2",
                    "hint": f"{m}·{v}²/2 = {E}"
                }
            else:  # Потенциальная энергия
                m = random.randint(2, 8)
                h = random.randint(2, 10)
                E = self._round_answer(m * 9.8 * h)
                q = {
                    "id": f"mech_{i + 1}",
                    "topic": "Законы сохранения",
                    "type": "Потенциальная энергия",
                    "question": f"Тело массой {m} кг поднято на высоту {h} м. Какова потенциальная энергия? (g=9.8 м/с²)",
                    "correct": str(E),
                    "formula": "E_p = mgh",
                    "hint": f"{m}·9.8·{h} = {E}"
                }

            q["options"] = self._generate_options(q["correct"])
            questions.append(q)

        # ============================================================
        # МКТ — 70 вопросов
        # ============================================================

        for i in range(70):
            topic = random.choice(["МКТ (Изопроцессы)", "МКТ (Влажность)"])

            if topic == "МКТ (Изопроцессы)":
                P1 = random.randint(1, 5)
                V1 = random.randint(2, 8)
                V2 = random.randint(1, 6)
                P2 = self._round_answer(P1 * V1 / V2)
                q = {
                    "id": f"mkt_{i + 1}",
                    "topic": topic,
                    "type": "Изотермический",
                    "question": f"Газ находится под давлением {P1} атм при объёме {V1} л. При изотермическом расширении объём увеличился до {V2} л. Каким стало давление?",
                    "correct": str(P2),
                    "formula": "P₁V₁ = P₂V₂",
                    "hint": f"{P1}·{V1}/{V2} = {P2}"
                }
            else:
                rho = random.randint(10, 25)
                rho_nas = random.randint(20, 30)
                phi = self._round_answer(rho / rho_nas * 100)
                q = {
                    "id": f"mkt_{i + 1}",
                    "topic": topic,
                    "type": "Относительная влажность",
                    "question": f"Абсолютная влажность воздуха составляет {rho} г/м³. Плотность насыщенного пара {rho_nas} г/м³. Какова относительная влажность?",
                    "correct": str(phi),
                    "formula": "φ = ρ/ρ_нас · 100%",
                    "hint": f"{rho}/{rho_nas}·100 = {phi}%"
                }

            q["options"] = self._generate_options(q["correct"])
            questions.append(q)

        # ============================================================
        # ТЕРМОДИНАМИКА — 60 вопросов
        # ============================================================

        for i in range(60):
            topic = random.choice(["Термодинамика (Первый закон)", "Термодинамика (КПД)"])

            if topic == "Термодинамика (Первый закон)":
                P = random.randint(100, 300)
                V1 = random.randint(2, 5)
                V2 = random.randint(6, 10)
                A = self._round_answer(P * (V2 - V1))
                q = {
                    "id": f"thermo_{i + 1}",
                    "topic": topic,
                    "type": "Работа газа",
                    "question": f"Газ расширяется при постоянном давлении {P} кПа, объём увеличивается с {V1} л до {V2} л. Какую работу совершает газ?",
                    "correct": str(A),
                    "formula": "A = P·ΔV",
                    "hint": f"{P}·({V2}-{V1}) = {A}"
                }
            else:
                Q1 = random.randint(1000, 2000)
                Q2 = random.randint(200, 400)
                eta = self._round_answer((Q1 - Q2) / Q1 * 100)
                q = {
                    "id": f"thermo_{i + 1}",
                    "topic": topic,
                    "type": "КПД двигателя",
                    "question": f"Тепловой двигатель получает {Q1} Дж теплоты и отдаёт {Q2} Дж холодильнику. Каков КПД двигателя?",
                    "correct": str(eta),
                    "formula": "η = (Q₁-Q₂)/Q₁ · 100%",
                    "hint": f"({Q1}-{Q2})/{Q1}·100 = {eta}%"
                }

            q["options"] = self._generate_options(q["correct"])
            questions.append(q)

        # ============================================================
        # ЭЛЕКТРОСТАТИКА — 80 вопросов
        # ============================================================

        for i in range(80):
            topic = random.choice([
                "Электростатика (Заряды)",
                "Электростатика (Конденсаторы)",
                "Электростатика (Постоянный ток)"
            ])

            if topic == "Электростатика (Заряды)":
                q1 = random.randint(2, 6)
                q2 = random.randint(2, 6)
                r = random.randint(1, 3)
                F = self._round_answer(9 * q1 * q2 / (r ** 2))
                q = {
                    "id": f"electro_{i + 1}",
                    "topic": topic,
                    "type": "Закон Кулона",
                    "question": f"Два точечных заряда {q1} нКл и {q2} нКл находятся на расстоянии {r} см. Какова сила взаимодействия? (k=9·10⁹ Н·м²/Кл²)",
                    "correct": str(F),
                    "formula": "F = k·q₁·q₂/r²",
                    "hint": f"9·{q1}·{q2}/{r}² = {F} мН"
                }
            elif topic == "Электростатика (Конденсаторы)":
                C = random.randint(10, 50)
                U = random.randint(100, 300)
                W = self._round_answer(C * U ** 2 / 2 / 10 ** 6)
                q = {
                    "id": f"electro_{i + 1}",
                    "topic": topic,
                    "type": "Энергия конденсатора",
                    "question": f"Конденсатор ёмкостью {C} мкФ заряжен до напряжения {U} В. Какова энергия конденсатора?",
                    "correct": str(W),
                    "formula": "W = CU²/2",
                    "hint": f"{C}·{U}²/2/10⁶ = {W} Дж"
                }
            else:
                R = random.randint(5, 20)
                U = random.randint(10, 50)
                I = self._round_answer(U / R)
                q = {
                    "id": f"electro_{i + 1}",
                    "topic": topic,
                    "type": "Закон Ома",
                    "question": f"Напряжение на участке цепи {U} В, сопротивление {R} Ом. Какова сила тока?",
                    "correct": str(I),
                    "formula": "I = U/R",
                    "hint": f"{U}/{R} = {I} А"
                }

            q["options"] = self._generate_options(q["correct"])
            questions.append(q)

        # ============================================================
        # ОПТИКА — 40 вопросов
        # ============================================================

        for i in range(40):
            topic = random.choice(["Оптика (Линзы)", "Оптика (Оптическая сила)"])

            if topic == "Оптика (Линзы)":
                F = random.randint(10, 30)
                d = random.randint(20, 50)
                if d == F:
                    d = F + random.randint(5, 15)
                f = self._round_answer(1 / (1 / F - 1 / d))
                q = {
                    "id": f"optics_{i + 1}",
                    "topic": topic,
                    "type": "Формула линзы",
                    "question": f"Фокусное расстояние линзы {F} см, предмет находится на расстоянии {d} см. Каково расстояние до изображения?",
                    "correct": str(f),
                    "formula": "1/F = 1/d + 1/f",
                    "hint": f"1/(1/{F}-1/{d}) = {f}"
                }
            else:
                F = random.randint(10, 30)
                D = self._round_answer(1 / (F / 100))
                q = {
                    "id": f"optics_{i + 1}",
                    "topic": topic,
                    "type": "Оптическая сила",
                    "question": f"Фокусное расстояние линзы {F} см. Какова оптическая сила линзы?",
                    "correct": str(D),
                    "formula": "D = 1/F",
                    "hint": f"1/{F / 100} = {D} дптр"
                }

            q["options"] = self._generate_options(q["correct"])
            questions.append(q)

        # ============================================================
        # ЯДЕРНАЯ ФИЗИКА — 30 вопросов
        # ============================================================

        for i in range(30):
            topic = random.choice([
                "Ядерная физика (Строение атома)",
                "Ядерная физика (Радиоактивность)"
            ])

            if topic == "Ядерная физика (Строение атома)":
                Z = random.randint(3, 10)
                N = random.randint(3, 8)
                A = Z + N
                q = {
                    "id": f"nuclear_{i + 1}",
                    "topic": topic,
                    "type": "Состав атома",
                    "question": f"Атом имеет {Z} протонов и {N} нейтронов. Каковы массовое число и заряд ядра?",
                    "correct": f"A={A}, Z={Z}",
                    "formula": "A = Z + N",
                    "hint": f"{Z}+{N}={A}, Z={Z}"
                }
            else:
                A_old = random.randint(210, 230)
                Z_old = random.randint(82, 90)
                q = {
                    "id": f"nuclear_{i + 1}",
                    "topic": topic,
                    "type": "Альфа-распад",
                    "question": f"Ядро {A_old}/{Z_old} претерпевает α-распад. Какие массовое число и заряд у нового ядра?",
                    "correct": f"{A_old - 4}/{Z_old - 2}",
                    "formula": "A→A-4, Z→Z-2",
                    "hint": f"{A_old}-4={A_old - 4}, {Z_old}-2={Z_old - 2}"
                }

            q["options"] = self._generate_options(q["correct"])
            questions.append(q)

        random.shuffle(questions)
        return questions[:400]

    def _create_section_questions(self):
        """Создаёт вопросы для мини-марафонов"""
        sections = {}
        topics = ["Механика", "МКТ", "Термодинамика", "Электростатика", "Оптика", "Ядерная физика"]
        for topic in topics:
            qs = [q for q in self.marathon_questions if topic in q["topic"]]
            while len(qs) < 50:
                q = random.choice(self.marathon_questions).copy()
                q["topic"] = topic
                q["id"] = f"{topic}_{len(qs) + 1}"
                qs.append(q)
            sections[topic] = qs[:50]
        return sections

    def get_next_marathon_question(self, index):
        if index < len(self.marathon_questions):
            return self.marathon_questions[index]
        return None

    def get_next_section_question(self, section, index):
        if section in self.section_questions:
            questions = self.section_questions[section]
            if index < len(questions):
                return questions[index]
        return None

    def get_marathon_total(self):
        return len(self.marathon_questions)

    def get_section_total(self, section):
        if section in self.section_questions:
            return len(self.section_questions[section])
        return 0
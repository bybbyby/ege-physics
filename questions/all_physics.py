import random
import math


class PhysicsGenerator:
    def __init__(self):
        # 5 типов вопросов для каждой подтемы
        self.templates = {
            # ===== МЕХАНИКА =====
            "kinematics_linear": [
                self.kin_lin_type1, self.kin_lin_type2, self.kin_lin_type3,
                self.kin_lin_type4, self.kin_lin_type5
            ],
            "kinematics_circular": [
                self.kin_circ_type1, self.kin_circ_type2, self.kin_circ_type3,
                self.kin_circ_type4, self.kin_circ_type5
            ],
            "ballistics": [
                self.ball_type1, self.ball_type2, self.ball_type3,
                self.ball_type4, self.ball_type5
            ],
            "dynamics": [
                self.dyn_type1, self.dyn_type2, self.dyn_type3,
                self.dyn_type4, self.dyn_type5
            ],
            "conservation": [
                self.cons_type1, self.cons_type2, self.cons_type3,
                self.cons_type4, self.cons_type5
            ],
            "statics": [
                self.stat_type1, self.stat_type2, self.stat_type3,
                self.stat_type4, self.stat_type5
            ],
            "oscillations": [
                self.osc_type1, self.osc_type2, self.osc_type3,
                self.osc_type4, self.osc_type5
            ],

            # ===== МКТ =====
            "mkt_isoprocesses": [
                self.mkt_isop1, self.mkt_isop2, self.mkt_isop3,
                self.mkt_isop4, self.mkt_isop5
            ],
            "mkt_humidity": [
                self.mkt_hum1, self.mkt_hum2, self.mkt_hum3,
                self.mkt_hum4, self.mkt_hum5
            ],

            # ===== ТЕРМОДИНАМИКА =====
            "thermo_first_law": [
                self.thermo_fl1, self.thermo_fl2, self.thermo_fl3,
                self.thermo_fl4, self.thermo_fl5
            ],
            "thermo_efficiency": [
                self.thermo_eff1, self.thermo_eff2, self.thermo_eff3,
                self.thermo_eff4, self.thermo_eff5
            ],

            # ===== ЭЛЕКТРОСТАТИКА =====
            "electro_charges": [
                self.elec_ch1, self.elec_ch2, self.elec_ch3,
                self.elec_ch4, self.elec_ch5
            ],
            "electro_field": [
                self.elec_f1, self.elec_f2, self.elec_f3,
                self.elec_f4, self.elec_f5
            ],
            "electro_capacitors": [
                self.elec_cap1, self.elec_cap2, self.elec_cap3,
                self.elec_cap4, self.elec_cap5
            ],
            "electro_dc": [
                self.elec_dc1, self.elec_dc2, self.elec_dc3,
                self.elec_dc4, self.elec_dc5
            ],
            "electro_ac": [
                self.elec_ac1, self.elec_ac2, self.elec_ac3,
                self.elec_ac4, self.elec_ac5
            ],
            "electro_ohm_full": [
                self.elec_ohm1, self.elec_ohm2, self.elec_ohm3,
                self.elec_ohm4, self.elec_ohm5
            ],
            "electro_lorentz": [
                self.elec_lor1, self.elec_lor2, self.elec_lor3,
                self.elec_lor4, self.elec_lor5
            ],
            "electro_ampere": [
                self.elec_amp1, self.elec_amp2, self.elec_amp3,
                self.elec_amp4, self.elec_amp5
            ],
            "electro_flux": [
                self.elec_fl1, self.elec_fl2, self.elec_fl3,
                self.elec_fl4, self.elec_fl5
            ],
            "electro_osc_circuit": [
                self.elec_osc1, self.elec_osc2, self.elec_osc3,
                self.elec_osc4, self.elec_osc5
            ],

            # ===== ОПТИКА =====
            "optics_lenses": [
                self.opt_lens1, self.opt_lens2, self.opt_lens3,
                self.opt_lens4, self.opt_lens5
            ],
            "optics_power": [
                self.opt_pow1, self.opt_pow2, self.opt_pow3,
                self.opt_pow4, self.opt_pow5
            ],
            "optics_interference": [
                self.opt_int1, self.opt_int2, self.opt_int3,
                self.opt_int4, self.opt_int5
            ],
            "optics_diffraction": [
                self.opt_diff1, self.opt_diff2, self.opt_diff3,
                self.opt_diff4, self.opt_diff5
            ],

            # ===== ЯДЕРНАЯ ФИЗИКА =====
            "nuclear_atom": [
                self.nuc_at1, self.nuc_at2, self.nuc_at3,
                self.nuc_at4, self.nuc_at5
            ],
            "nuclear_radioactivity": [
                self.nuc_rad1, self.nuc_rad2, self.nuc_rad3,
                self.nuc_rad4, self.nuc_rad5
            ],
            "nuclear_reactions": [
                self.nuc_react1, self.nuc_react2, self.nuc_react3,
                self.nuc_react4, self.nuc_react5
            ],
            "nuclear_binding": [
                self.nuc_bind1, self.nuc_bind2, self.nuc_bind3,
                self.nuc_bind4, self.nuc_bind5
            ],
        }

        # Кэш для вопросов
        self.question_cache = {}

    def _round_answer(self, value):
        """Округляет число до 2 знаков после запятой"""
        if isinstance(value, (int, float)):
            return round(value, 2)
        return value

    def _generate_options(self, correct, min_val=0):
        """Генерирует 4 варианта ответа"""
        if isinstance(correct, (int, float)):
            wrong = []
            attempts = 0
            while len(wrong) < 3 and attempts < 50:
                deviation = random.choice([-3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3])
                if isinstance(correct, float):
                    w = round(correct + deviation, 1)
                else:
                    w = correct + random.randint(-3, 3)
                if w != correct and w not in wrong and w > min_val:
                    wrong.append(w)
                attempts += 1

            while len(wrong) < 3:
                if isinstance(correct, float):
                    w = round(correct + random.uniform(-5, 5), 1)
                else:
                    w = correct + random.randint(-5, 5)
                if w != correct and w not in wrong and w > min_val:
                    wrong.append(w)

            answers = wrong + [correct]
            random.shuffle(answers)
            return [str(x) for x in answers]
        else:
            return ["Да", "Нет", "Зависит", "Недостаточно данных"]

    def get_next_question(self, topic, question_index):
        """
        Генерирует следующий вопрос по индексу
        """
        if topic not in self.templates:
            return None

        type_index = (question_index // 10) % 5
        type_subindex = question_index % 10

        if type_index >= len(self.templates[topic]):
            return None

        gen_func = self.templates[topic][type_index]
        qid = f"{topic}_{type_index}_{type_subindex}"
        question = gen_func(qid)

        return question

    def get_total_questions(self, topic):
        """Возвращает общее количество вопросов для темы (50)"""
        if topic in self.templates:
            return 50
        return 0

    # ============ ВСЕ МЕТОДЫ ГЕНЕРАЦИИ ВОПРОСОВ ============

    # ----- Кинематика (прямолинейная) -----
    def kin_lin_type1(self, qid):
        a = random.randint(1, 5)
        v0 = random.randint(0, 10)
        t = random.randint(2, 8)
        v = self._round_answer(v0 + a * t)
        return {
            "id": qid,
            "topic": "Кинематика (прямолинейное)",
            "type": "Скорость",
            "question": f"Тело движется равноускоренно с ускорением {a} м/с². Начальная скорость {v0} м/с. Какова скорость через {t} с?",
            "options": self._generate_options(v),
            "correct": str(v),
            "formula": "v = v₀ + at",
            "hint": f"{v0} + {a}·{t} = {v}"
        }

    def kin_lin_type2(self, qid):
        a = random.randint(1, 4)
        v0 = random.randint(0, 8)
        t = random.randint(2, 6)
        s = self._round_answer(v0 * t + (a * t * t) / 2)
        return {
            "id": qid,
            "topic": "Кинематика (прямолинейное)",
            "type": "Путь",
            "question": f"Тело движется равноускоренно с ускорением {a} м/с². Начальная скорость {v0} м/с. Какой путь пройдёт тело за {t} с?",
            "options": self._generate_options(s),
            "correct": str(s),
            "formula": "s = v₀t + at²/2",
            "hint": f"{v0}·{t} + {a}·{t}²/2 = {s}"
        }

    def kin_lin_type3(self, qid):
        v0 = random.randint(2, 8)
        v = random.randint(12, 20)
        a = random.randint(1, 4)
        t = (v - v0) / a
        return {
            "id": qid,
            "topic": "Кинематика (прямолинейное)",
            "type": "Время",
            "question": f"Тело увеличило скорость с {v0} м/с до {v} м/с с ускорением {a} м/с². Сколько времени длилось движение?",
            "options": self._generate_options(t),
            "correct": str(t),
            "formula": "t = (v - v₀)/a",
            "hint": f"({v} - {v0})/{a} = {t}"
        }

    def kin_lin_type4(self, qid):
        v0 = random.randint(2, 8)
        v = random.randint(10, 18)
        t = random.randint(2, 5)
        a = (v - v0) / t
        return {
            "id": qid,
            "topic": "Кинематика (прямолинейное)",
            "type": "Ускорение",
            "question": f"Тело увеличило скорость с {v0} м/с до {v} м/с за {t} с. Каково ускорение тела?",
            "options": self._generate_options(a),
            "correct": str(a),
            "formula": "a = (v - v₀)/t",
            "hint": f"({v} - {v0})/{t} = {a}"
        }

    def kin_lin_type5(self, qid):
        v = random.randint(10, 20)
        a = random.randint(2, 5)
        s = (v * v) / (2 * a)
        return {
            "id": qid,
            "topic": "Кинематика (прямолинейное)",
            "type": "Тормозной путь",
            "question": f"Автомобиль движется со скоростью {v} м/с и начинает тормозить с ускорением {a} м/с². Каков тормозной путь?",
            "options": self._generate_options(s),
            "correct": str(s),
            "formula": "s = v²/(2a)",
            "hint": f"{v}²/(2·{a}) = {s}"
        }

    # ----- Кинематика (криволинейная) -----
    def kin_circ_type1(self, qid):
        R = random.randint(2, 10)
        T = random.randint(2, 6)
        v = round(2 * math.pi * R / T, 1)
        return {
            "id": qid,
            "topic": "Кинематика (криволинейное)",
            "type": "Линейная скорость",
            "question": f"Тело движется по окружности радиусом {R} м с периодом {T} с. Какова линейная скорость?",
            "options": self._generate_options(v, 0.5),
            "correct": str(v),
            "formula": "v = 2πR/T",
            "hint": f"2·3.14·{R}/{T} = {v}"
        }

    def kin_circ_type2(self, qid):
        R = random.randint(2, 8)
        v = random.randint(5, 15)
        omega = round(v / R, 1)
        return {
            "id": qid,
            "topic": "Кинематика (криволинейное)",
            "type": "Угловая скорость",
            "question": f"Тело движется по окружности радиусом {R} м с линейной скоростью {v} м/с. Какова угловая скорость?",
            "options": self._generate_options(omega, 0.5),
            "correct": str(omega),
            "formula": "ω = v/R",
            "hint": f"{v}/{R} = {omega}"
        }

    def kin_circ_type3(self, qid):
        R = random.randint(2, 8)
        v = random.randint(4, 12)
        a = round(v * v / R, 1)
        return {
            "id": qid,
            "topic": "Кинематика (криволинейное)",
            "type": "Центростремительное ускорение",
            "question": f"Тело движется по окружности радиусом {R} м со скоростью {v} м/с. Каково центростремительное ускорение?",
            "options": self._generate_options(a, 0.5),
            "correct": str(a),
            "formula": "a = v²/R",
            "hint": f"{v}²/{R} = {a}"
        }

    def kin_circ_type4(self, qid):
        R = random.randint(3, 10)
        v = random.randint(5, 15)
        T = round(2 * math.pi * R / v, 1)
        return {
            "id": qid,
            "topic": "Кинематика (криволинейное)",
            "type": "Период",
            "question": f"Тело движется по окружности радиусом {R} м с линейной скоростью {v} м/с. Каков период обращения?",
            "options": self._generate_options(T, 0.5),
            "correct": str(T),
            "formula": "T = 2πR/v",
            "hint": f"2·3.14·{R}/{v} = {T}"
        }

    def kin_circ_type5(self, qid):
        T = random.randint(2, 8)
        nu = round(1 / T, 2)
        return {
            "id": qid,
            "topic": "Кинематика (криволинейное)",
            "type": "Частота",
            "question": f"Период обращения тела по окружности составляет {T} с. Какова частота обращения?",
            "options": self._generate_options(nu, 0.01),
            "correct": str(nu),
            "formula": "ν = 1/T",
            "hint": f"1/{T} = {nu}"
        }

    # ----- Баллистика -----
    def ball_type1(self, qid):
        v0 = random.randint(10, 30)
        angle = random.choice([30, 45, 60])
        g = 9.8
        s = self._round_answer(v0 * t + (a * t * t) / 2)
        return {
            "id": qid,
            "topic": "Баллистика",
            "type": "Дальность полёта",
            "question": f"Тело брошено со скоростью {v0} м/с под углом {angle}° к горизонту. Какова дальность полёта? (g=9.8 м/с²)",
            "options": self._generate_options(L, 1),
            "correct": str(L),
            "formula": "L = v₀²·sin(2α)/g",
            "hint": f"{v0}²·sin({2 * angle}°)/9.8 = {L}"
        }

    def ball_type2(self, qid):
        v0 = random.randint(10, 25)
        angle = random.choice([30, 45, 60])
        g = 9.8
        t = round(2 * v0 * math.sin(math.radians(angle)) / g, 1)
        return {
            "id": qid,
            "topic": "Баллистика",
            "type": "Время полёта",
            "question": f"Тело брошено со скоростью {v0} м/с под углом {angle}° к горизонту. Сколько времени тело будет в полёте? (g=9.8 м/с²)",
            "options": self._generate_options(t, 0.5),
            "correct": str(t),
            "formula": "t = 2v₀·sin(α)/g",
            "hint": f"2·{v0}·sin({angle}°)/9.8 = {t}"
        }

    def ball_type3(self, qid):
        v0 = random.randint(10, 25)
        angle = random.choice([30, 45, 60])
        g = 9.8
        h = round(v0 ** 2 * math.sin(math.radians(angle)) ** 2 / (2 * g), 1)
        return {
            "id": qid,
            "topic": "Баллистика",
            "type": "Максимальная высота",
            "question": f"Тело брошено со скоростью {v0} м/с под углом {angle}° к горизонту. Какова максимальная высота подъёма? (g=9.8 м/с²)",
            "options": self._generate_options(h, 0.5),
            "correct": str(h),
            "formula": "H = v₀²·sin²(α)/(2g)",
            "hint": f"{v0}²·sin²({angle}°)/(2·9.8) = {h}"
        }

    def ball_type4(self, qid):
        v0 = random.randint(10, 25)
        angle = random.choice([30, 45, 60])
        g = 9.8
        t = round(v0 * math.sin(math.radians(angle)) / g, 1)
        return {
            "id": qid,
            "topic": "Баллистика",
            "type": "Время подъёма",
            "question": f"Тело брошено со скоростью {v0} м/с под углом {angle}° к горизонту. Сколько времени тело поднимается? (g=9.8 м/с²)",
            "options": self._generate_options(t, 0.5),
            "correct": str(t),
            "formula": "t_под = v₀·sin(α)/g",
            "hint": f"{v0}·sin({angle}°)/9.8 = {t}"
        }

    def ball_type5(self, qid):
        v0 = random.randint(10, 25)
        angle = random.choice([30, 45, 60])
        vx = round(v0 * math.cos(math.radians(angle)), 1)
        return {
            "id": qid,
            "topic": "Баллистика",
            "type": "Скорость в верхней точке",
            "question": f"Тело брошено со скоростью {v0} м/с под углом {angle}° к горизонту. Какова скорость тела в верхней точке траектории?",
            "options": self._generate_options(vx, 0.5),
            "correct": str(vx),
            "formula": "v_верх = v₀·cos(α)",
            "hint": f"{v0}·cos({angle}°) = {vx}"
        }

    # ----- Динамика -----
    def dyn_type1(self, qid):
        m = random.randint(2, 10)
        F = random.randint(10, 50)
        a = round(F / m, 1)
        return {
            "id": qid,
            "topic": "Динамика",
            "type": "Ускорение",
            "question": f"На тело массой {m} кг действует сила {F} Н. Какое ускорение приобретает тело?",
            "options": self._generate_options(a, 0.5),
            "correct": str(a),
            "formula": "a = F/m",
            "hint": f"{F}/{m} = {a}"
        }

    def dyn_type2(self, qid):
        m = random.randint(2, 8)
        mu = round(random.uniform(0.1, 0.5), 1)
        g = 9.8
        F_tr = round(mu * m * g, 1)
        return {
            "id": qid,
            "topic": "Динамика",
            "type": "Сила трения",
            "question": f"Тело массой {m} кг движется по горизонтальной поверхности. Коэффициент трения μ = {mu}. Какова сила трения? (g=9.8 м/с²)",
            "options": self._generate_options(F_tr, 1),
            "correct": str(F_tr),
            "formula": "F_тр = μ·m·g",
            "hint": f"{mu}·{m}·9.8 = {F_tr}"
        }

    def dyn_type3(self, qid):
        m = random.randint(2, 10)
        a = random.choice([0, 1, 2, 3])
        g = 9.8
        if a == 0:
            P = round(m * g, 1)
            desc = "покоится или движется равномерно"
            hint = f"{m}·9.8 = {P}"
        else:
            direction = random.choice(['вверх', 'вниз'])
            if direction == 'вверх':
                P = round(m * (g + a), 1)
                desc = f"поднимается вверх с ускорением {a} м/с²"
                hint = f"{m}·(9.8+{a}) = {P}"
            else:
                P = round(m * (g - a), 1)
                desc = f"опускается вниз с ускорением {a} м/с²"
                hint = f"{m}·(9.8-{a}) = {P}"
        return {
            "id": qid,
            "topic": "Динамика",
            "type": "Вес тела",
            "question": f"Тело массой {m} кг {desc}. Каков вес тела? (g=9.8 м/с²)",
            "options": self._generate_options(P, 5),
            "correct": str(P),
            "formula": "P = m(g ± a)",
            "hint": hint
        }

    def dyn_type4(self, qid):
        alpha = random.choice([30, 45, 60])
        g = 9.8
        a = round(g * math.sin(math.radians(alpha)), 1)
        return {
            "id": qid,
            "topic": "Динамика",
            "type": "Ускорение на наклонной",
            "question": f"Тело скользит по наклонной плоскости с углом {alpha}° (трения нет). Каково ускорение тела? (g=9.8 м/с²)",
            "options": self._generate_options(a, 0.5),
            "correct": str(a),
            "formula": "a = g·sin(α)",
            "hint": f"9.8·sin({alpha}°) = {a}"
        }

    def dyn_type5(self, qid):
        k = random.randint(50, 200)
        x = round(random.uniform(0.1, 0.5), 2)
        F = round(k * x, 1)
        return {
            "id": qid,
            "topic": "Динамика",
            "type": "Сила упругости",
            "question": f"Пружина жёсткостью {k} Н/м растянута на {x} м. Какова сила упругости?",
            "options": self._generate_options(F, 5),
            "correct": str(F),
            "formula": "F = k·x",
            "hint": f"{k}·{x} = {F}"
        }

    # ----- Законы сохранения -----
    def cons_type1(self, qid):
        m1 = random.randint(2, 8)
        v1 = random.randint(3, 10)
        m2 = random.randint(2, 8)
        v_after = round((m1 * v1) / (m1 + m2), 1)
        return {
            "id": qid,
            "topic": "Законы сохранения",
            "type": "Импульс (неупругое)",
            "question": f"Тело массой {m1} кг движется со скоростью {v1} м/с и сталкивается с неподвижным телом массой {m2} кг. Какова скорость тел после абсолютно неупругого удара?",
            "options": self._generate_options(v_after, 0.5),
            "correct": str(v_after),
            "formula": "m₁v₁ = (m₁+m₂)v",
            "hint": f"({m1}·{v1})/({m1}+{m2}) = {v_after}"
        }

    def cons_type2(self, qid):
        m1 = random.randint(2, 6)
        v1 = random.randint(4, 10)
        m2 = random.randint(2, 6)
        v1_after = round((m1 - m2) * v1 / (m1 + m2), 1)
        return {
            "id": qid,
            "topic": "Законы сохранения",
            "type": "Импульс (упругое)",
            "question": f"Тело массой {m1} кг движется со скоростью {v1} м/с и упруго сталкивается с неподвижным телом массой {m2} кг. Какова скорость первого тела после удара?",
            "options": self._generate_options(v1_after, 0.1),
            "correct": str(v1_after),
            "formula": "v₁' = (m₁-m₂)·v₁/(m₁+m₂)",
            "hint": f"({m1}-{m2})·{v1}/({m1}+{m2}) = {v1_after}"
        }

    def cons_type3(self, qid):
        m = random.randint(2, 8)
        v = random.randint(3, 10)
        E = round((m * v * v) / 2, 1)
        return {
            "id": qid,
            "topic": "Законы сохранения",
            "type": "Кинетическая энергия",
            "question": f"Тело массой {m} кг движется со скоростью {v} м/с. Какова кинетическая энергия тела?",
            "options": self._generate_options(E, 5),
            "correct": str(E),
            "formula": "E_k = mv²/2",
            "hint": f"{m}·{v}²/2 = {E}"
        }

    def cons_type4(self, qid):
        m = random.randint(2, 8)
        h = random.randint(2, 10)
        g = 9.8
        E = round(m * g * h, 1)
        return {
            "id": qid,
            "topic": "Законы сохранения",
            "type": "Потенциальная энергия",
            "question": f"Тело массой {m} кг поднято на высоту {h} м. Какова потенциальная энергия тела? (g=9.8 м/с²)",
            "options": self._generate_options(E, 20),
            "correct": str(E),
            "formula": "E_p = mgh",
            "hint": f"{m}·9.8·{h} = {E}"
        }

    def cons_type5(self, qid):
        h = random.randint(5, 15)
        g = 9.8
        v = round(math.sqrt(2 * g * h), 1)
        return {
            "id": qid,
            "topic": "Законы сохранения",
            "type": "ЗСЭ",
            "question": f"Тело падает с высоты {h} м (без начальной скорости). Какова скорость тела у поверхности земли? (g=9.8 м/с²)",
            "options": self._generate_options(v, 5),
            "correct": str(v),
            "formula": "v = √(2gh)",
            "hint": f"√(2·9.8·{h}) = {v}"
        }

    # ----- Статика -----
    def stat_type1(self, qid):
        V = random.randint(2, 10)
        rho = 1000
        g = 9.8
        F_A = round(rho * g * V / 1000, 1)
        return {
            "id": qid,
            "topic": "Статика и гидростатика",
            "type": "Сила Архимеда",
            "question": f"Тело объёмом {V} л полностью погружено в воду (ρ=1000 кг/м³). Какова сила Архимеда?",
            "options": self._generate_options(F_A, 5),
            "correct": str(F_A),
            "formula": "F_A = ρ·g·V",
            "hint": f"1000·9.8·{V / 1000} = {F_A}"
        }

    def stat_type2(self, qid):
        rho = 1000
        h = random.randint(1, 10)
        g = 9.8
        P = round(rho * g * h, 1)
        return {
            "id": qid,
            "topic": "Статика и гидростатика",
            "type": "Давление жидкости",
            "question": f"На глубине {h} м давление воды составляет? (ρ=1000 кг/м³, g=9.8 м/с²)",
            "options": self._generate_options(P, 5000),
            "correct": str(P),
            "formula": "P = ρ·g·h",
            "hint": f"1000·9.8·{h} = {P}"
        }

    def stat_type3(self, qid):
        m = random.randint(200, 800)
        V = random.randint(200, 800)
        rho_body = round(m / V, 1)
        will_float = rho_body < 1000
        return {
            "id": qid,
            "topic": "Статика и гидростатика",
            "type": "Условие плавания",
            "question": f"Тело массой {m} г имеет объём {V} см³. Будет ли оно плавать в воде? (ρ_воды=1000 кг/м³)",
            "options": ["Да", "Нет", "Зависит от температуры", "Недостаточно данных"],
            "correct": "Да" if will_float else "Нет",
            "formula": "ρ_тела = m/V",
            "hint": f"ρ_тела = {m}/{V} = {rho_body} кг/м³ {'<' if will_float else '>'} 1000 → {'плавает' if will_float else 'тонет'}"
        }

    def stat_type4(self, qid):
        F = random.randint(10, 40)
        d = random.randint(1, 5)
        M = F * d
        return {
            "id": qid,
            "topic": "Статика и гидростатика",
            "type": "Момент силы",
            "question": f"К рычагу приложена сила {F} Н на расстоянии {d} м от оси вращения. Каков момент силы?",
            "options": self._generate_options(M, 10),
            "correct": str(M),
            "formula": "M = F·d",
            "hint": f"{F}·{d} = {M}"
        }

    def stat_type5(self, qid):
        F1 = random.randint(10, 30)
        d1 = random.randint(1, 4)
        d2 = random.randint(1, 4)
        F2 = round(F1 * d1 / d2, 1)
        return {
            "id": qid,
            "topic": "Статика и гидростатика",
            "type": "Рычаг",
            "question": f"На левое плечо рычага длиной {d1} м действует сила {F1} Н. Какую силу нужно приложить к правому плечу длиной {d2} м для равновесия?",
            "options": self._generate_options(F2, 2),
            "correct": str(F2),
            "formula": "F₁·d₁ = F₂·d₂",
            "hint": f"{F1}·{d1}/{d2} = {F2}"
        }

    # ----- Колебания -----
    def osc_type1(self, qid):
        m = random.randint(1, 5)
        k = random.randint(50, 200)
        T = round(2 * math.pi * math.sqrt(m / k), 2)
        return {
            "id": qid,
            "topic": "Колебания и волны",
            "type": "Период пружинного",
            "question": f"Груз массой {m} кг подвешен на пружине жёсткостью {k} Н/м. Каков период колебаний?",
            "options": self._generate_options(T, 0.1),
            "correct": str(T),
            "formula": "T = 2π·√(m/k)",
            "hint": f"2·3.14·√({m}/{k}) = {T}"
        }

    def osc_type2(self, qid):
        m = random.randint(1, 4)
        k = random.randint(50, 180)
        nu = round(1 / (2 * math.pi * math.sqrt(m / k)), 2)
        return {
            "id": qid,
            "topic": "Колебания и волны",
            "type": "Частота пружинного",
            "question": f"Груз массой {m} кг подвешен на пружине жёсткостью {k} Н/м. Какова частота колебаний?",
            "options": self._generate_options(nu, 0.1),
            "correct": str(nu),
            "formula": "ν = 1/(2π·√(m/k))",
            "hint": f"1/(2·3.14·√({m}/{k})) = {nu}"
        }

    def osc_type3(self, qid):
        L = random.randint(1, 5)
        g = 9.8
        T = round(2 * math.pi * math.sqrt(L / g), 2)
        return {
            "id": qid,
            "topic": "Колебания и волны",
            "type": "Период математического",
            "question": f"Математический маятник имеет длину {L} м. Каков период колебаний? (g=9.8 м/с²)",
            "options": self._generate_options(T, 0.5),
            "correct": str(T),
            "formula": "T = 2π·√(L/g)",
            "hint": f"2·3.14·√({L}/9.8) = {T}"
        }

    def osc_type4(self, qid):
        L = random.randint(1, 4)
        g = 9.8
        nu = round(1 / (2 * math.pi * math.sqrt(L / g)), 2)
        return {
            "id": qid,
            "topic": "Колебания и волны",
            "type": "Частота математического",
            "question": f"Математический маятник имеет длину {L} м. Какова частота колебаний? (g=9.8 м/с²)",
            "options": self._generate_options(nu, 0.1),
            "correct": str(nu),
            "formula": "ν = 1/(2π·√(L/g))",
            "hint": f"1/(2·3.14·√({L}/9.8)) = {nu}"
        }

    def osc_type5(self, qid):
        k = random.randint(50, 150)
        A = round(random.uniform(0.1, 0.3), 2)
        E = round((k * A * A) / 2, 1)
        return {
            "id": qid,
            "topic": "Колебания и волны",
            "type": "Энергия колебаний",
            "question": f"Пружинный маятник имеет жёсткость {k} Н/м и амплитуду колебаний {A} м. Какова полная энергия колебаний?",
            "options": self._generate_options(E, 0.5),
            "correct": str(E),
            "formula": "E = kA²/2",
            "hint": f"{k}·{A}²/2 = {E}"
        }

    # ============ МКТ ============
    def mkt_isop1(self, qid):
        P1 = random.randint(1, 5)
        V1 = random.randint(2, 8)
        V2 = random.randint(1, 6)
        P2 = round(P1 * V1 / V2, 1)
        return {
            "id": qid,
            "topic": "МКТ (Изопроцессы)",
            "type": "Изотермический",
            "question": f"Газ находится под давлением {P1} атм при объёме {V1} л. При изотермическом расширении объём увеличился до {V2} л. Каким стало давление?",
            "options": self._generate_options(P2, 0.5),
            "correct": str(P2),
            "formula": "P₁V₁ = P₂V₂",
            "hint": f"{P1}·{V1}/{V2} = {P2}"
        }

    def mkt_isop2(self, qid):
        V1 = random.randint(2, 6)
        T1 = random.randint(300, 400)
        T2 = random.randint(400, 500)
        V2 = round(V1 * T2 / T1, 1)
        return {
            "id": qid,
            "topic": "МКТ (Изопроцессы)",
            "type": "Изобарный",
            "question": f"Газ при температуре {T1} К занимает объём {V1} л. При изобарном нагревании температура стала {T2} К. Каким стал объём?",
            "options": self._generate_options(V2, 1),
            "correct": str(V2),
            "formula": "V₁/T₁ = V₂/T₂",
            "hint": f"{V1}·{T2}/{T1} = {V2}"
        }

    def mkt_isop3(self, qid):
        P1 = random.randint(1, 4)
        T1 = random.randint(300, 400)
        T2 = random.randint(400, 500)
        P2 = round(P1 * T2 / T1, 1)
        return {
            "id": qid,
            "topic": "МКТ (Изопроцессы)",
            "type": "Изохорный",
            "question": f"Газ при температуре {T1} К имеет давление {P1} атм. При изохорном нагревании температура стала {T2} К. Каким стало давление?",
            "options": self._generate_options(P2, 0.5),
            "correct": str(P2),
            "formula": "P₁/T₁ = P₂/T₂",
            "hint": f"{P1}·{T2}/{T1} = {P2}"
        }

    def mkt_isop4(self, qid):
        P = random.randint(1, 3)
        V = random.randint(2, 6)
        T = random.randint(300, 400)
        n = round(P * V / (0.082 * T), 2)
        return {
            "id": qid,
            "topic": "МКТ (Изопроцессы)",
            "type": "Уравнение состояния",
            "question": f"Газ при давлении {P} атм, объёме {V} л и температуре {T} К. Какое количество вещества (моль) содержится в газе? (R=0.082 л·атм/(моль·К))",
            "options": self._generate_options(n, 0.01),
            "correct": str(n),
            "formula": "PV = nRT",
            "hint": f"{P}·{V}/(0.082·{T}) = {n}"
        }

    def mkt_isop5(self, qid):
        P1 = random.randint(1, 3)
        V1 = random.randint(2, 5)
        T1 = random.randint(300, 400)
        P2 = random.randint(2, 4)
        T2 = random.randint(400, 500)
        V2 = round(P1 * V1 * T2 / (P2 * T1), 1)
        return {
            "id": qid,
            "topic": "МКТ (Изопроцессы)",
            "type": "Объединённый закон",
            "question": f"Газ при давлении {P1} атм, объёме {V1} л и температуре {T1} К переходит в состояние с давлением {P2} атм и температурой {T2} К. Каким стал объём?",
            "options": self._generate_options(V2, 0.5),
            "correct": str(V2),
            "formula": "P₁V₁/T₁ = P₂V₂/T₂",
            "hint": f"{P1}·{V1}·{T2}/({P2}·{T1}) = {V2}"
        }

    def mkt_hum1(self, qid):
        rho = random.randint(10, 25)
        rho_nas = random.randint(20, 30)
        phi = round(rho / rho_nas * 100, 1)
        return {
            "id": qid,
            "topic": "МКТ (Влажность)",
            "type": "Относительная влажность",
            "question": f"Абсолютная влажность воздуха составляет {rho} г/м³. Плотность насыщенного пара при этой температуре {rho_nas} г/м³. Какова относительная влажность?",
            "options": self._generate_options(phi, 10),
            "correct": str(phi),
            "formula": "φ = ρ/ρ_нас · 100%",
            "hint": f"{rho}/{rho_nas}·100 = {phi}%"
        }

    def mkt_hum2(self, qid):
        T = random.randint(15, 25)
        T_ros = T - random.randint(5, 15)
        return {
            "id": qid,
            "topic": "МКТ (Влажность)",
            "type": "Точка росы",
            "question": f"Температура воздуха {T}°C. Точка росы {T_ros}°C. Что произойдёт при охлаждении воздуха до {T_ros - 2}°C?",
            "options": ["Образуется роса", "Влажность уменьшится", "Ничего не произойдёт", "Влажность станет 0%"],
            "correct": "Образуется роса",
            "formula": "T_росы — температура конденсации",
            "hint": f"При охлаждении ниже точки росы ({T_ros}°C) пар конденсируется"
        }

    def mkt_hum3(self, qid):
        phi = random.randint(40, 80)
        rho_nas = random.randint(20, 30)
        rho = round(phi * rho_nas / 100, 1)
        return {
            "id": qid,
            "topic": "МКТ (Влажность)",
            "type": "Абсолютная влажность",
            "question": f"Относительная влажность воздуха {phi}%. Плотность насыщенного пара {rho_nas} г/м³. Какова абсолютная влажность?",
            "options": self._generate_options(rho, 5),
            "correct": str(rho),
            "formula": "ρ = φ·ρ_нас/100%",
            "hint": f"{phi}·{rho_nas}/100 = {rho}"
        }

    def mkt_hum4(self, qid):
        phi1 = random.randint(60, 90)
        T1 = random.randint(10, 20)
        T2 = random.randint(25, 35)
        return {
            "id": qid,
            "topic": "МКТ (Влажность)",
            "type": "Изменение влажности",
            "question": f"При температуре {T1}°C относительная влажность {phi1}%. Как изменится влажность при нагревании до {T2}°C?",
            "options": ["Уменьшится", "Увеличится", "Не изменится", "Станет 100%"],
            "correct": "Уменьшится",
            "formula": "При нагревании φ ↓ (ρ_нас ↑)",
            "hint": f"С ростом температуры плотность насыщенного пара увеличивается"
        }

    def mkt_hum5(self, qid):
        V = random.randint(50, 100)
        rho = random.randint(10, 20)
        m = round(rho * V / 1000, 2)
        return {
            "id": qid,
            "topic": "МКТ (Влажность)",
            "type": "Масса пара",
            "question": f"В комнате объёмом {V} м³ абсолютная влажность составляет {rho} г/м³. Какова масса водяного пара в комнате?",
            "options": self._generate_options(m, 0.01),
            "correct": str(m),
            "formula": "m = ρ·V",
            "hint": f"{rho}·{V}/1000 = {m} кг"
        }

    # ============ ТЕРМОДИНАМИКА ============
    def thermo_fl1(self, qid):
        P = random.randint(100, 300)
        V1 = random.randint(2, 5)
        V2 = random.randint(6, 10)
        A = round(P * (V2 - V1), 1)
        return {
            "id": qid,
            "topic": "Термодинамика (Первый закон)",
            "type": "Работа газа",
            "question": f"Газ расширяется при постоянном давлении {P} кПа, объём увеличивается с {V1} л до {V2} л. Какую работу совершает газ?",
            "options": self._generate_options(A, 100),
            "correct": str(A),
            "formula": "A = P·ΔV",
            "hint": f"{P}·({V2}-{V1}) = {A}"
        }

    def thermo_fl2(self, qid):
        Q = random.randint(500, 2000)
        A = random.randint(200, 800)
        delta_U = Q - A
        return {
            "id": qid,
            "topic": "Термодинамика (Первый закон)",
            "type": "Изменение внутренней энергии",
            "question": f"Газ получил количество теплоты {Q} Дж и совершил работу {A} Дж. Как изменилась внутренняя энергия газа?",
            "options": self._generate_options(delta_U, 100),
            "correct": str(delta_U),
            "formula": "ΔU = Q - A",
            "hint": f"{Q} - {A} = {delta_U}"
        }

    def thermo_fl3(self, qid):
        m = random.randint(2, 8)
        c = 4200
        delta_T = random.randint(10, 30)
        Q = round(m * c * delta_T, 1)
        return {
            "id": qid,
            "topic": "Термодинамика (Первый закон)",
            "type": "Количество теплоты",
            "question": f"Воду массой {m} кг нагревают на {delta_T}°C. Какое количество теплоты необходимо? (c=4200 Дж/(кг·°C))",
            "options": self._generate_options(Q, 10000),
            "correct": str(Q),
            "formula": "Q = cmΔT",
            "hint": f"4200·{m}·{delta_T} = {Q}"
        }

    def thermo_fl4(self, qid):
        return {
            "id": qid,
            "topic": "Термодинамика (Первый закон)",
            "type": "Адиабатный процесс",
            "question": "Газ адиабатно расширяется. Как изменилась внутренняя энергия?",
            "options": ["Уменьшилась", "Увеличилась", "Не изменилась", "Стала 0"],
            "correct": "Уменьшилась",
            "formula": "ΔU = -A (Q=0)",
            "hint": "При адиабатном расширении T↓ → U↓"
        }

    def thermo_fl5(self, qid):
        n = random.randint(1, 3)
        delta_T = random.randint(100, 200)
        R = 8.31
        Q = round(n * R * delta_T / 2, 1)
        return {
            "id": qid,
            "topic": "Термодинамика (Первый закон)",
            "type": "Изохорный нагрев",
            "question": f"{n} моль одноатомного газа нагревают в изохорном процессе на {delta_T} К. Какое количество теплоты получил газ? (R=8.31 Дж/(моль·К))",
            "options": self._generate_options(Q, 100),
            "correct": str(Q),
            "formula": "Q = (3/2)nRΔT",
            "hint": f"1.5·{n}·8.31·{delta_T} = {Q}"
        }

    def thermo_eff1(self, qid):
        Q1 = random.randint(500, 1000)
        Q2 = random.randint(200, 400)
        eta = round((Q1 - Q2) / Q1 * 100, 1)
        return {
            "id": qid,
            "topic": "Термодинамика (КПД)",
            "type": "КПД двигателя",
            "question": f"Тепловой двигатель получает {Q1} Дж теплоты и отдаёт {Q2} Дж холодильнику. Каков КПД двигателя?",
            "options": self._generate_options(eta, 10),
            "correct": str(eta),
            "formula": "η = (Q₁-Q₂)/Q₁ · 100%",
            "hint": f"({Q1}-{Q2})/{Q1}·100 = {eta}%"
        }

    def thermo_eff2(self, qid):
        T1 = random.randint(500, 800)
        T2 = random.randint(300, 400)
        eta = round((1 - T2 / T1) * 100, 1)
        return {
            "id": qid,
            "topic": "Термодинамика (КПД)",
            "type": "Цикл Карно",
            "question": f"Температура нагревателя {T1} К, холодильника {T2} К. Каков максимальный КПД теплового двигателя?",
            "options": self._generate_options(eta, 10),
            "correct": str(eta),
            "formula": "η = (1 - T₂/T₁)·100%",
            "hint": f"(1-{T2}/{T1})·100 = {eta}%"
        }

    def thermo_eff3(self, qid):
        Q1 = random.randint(1000, 2000)
        eta = random.randint(25, 45)
        A = round(Q1 * eta / 100, 1)
        return {
            "id": qid,
            "topic": "Термодинамика (КПД)",
            "type": "Полезная работа",
            "question": f"Тепловой двигатель с КПД {eta}% получает от нагревателя {Q1} Дж теплоты. Какую полезную работу совершает двигатель?",
            "options": self._generate_options(A, 200),
            "correct": str(A),
            "formula": "A = η·Q₁/100%",
            "hint": f"{eta}·{Q1}/100 = {A}"
        }

    def thermo_eff4(self, qid):
        Q1 = random.randint(800, 1500)
        eta = random.randint(20, 40)
        Q2 = round(Q1 * (100 - eta) / 100, 1)
        return {
            "id": qid,
            "topic": "Термодинамика (КПД)",
            "type": "Теплота холодильнику",
            "question": f"Двигатель с КПД {eta}% получает от нагревателя {Q1} Дж. Сколько теплоты отдаётся холодильнику?",
            "options": self._generate_options(Q2, 300),
            "correct": str(Q2),
            "formula": "Q₂ = Q₁·(1-η)",
            "hint": f"{Q1}·({100 - eta})/100 = {Q2}"
        }

    def thermo_eff5(self, qid):
        T1_old = 500
        T1_new = 600
        T2 = 300
        eta_old = round((1 - T2 / T1_old) * 100, 1)
        eta_new = round((1 - T2 / T1_new) * 100, 1)
        delta = round(eta_new - eta_old, 1)
        return {
            "id": qid,
            "topic": "Термодинамика (КПД)",
            "type": "Изменение КПД",
            "question": f"Температуру нагревателя увеличили с {T1_old} К до {T1_new} К. Холодильник {T2} К. На сколько % увеличился КПД?",
            "options": self._generate_options(delta, 1),
            "correct": str(delta),
            "formula": "Δη = (1-T₂/T₁_нов)·100% - (1-T₂/T₁_стар)·100%",
            "hint": f"({eta_new}-{eta_old}) = {delta}%"
        }

    # ============ ЭЛЕКТРОСТАТИКА ============
    def elec_ch1(self, qid):
        q1 = random.randint(2, 6)
        q2 = random.randint(2, 6)
        r = random.randint(1, 3)
        F = round(9 * q1 * q2 / (r ** 2), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Заряды)",
            "type": "Закон Кулона",
            "question": f"Два точечных заряда {q1} нКл и {q2} нКл находятся на расстоянии {r} см. Какова сила взаимодействия? (k=9·10⁹ Н·м²/Кл²)",
            "options": self._generate_options(F, 0.1),
            "correct": str(F),
            "formula": "F = k·q₁·q₂/r²",
            "hint": f"9·{q1}·{q2}/{r}² = {F} мН"
        }

    def elec_ch2(self, qid):
        q = random.randint(2, 6)
        r = random.randint(1, 3)
        E = round(9 * q / (r ** 2), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Заряды)",
            "type": "Напряжённость поля",
            "question": f"Точечный заряд {q} нКл. Какова напряжённость электрического поля на расстоянии {r} см? (k=9·10⁹ Н·м²/Кл²)",
            "options": self._generate_options(E, 0.1),
            "correct": str(E),
            "formula": "E = k·q/r²",
            "hint": f"9·{q}/{r}² = {E} кВ/м"
        }

    def elec_ch3(self, qid):
        q = random.randint(2, 6)
        r = random.randint(1, 3)
        phi = round(9 * q / r, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Заряды)",
            "type": "Потенциал",
            "question": f"Точечный заряд {q} нКл. Каков потенциал электрического поля на расстоянии {r} см? (k=9·10⁹ Н·м²/Кл²)",
            "options": self._generate_options(phi, 100),
            "correct": str(phi),
            "formula": "φ = k·q/r",
            "hint": f"9·{q}/{r} = {phi} В"
        }

    def elec_ch4(self, qid):
        q = random.randint(2, 5)
        U = random.randint(100, 500)
        A = round(q * U / 1000, 2)
        return {
            "id": qid,
            "topic": "Электростатика (Заряды)",
            "type": "Работа поля",
            "question": f"Заряд {q} мКл перемещается в электрическом поле с напряжением {U} В. Какую работу совершает поле?",
            "options": self._generate_options(A, 0.01),
            "correct": str(A),
            "formula": "A = q·U",
            "hint": f"{q}·{U}/1000 = {A} Дж"
        }

    def elec_ch5(self, qid):
        q = random.randint(2, 5)
        phi = random.randint(100, 300)
        W = round(q * phi / 1000, 2)
        return {
            "id": qid,
            "topic": "Электростатика (Заряды)",
            "type": "Энергия заряда",
            "question": f"Заряд {q} мКл находится в точке поля с потенциалом {phi} В. Какова потенциальная энергия заряда?",
            "options": self._generate_options(W, 0.01),
            "correct": str(W),
            "formula": "W = q·φ",
            "hint": f"{q}·{phi}/1000 = {W} Дж"
        }

    def elec_f1(self, qid):
        U = random.randint(100, 500)
        d = random.randint(1, 5)
        E = round(U / d, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Напряжённость)",
            "type": "Поле между пластинами",
            "question": f"Между пластинами конденсатора напряжение {U} В, расстояние {d} см. Какова напряжённость поля?",
            "options": self._generate_options(E, 20),
            "correct": str(E),
            "formula": "E = U/d",
            "hint": f"{U}/{d} = {E} В/см"
        }

    def elec_f2(self, qid):
        E = random.randint(100, 300)
        q = random.randint(2, 6)
        F = round(E * q / 1000, 2)
        return {
            "id": qid,
            "topic": "Электростатика (Напряжённость)",
            "type": "Сила в поле",
            "question": f"Напряжённость поля {E} В/м. Какую силу испытывает заряд {q} мКл?",
            "options": self._generate_options(F, 0.01),
            "correct": str(F),
            "formula": "F = q·E",
            "hint": f"{E}·{q}/1000 = {F} Н"
        }

    def elec_f3(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Напряжённость)",
            "type": "Линии поля",
            "question": "Как направлены линии напряжённости электрического поля положительного заряда?",
            "options": ["От заряда", "К заряду", "По окружности", "Перпендикулярно радиусу"],
            "correct": "От заряда",
            "formula": "E = k·q/r²",
            "hint": "Линии E выходят из положительного заряда"
        }

    def elec_f4(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Напряжённость)",
            "type": "Суперпозиция",
            "question": "В некоторой точке поля напряжённость создаётся двумя одинаковыми положительными зарядами. Как найти результирующую напряжённость?",
            "options": ["Векторная сумма", "Алгебраическая сумма", "Разность", "Произведение"],
            "correct": "Векторная сумма",
            "formula": "E = E₁ + E₂ (векторно)",
            "hint": "Напряжённость складывается по правилу параллелограмма"
        }

    def elec_f5(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Напряжённость)",
            "type": "Эквипотенциальные поверхности",
            "question": "Как направлены линии напряжённости относительно эквипотенциальных поверхностей?",
            "options": ["Перпендикулярно", "Параллельно", "Под углом 45°", "Не имеют связи"],
            "correct": "Перпендикулярно",
            "formula": "E ⟂ φ = const",
            "hint": "Линии E всегда перпендикулярны эквипотенциальным поверхностям"
        }

    def elec_cap1(self, qid):
        q = random.randint(2, 6)
        U = random.randint(100, 500)
        C = round(q / U * 10 ** 6, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Конденсаторы)",
            "type": "Ёмкость",
            "question": f"Конденсатор имеет заряд {q} мКл и напряжение {U} В. Какова ёмкость конденсатора?",
            "options": self._generate_options(C, 1),
            "correct": str(C),
            "formula": "C = q/U",
            "hint": f"{q}·10⁻³/{U}·10⁶ = {C} мкФ"
        }

    def elec_cap2(self, qid):
        C = random.randint(10, 50)
        U = random.randint(100, 300)
        W = round(C * U ** 2 / 2 / 10 ** 6, 2)
        return {
            "id": qid,
            "topic": "Электростатика (Конденсаторы)",
            "type": "Энергия",
            "question": f"Конденсатор ёмкостью {C} мкФ заряжен до напряжения {U} В. Какова энергия конденсатора?",
            "options": self._generate_options(W, 0.01),
            "correct": str(W),
            "formula": "W = CU²/2",
            "hint": f"{C}·{U}²/2/10⁶ = {W} Дж"
        }

    def elec_cap3(self, qid):
        C1 = random.randint(10, 30)
        C2 = random.randint(10, 30)
        C = round(C1 * C2 / (C1 + C2), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Конденсаторы)",
            "type": "Последовательное",
            "question": f"Два конденсатора ёмкостью {C1} мкФ и {C2} мкФ соединены последовательно. Какова общая ёмкость?",
            "options": self._generate_options(C, 5),
            "correct": str(C),
            "formula": "1/C = 1/C₁ + 1/C₂",
            "hint": f"{C1}·{C2}/({C1}+{C2}) = {C}"
        }

    def elec_cap4(self, qid):
        C1 = random.randint(10, 30)
        C2 = random.randint(10, 30)
        C = C1 + C2
        return {
            "id": qid,
            "topic": "Электростатика (Конденсаторы)",
            "type": "Параллельное",
            "question": f"Два конденсатора ёмкостью {C1} мкФ и {C2} мкФ соединены параллельно. Какова общая ёмкость?",
            "options": self._generate_options(C, 20),
            "correct": str(C),
            "formula": "C = C₁ + C₂",
            "hint": f"{C1}+{C2} = {C}"
        }

    def elec_cap5(self, qid):
        S = random.randint(100, 300)
        d = random.randint(1, 3)
        C = round(8.85 * S / d / 10, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Конденсаторы)",
            "type": "Плоский конденсатор",
            "question": f"Площадь пластин конденсатора {S} см², расстояние {d} мм (вакуум). Какова ёмкость? (ε₀=8.85·10⁻¹² Ф/м)",
            "options": self._generate_options(C, 10),
            "correct": str(C),
            "formula": "C = ε₀·S/d",
            "hint": f"8.85·{S}·10⁻⁴/{d}·10⁻³·10¹² = {C} пФ"
        }

    def elec_dc1(self, qid):
        U = random.randint(10, 50)
        R = random.randint(5, 20)
        I = round(U / R, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Постоянный ток)",
            "type": "Закон Ома",
            "question": f"Напряжение на участке цепи {U} В, сопротивление {R} Ом. Какова сила тока?",
            "options": self._generate_options(I, 0.5),
            "correct": str(I),
            "formula": "I = U/R",
            "hint": f"{U}/{R} = {I} А"
        }

    def elec_dc2(self, qid):
        U = random.randint(10, 50)
        I = random.randint(2, 8)
        P = U * I
        return {
            "id": qid,
            "topic": "Электростатика (Постоянный ток)",
            "type": "Мощность",
            "question": f"Напряжение на участке {U} В, сила тока {I} А. Какова мощность тока?",
            "options": self._generate_options(P, 20),
            "correct": str(P),
            "formula": "P = U·I",
            "hint": f"{U}·{I} = {P} Вт"
        }

    def elec_dc3(self, qid):
        P = random.randint(20, 80)
        t = random.randint(10, 30)
        A = P * t
        return {
            "id": qid,
            "topic": "Электростатика (Постоянный ток)",
            "type": "Работа тока",
            "question": f"Мощность тока {P} Вт. Какую работу совершает ток за {t} с?",
            "options": self._generate_options(A, 100),
            "correct": str(A),
            "formula": "A = P·t",
            "hint": f"{P}·{t} = {A} Дж"
        }

    def elec_dc4(self, qid):
        R1 = random.randint(5, 15)
        R2 = random.randint(5, 15)
        R = R1 + R2
        return {
            "id": qid,
            "topic": "Электростатика (Постоянный ток)",
            "type": "Последовательное",
            "question": f"Два резистора {R1} Ом и {R2} Ом соединены последовательно. Каково общее сопротивление?",
            "options": self._generate_options(R, 10),
            "correct": str(R),
            "formula": "R = R₁ + R₂",
            "hint": f"{R1}+{R2} = {R}"
        }

    def elec_dc5(self, qid):
        R1 = random.randint(10, 30)
        R2 = random.randint(10, 30)
        R = round(R1 * R2 / (R1 + R2), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Постоянный ток)",
            "type": "Параллельное",
            "question": f"Два резистора {R1} Ом и {R2} Ом соединены параллельно. Каково общее сопротивление?",
            "options": self._generate_options(R, 5),
            "correct": str(R),
            "formula": "1/R = 1/R₁ + 1/R₂",
            "hint": f"{R1}·{R2}/({R1}+{R2}) = {R}"
        }

    def elec_ac1(self, qid):
        U_max = random.randint(200, 400)
        U = round(U_max / 1.41, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Переменный ток)",
            "type": "Действующее значение",
            "question": f"Амплитудное значение напряжения {U_max} В. Каково действующее значение?",
            "options": self._generate_options(U, 100),
            "correct": str(U),
            "formula": "U_д = U_м/√2",
            "hint": f"{U_max}/1.41 = {U}"
        }

    def elec_ac2(self, qid):
        T = random.randint(2, 10)
        nu = round(1 / T, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Переменный ток)",
            "type": "Частота",
            "question": f"Период переменного тока {T} с. Какова частота тока?",
            "options": self._generate_options(nu, 0.1),
            "correct": str(nu),
            "formula": "ν = 1/T",
            "hint": f"1/{T} = {nu} Гц"
        }

    def elec_ac3(self, qid):
        L = random.randint(1, 5)
        nu = random.randint(50, 100)
        XL = round(2 * 3.14 * nu * L / 1000, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Переменный ток)",
            "type": "Индуктивное сопротивление",
            "question": f"Катушка индуктивности {L} мГн в цепи переменного тока частотой {nu} Гц. Каково индуктивное сопротивление?",
            "options": self._generate_options(XL, 0.1),
            "correct": str(XL),
            "formula": "X_L = 2πνL",
            "hint": f"2·3.14·{nu}·{L}/1000 = {XL} Ом"
        }

    def elec_ac4(self, qid):
        C = random.randint(10, 50)
        nu = random.randint(50, 100)
        XC = round(1 / (2 * 3.14 * nu * C * 10 ** -6), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Переменный ток)",
            "type": "Ёмкостное сопротивление",
            "question": f"Конденсатор ёмкостью {C} мкФ в цепи переменного тока частотой {nu} Гц. Каково ёмкостное сопротивление?",
            "options": self._generate_options(XC, 20),
            "correct": str(XC),
            "formula": "X_C = 1/(2πνC)",
            "hint": f"1/(2·3.14·{nu}·{C}·10⁻⁶) = {XC}"
        }

    def elec_ac5(self, qid):
        U = random.randint(100, 250)
        I = random.randint(2, 6)
        cos_fi = round(random.uniform(0.7, 0.95), 2)
        P = round(U * I * cos_fi, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Переменный ток)",
            "type": "Мощность",
            "question": f"Напряжение в цепи {U} В, ток {I} А, cos φ = {cos_fi}. Какова активная мощность?",
            "options": self._generate_options(P, 100),
            "correct": str(P),
            "formula": "P = U·I·cos φ",
            "hint": f"{U}·{I}·{cos_fi} = {P} Вт"
        }

    def elec_ohm1(self, qid):
        E = random.randint(10, 30)
        R = random.randint(5, 15)
        r = random.randint(1, 3)
        I = round(E / (R + r), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Закон Ома для полной цепи)",
            "type": "Закон Ома",
            "question": f"ЭДС источника {E} В, внешнее сопротивление {R} Ом, внутреннее сопротивление {r} Ом. Какова сила тока в цепи?",
            "options": self._generate_options(I, 0.5),
            "correct": str(I),
            "formula": "I = E/(R+r)",
            "hint": f"{E}/({R}+{r}) = {I} А"
        }

    def elec_ohm2(self, qid):
        E = random.randint(10, 30)
        R = random.randint(5, 15)
        r = random.randint(1, 3)
        U = round(E * R / (R + r), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Закон Ома для полной цепи)",
            "type": "Напряжение",
            "question": f"ЭДС источника {E} В, внешнее сопротивление {R} Ом, внутреннее сопротивление {r} Ом. Каково напряжение на внешнем участке?",
            "options": self._generate_options(U, 5),
            "correct": str(U),
            "formula": "U = E·R/(R+r)",
            "hint": f"{E}·{R}/({R}+{r}) = {U} В"
        }

    def elec_ohm3(self, qid):
        E = random.randint(10, 30)
        r = random.randint(1, 3)
        I_kz = round(E / r, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Закон Ома для полной цепи)",
            "type": "Ток КЗ",
            "question": f"ЭДС источника {E} В, внутреннее сопротивление {r} Ом. Каков ток короткого замыкания?",
            "options": self._generate_options(I_kz, 5),
            "correct": str(I_kz),
            "formula": "I_кз = E/r",
            "hint": f"{E}/{r} = {I_kz} А"
        }

    def elec_ohm4(self, qid):
        R = random.randint(5, 15)
        r = random.randint(1, 3)
        eta = round(R / (R + r) * 100, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Закон Ома для полной цепи)",
            "type": "КПД источника",
            "question": f"Внешнее сопротивление {R} Ом, внутреннее {r} Ом. Каков КПД источника тока?",
            "options": self._generate_options(eta, 50),
            "correct": str(eta),
            "formula": "η = R/(R+r)·100%",
            "hint": f"{R}/({R}+{r})·100 = {eta}%"
        }

    def elec_ohm5(self, qid):
        E = random.randint(10, 20)
        R = random.randint(5, 15)
        r = random.randint(1, 3)
        P = round(E ** 2 * R / (R + r) ** 2, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Закон Ома для полной цепи)",
            "type": "Полезная мощность",
            "question": f"ЭДС {E} В, внешнее сопротивление {R} Ом, внутреннее {r} Ом. Какова полезная мощность источника?",
            "options": self._generate_options(P, 5),
            "correct": str(P),
            "formula": "P = E²·R/(R+r)²",
            "hint": f"{E}²·{R}/({R}+{r})² = {P} Вт"
        }

    def elec_lor1(self, qid):
        q = random.randint(1, 3)
        v = random.randint(10, 30)
        B = random.randint(1, 4)
        F = round(q * v * B / 10, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Сила Лоренца)",
            "type": "Сила Лоренца",
            "question": f"Заряд {q} мКл влетает в магнитное поле {B} Тл со скоростью {v} км/с перпендикулярно полю. Какова сила Лоренца?",
            "options": self._generate_options(F, 0.1),
            "correct": str(F),
            "formula": "F = qvB·sin α",
            "hint": f"{q}·10⁻³·{v}·10³·{B} = {F} Н"
        }

    def elec_lor2(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Сила Лоренца)",
            "type": "Направление",
            "question": "Положительный заряд движется в магнитном поле. Как определить направление силы Лоренца?",
            "options": ["Правило левой руки", "Правило правой руки", "Правило буравчика", "Правило Ленца"],
            "correct": "Правило левой руки",
            "formula": "F = q[v×B]",
            "hint": "Для положительного заряда — правило левой руки"
        }

    def elec_lor3(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Сила Лоренца)",
            "type": "Работа",
            "question": "Какую работу совершает сила Лоренца при движении заряда в магнитном поле?",
            "options": ["0 Дж", "qvB·s", "qU", "mv²/2"],
            "correct": "0 Дж",
            "formula": "A = 0",
            "hint": "Сила Лоренца всегда перпендикулярна скорости"
        }

    def elec_lor4(self, qid):
        m = random.randint(1, 5)
        v = random.randint(1, 5)
        q = random.randint(1, 3)
        B = random.randint(1, 4)
        R = round(m * v / (q * B), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Сила Лоренца)",
            "type": "Радиус",
            "question": f"Частица массой {m}·10⁻²⁷ кг, зарядом {q}·10⁻¹⁹ Кл влетает в поле {B} Тл со скоростью {v}·10⁶ м/с перпендикулярно полю. Каков радиус траектории?",
            "options": self._generate_options(R, 0.5),
            "correct": str(R),
            "formula": "R = mv/(qB)",
            "hint": f"{m}·{v}/({q}·{B}) = {R}"
        }

    def elec_lor5(self, qid):
        m = random.randint(1, 5)
        q = random.randint(1, 3)
        B = random.randint(1, 4)
        T = round(2 * 3.14 * m / (q * B), 2)
        return {
            "id": qid,
            "topic": "Электростатика (Сила Лоренца)",
            "type": "Период",
            "question": f"Частица с зарядом {q}·10⁻¹⁹ Кл, массой {m}·10⁻²⁷ кг движется в поле {B} Тл. Каков период обращения?",
            "options": self._generate_options(T, 0.01),
            "correct": str(T),
            "formula": "T = 2πm/(qB)",
            "hint": f"2·3.14·{m}/({q}·{B}) = {T}"
        }

    def elec_amp1(self, qid):
        I = random.randint(2, 8)
        L = random.randint(10, 30)
        B = random.randint(1, 4)
        F = round(I * L * B / 100, 2)
        return {
            "id": qid,
            "topic": "Электростатика (Сила Ампера)",
            "type": "Сила Ампера",
            "question": f"Проводник длиной {L} см с током {I} А находится в поле {B} Тл перпендикулярно. Какова сила Ампера?",
            "options": self._generate_options(F, 0.01),
            "correct": str(F),
            "formula": "F = BIL·sin α",
            "hint": f"{B}·{I}·{L}/100 = {F} Н"
        }

    def elec_amp2(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Сила Ампера)",
            "type": "Направление",
            "question": "Как определить направление силы Ампера?",
            "options": ["Правило левой руки", "Правило правой руки", "Правило Ленца", "Правило буравчика"],
            "correct": "Правило левой руки",
            "formula": "F = BIL·sin α",
            "hint": "Сила Ампера — правило левой руки"
        }

    def elec_amp3(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Сила Ампера)",
            "type": "Взаимодействие",
            "question": "Как взаимодействуют два параллельных проводника с токами одного направления?",
            "options": ["Притягиваются", "Отталкиваются", "Не взаимодействуют", "Вращаются"],
            "correct": "Притягиваются",
            "formula": "F = μ₀I₁I₂L/(2πr)",
            "hint": "Токи одного направления притягиваются"
        }

    def elec_amp4(self, qid):
        I = random.randint(2, 8)
        r = random.randint(5, 15)
        B = round(2 * I / r, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Сила Ампера)",
            "type": "Магнитная индукция",
            "question": f"По прямому проводнику течёт ток {I} А. Какова индукция поля на расстоянии {r} см? (μ₀=4π·10⁻⁷ Гн/м)",
            "options": self._generate_options(B, 0.1),
            "correct": str(B),
            "formula": "B = μ₀I/(2πr)",
            "hint": f"2·{I}/{r} = {B} мкТл"
        }

    def elec_amp5(self, qid):
        I = random.randint(2, 6)
        S = random.randint(10, 30)
        pm = round(I * S / 10000, 4)
        return {
            "id": qid,
            "topic": "Электростатика (Сила Ампера)",
            "type": "Магнитный момент",
            "question": f"Круговой виток с током {I} А имеет площадь {S} см². Каков магнитный момент витка?",
            "options": self._generate_options(pm, 0.001),
            "correct": str(pm),
            "formula": "p_m = I·S",
            "hint": f"{I}·{S}·10⁻⁴ = {pm} А·м²"
        }

    def elec_fl1(self, qid):
        B = random.randint(1, 4)
        S = random.randint(10, 30)
        F = round(B * S / 100, 2)
        return {
            "id": qid,
            "topic": "Электростатика (Магнитный поток)",
            "type": "Магнитный поток",
            "question": f"Магнитная индукция {B} Тл, площадь {S} см², угол между нормалью и полем 0°. Каков магнитный поток?",
            "options": self._generate_options(F, 0.01),
            "correct": str(F),
            "formula": "Φ = B·S·cos α",
            "hint": f"{B}·{S}/100 = {F} Вб"
        }

    def elec_fl2(self, qid):
        dF = random.randint(1, 5)
        dt = random.randint(1, 5)
        E = round(dF / dt, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Магнитный поток)",
            "type": "ЭДС индукции",
            "question": f"Магнитный поток изменился на {dF} Вб за {dt} с. Какова ЭДС индукции?",
            "options": self._generate_options(E, 0.1),
            "correct": str(E),
            "formula": "ε = ΔΦ/Δt",
            "hint": f"{dF}/{dt} = {E} В"
        }

    def elec_fl3(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Магнитный поток)",
            "type": "Правило Ленца",
            "question": "Согласно правилу Ленца, индукционный ток направлен так, чтобы...",
            "options": ["Компенсировать изменение потока", "Увеличить поток", "Не влиять на поток", "Уничтожить поле"],
            "correct": "Компенсировать изменение потока",
            "formula": "ε = -ΔΦ/Δt",
            "hint": "Индукционный ток препятствует причине, его вызывающей"
        }

    def elec_fl4(self, qid):
        N = random.randint(10, 30)
        dF = random.randint(1, 3)
        dt = random.randint(1, 5)
        E = round(N * dF / dt, 1)
        return {
            "id": qid,
            "topic": "Электростатика (Магнитный поток)",
            "type": "Закон Фарадея",
            "question": f"В катушке из {N} витков поток изменился на {dF} Вб за {dt} с. Какова ЭДС индукции?",
            "options": self._generate_options(E, 5),
            "correct": str(E),
            "formula": "ε = N·ΔΦ/Δt",
            "hint": f"{N}·{dF}/{dt} = {E} В"
        }

    def elec_fl5(self, qid):
        I = random.randint(2, 6)
        F = round(random.uniform(0.1, 0.5), 2)
        L = round(F / I, 3)
        return {
            "id": qid,
            "topic": "Электростатика (Магнитный поток)",
            "type": "Индуктивность",
            "question": f"При токе {I} А магнитный поток в катушке {F} Вб. Какова индуктивность катушки?",
            "options": self._generate_options(L, 0.01),
            "correct": str(L),
            "formula": "L = Φ/I",
            "hint": f"{F}/{I} = {L} Гн"
        }

    def elec_osc1(self, qid):
        L = random.randint(1, 10)
        C = random.randint(10, 50)
        T = round(2 * 3.14 * (L * C * 10 ** -9) ** 0.5, 4)
        return {
            "id": qid,
            "topic": "Электростатика (Колебательный контур)",
            "type": "Период",
            "question": f"Индуктивность {L} мГн, ёмкость {C} мкФ. Каков период колебаний в контуре?",
            "options": self._generate_options(T, 0.0001),
            "correct": str(T),
            "formula": "T = 2π√(LC)",
            "hint": f"2·3.14·√({L}·10⁻³·{C}·10⁻⁶) = {T} с"
        }

    def elec_osc2(self, qid):
        L = random.randint(1, 10)
        C = random.randint(10, 50)
        nu = round(1 / (2 * 3.14 * (L * C * 10 ** -9) ** 0.5), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Колебательный контур)",
            "type": "Частота",
            "question": f"Индуктивность {L} мГн, ёмкость {C} мкФ. Какова частота колебаний в контуре?",
            "options": self._generate_options(nu, 100),
            "correct": str(nu),
            "formula": "ν = 1/(2π√(LC))",
            "hint": f"1/(2·3.14·√({L}·10⁻³·{C}·10⁻⁶)) = {nu} Гц"
        }

    def elec_osc3(self, qid):
        return {
            "id": qid,
            "topic": "Электростатика (Колебательный контур)",
            "type": "Формула Томсона",
            "question": "По какой формуле рассчитывается период колебаний в идеальном колебательном контуре?",
            "options": ["T = 2π√(LC)", "T = 2π√(L/C)", "T = 2π√(C/L)", "T = 1/(2π√(LC))"],
            "correct": "T = 2π√(LC)",
            "formula": "T = 2π√(LC)",
            "hint": "Период пропорционален √(LC)"
        }

    def elec_osc4(self, qid):
        L = random.randint(1, 5)
        I_max = random.randint(2, 6)
        W = round(L * I_max ** 2 / 2, 2)
        return {
            "id": qid,
            "topic": "Электростатика (Колебательный контур)",
            "type": "Энергия",
            "question": f"Индуктивность {L} мГн, максимальный ток {I_max} А. Какова полная энергия колебательного контура?",
            "options": self._generate_options(W, 0.01),
            "correct": str(W),
            "formula": "W = LI²/2",
            "hint": f"{L}·10⁻³·{I_max}²/2 = {W} Дж"
        }

    def elec_osc5(self, qid):
        L = random.randint(1, 10)
        C = random.randint(20, 60)
        f = round(1 / (2 * 3.14 * (L * C * 10 ** -9) ** 0.5), 1)
        return {
            "id": qid,
            "topic": "Электростатика (Колебательный контур)",
            "type": "Резонансная частота",
            "question": f"Контур с L={L} мГн и C={C} мкФ. Какова резонансная частота?",
            "options": self._generate_options(f, 100),
            "correct": str(f),
            "formula": "f = 1/(2π√(LC))",
            "hint": f"1/(2·3.14·√({L}·10⁻³·{C}·10⁻⁶)) = {f} Гц"
        }

    # ============ ОПТИКА ============
    def opt_lens1(self, qid):
        F = random.randint(10, 30)
        d = random.randint(20, 50)
        f = round(1 / (1 / F - 1 / d), 1)
        return {
            "id": qid,
            "topic": "Оптика (Линзы)",
            "type": "Формула линзы",
            "question": f"Фокусное расстояние линзы {F} см, предмет находится на расстоянии {d} см. Каково расстояние до изображения?",
            "options": self._generate_options(f, 5),
            "correct": str(f),
            "formula": "1/F = 1/d + 1/f",
            "hint": f"1/(1/{F}-1/{d}) = {f}"
        }

    def opt_lens2(self, qid):
        f = random.randint(10, 30)
        d = random.randint(20, 50)
        G = round(f / d, 2)
        return {
            "id": qid,
            "topic": "Оптика (Линзы)",
            "type": "Увеличение",
            "question": f"Изображение находится на расстоянии {f} см, предмет на {d} см. Каково линейное увеличение?",
            "options": self._generate_options(G, 0.1),
            "correct": str(G),
            "formula": "Γ = f/d",
            "hint": f"{f}/{d} = {G}"
        }

    def opt_lens3(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Линзы)",
            "type": "Типы линз",
            "question": "Какая линза называется собирающей?",
            "options": ["Толще в центре", "Толще по краям", "Плоская", "Вогнутая"],
            "correct": "Толще в центре",
            "formula": "Собирающая линза",
            "hint": "У собирающей линзы края тоньше середины"
        }

    def opt_lens4(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Линзы)",
            "type": "Построение",
            "question": "Какой луч проходит через оптический центр линзы без преломления?",
            "options": ["Луч, проходящий через центр", "Луч, параллельный оси", "Луч, проходящий через фокус",
                        "Все лучи"],
            "correct": "Луч, проходящий через центр",
            "formula": "Луч через центр",
            "hint": "Луч через оптический центр не меняет направления"
        }

    def opt_lens5(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Линзы)",
            "type": "Мнимое изображение",
            "question": "В каком случае собирающая линза даёт мнимое изображение?",
            "options": ["d < F", "d > F", "d = F", "d = 2F"],
            "correct": "d < F",
            "formula": "d < F → мнимое, увеличенное",
            "hint": "Предмет между линзой и фокусом"
        }

    def opt_pow1(self, qid):
        F = random.randint(10, 30)
        D = round(1 / (F / 100), 1)
        return {
            "id": qid,
            "topic": "Оптика (Оптическая сила)",
            "type": "Оптическая сила",
            "question": f"Фокусное расстояние линзы {F} см. Какова оптическая сила линзы?",
            "options": self._generate_options(D, 1),
            "correct": str(D),
            "formula": "D = 1/F",
            "hint": f"1/{F / 100} = {D} дптр"
        }

    def opt_pow2(self, qid):
        D1 = random.randint(2, 5)
        D2 = random.randint(2, 5)
        D = D1 + D2
        return {
            "id": qid,
            "topic": "Оптика (Оптическая сила)",
            "type": "Система линз",
            "question": f"Оптические силы двух линз {D1} дптр и {D2} дптр. Какова оптическая сила системы (вплотную)?",
            "options": self._generate_options(D, 4),
            "correct": str(D),
            "formula": "D = D₁ + D₂",
            "hint": f"{D1}+{D2} = {D} дптр"
        }

    def opt_pow3(self, qid):
        D = random.randint(2, 5)
        F = round(1 / D * 100, 1)
        return {
            "id": qid,
            "topic": "Оптика (Оптическая сила)",
            "type": "Фокусное расстояние",
            "question": f"Оптическая сила линзы {D} дптр. Каково фокусное расстояние?",
            "options": self._generate_options(F, 10),
            "correct": str(F),
            "formula": "F = 1/D",
            "hint": f"1/{D}·100 = {F} см"
        }

    def opt_pow4(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Оптическая сила)",
            "type": "Близорукость",
            "question": "Какие линзы используют для коррекции близорукости?",
            "options": ["Рассеивающие", "Собирающие", "Плоские", "Цилиндрические"],
            "correct": "Рассеивающие",
            "formula": "D < 0",
            "hint": "Близорукость исправляют отрицательными линзами"
        }

    def opt_pow5(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Оптическая сила)",
            "type": "Дальнозоркость",
            "question": "Какие линзы используют для коррекции дальнозоркости?",
            "options": ["Собирающие", "Рассеивающие", "Плоские", "Цилиндрические"],
            "correct": "Собирающие",
            "formula": "D > 0",
            "hint": "Дальнозоркость исправляют положительными линзами"
        }

    def opt_int1(self, qid):
        lam = random.randint(400, 700)
        k = random.randint(1, 3)
        delta = round(k * lam / 1000, 2)
        return {
            "id": qid,
            "topic": "Оптика (Интерференция)",
            "type": "Условие максимума",
            "question": f"Длина волны света {lam} нм, разность хода {delta} мкм. Какой порядок интерференционного максимума?",
            "options": [str(k - 1), str(k), str(k + 1), "0"],
            "correct": str(k),
            "formula": "Δ = k·λ",
            "hint": f"{delta * 1000 / lam} = {k}"
        }

    def opt_int2(self, qid):
        lam = random.randint(400, 700)
        k = random.randint(1, 3)
        delta = round((2 * k + 1) * lam / 2000, 2)
        return {
            "id": qid,
            "topic": "Оптика (Интерференция)",
            "type": "Условие минимума",
            "question": f"Длина волны {lam} нм. При какой разности хода будет интерференционный минимум?",
            "options": [f"{round((2 * k - 1) * lam / 2000, 2)} мкм", f"{delta} мкм", f"{round(k * lam / 1000, 2)} мкм",
                        "0"],
            "correct": f"{delta} мкм",
            "formula": "Δ = (2k+1)·λ/2",
            "hint": f"Δ = (2·{k}+1)·{lam}/2000 = {delta} мкм"
        }

    def opt_int3(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Интерференция)",
            "type": "Когерентность",
            "question": "Какие волны называются когерентными?",
            "options": ["С постоянной разностью фаз", "С одинаковой частотой", "С одинаковой амплитудой",
                        "С одинаковой длиной волны"],
            "correct": "С постоянной разностью фаз",
            "formula": "Δφ = const",
            "hint": "Когерентные волны имеют постоянную разность фаз"
        }

    def opt_int4(self, qid):
        lam = random.randint(400, 700)
        L = random.randint(1, 3)
        d = round(random.uniform(0.1, 0.5), 2)
        delta_x = round(lam * L / (d * 1000), 2)
        return {
            "id": qid,
            "topic": "Оптика (Интерференция)",
            "type": "Ширина полосы",
            "question": f"Длина волны {lam} нм, расстояние до экрана {L} м, расстояние между щелями {d} мм. Какова ширина интерференционной полосы?",
            "options": self._generate_options(delta_x, 0.1),
            "correct": str(delta_x),
            "formula": "Δx = λ·L/d",
            "hint": f"{lam}·{L}/{d}·10⁻⁶ = {delta_x} мм"
        }

    def opt_int5(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Интерференция)",
            "type": "Опыт Юнга",
            "question": "В каком опыте впервые наблюдали интерференцию света?",
            "options": ["Опыт Юнга", "Опыт Майкельсона", "Опыт Физо", "Опыт Резерфорда"],
            "correct": "Опыт Юнга",
            "formula": "Две щели",
            "hint": "Томас Юнг, 1801 год"
        }

    def opt_diff1(self, qid):
        d = random.randint(2, 5)
        lam = random.randint(400, 700)
        k = random.randint(1, 3)
        sin_alpha = round(k * lam / (d * 1000), 2)
        return {
            "id": qid,
            "topic": "Оптика (Дифракция)",
            "type": "Условие максимума",
            "question": f"Период решётки {d} мкм, длина волны {lam} нм. sin α для максимума {k}-го порядка равен?",
            "options": self._generate_options(sin_alpha, 0.01),
            "correct": str(sin_alpha),
            "formula": "d·sin α = k·λ",
            "hint": f"{k}·{lam}/{d}·10⁻³ = {sin_alpha}"
        }

    def opt_diff2(self, qid):
        N = random.randint(100, 300)
        k = random.randint(1, 3)
        R = N * k
        return {
            "id": qid,
            "topic": "Оптика (Дифракция)",
            "type": "Разрешающая способность",
            "question": f"Дифракционная решётка имеет {N} штрихов/мм. Какова разрешающая способность для {k}-го порядка?",
            "options": self._generate_options(R, 100),
            "correct": str(R),
            "formula": "R = N·k",
            "hint": f"{N}·{k} = {R}"
        }

    def opt_diff3(self, qid):
        N = random.randint(100, 300)
        d = round(1 / N * 1000, 2)
        return {
            "id": qid,
            "topic": "Оптика (Дифракция)",
            "type": "Период решётки",
            "question": f"Дифракционная решётка имеет {N} штрихов/мм. Каков период решётки?",
            "options": self._generate_options(d, 1),
            "correct": str(d),
            "formula": "d = 1/N",
            "hint": f"1/{N}·1000 = {d} мкм"
        }

    def opt_diff4(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Дифракция)",
            "type": "Типы дифракции",
            "question": "Какая дифракция наблюдается на щели при параллельном пучке света?",
            "options": ["Фраунгофера", "Френеля", "Юнга", "Майкельсона"],
            "correct": "Фраунгофера",
            "formula": "Дифракция в параллельных лучах",
            "hint": "Дифракция Фраунгофера — в параллельных лучах"
        }

    def opt_diff5(self, qid):
        return {
            "id": qid,
            "topic": "Оптика (Дифракция)",
            "type": "Спектральный прибор",
            "question": "Какое свойство дифракционной решётки позволяет использовать её как спектральный прибор?",
            "options": ["Разложение света в спектр", "Увеличение интенсивности", "Сужение пучка", "Поляризация"],
            "correct": "Разложение света в спектр",
            "formula": "d·sin α = k·λ",
            "hint": "Дифракционная решётка даёт спектр"
        }

    # ============ ЯДЕРНАЯ ФИЗИКА ============
    def nuc_at1(self, qid):
        Z = random.randint(3, 10)
        N = random.randint(3, 8)
        A = Z + N
        return {
            "id": qid,
            "topic": "Ядерная физика (Строение атома)",
            "type": "Состав атома",
            "question": f"Атом имеет {Z} протонов и {N} нейтронов. Каковы массовое число и заряд ядра?",
            "options": [f"A={A}, Z={Z}", f"A={Z + N}, Z={Z}", f"A={A}, Z={Z + N}", f"A={Z}, Z={N}"],
            "correct": f"A={A}, Z={Z}",
            "formula": "A = Z + N",
            "hint": f"A = {Z}+{N} = {A}, Z = {Z}"
        }

    def nuc_at2(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Строение атома)",
            "type": "Модель атома",
            "question": "Кто предложил планетарную модель атома?",
            "options": ["Резерфорд", "Бор", "Томсон", "Резерфорд и Бор"],
            "correct": "Резерфорд",
            "formula": "Ядро + электроны",
            "hint": "Эрнест Резерфорд, 1911"
        }

    def nuc_at3(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Строение атома)",
            "type": "Постулаты Бора",
            "question": "Согласно постулатам Бора, атом излучает энергию...",
            "options": ["При переходе на более низкий уровень", "При переходе на более высокий уровень", "Постоянно",
                        "Только в основном состоянии"],
            "correct": "При переходе на более низкий уровень",
            "formula": "E = hν",
            "hint": "Излучение при переходе с верхнего на нижний уровень"
        }

    def nuc_at4(self, qid):
        Z = random.randint(3, 8)
        E = round(13.6 * Z ** 2, 1)
        return {
            "id": qid,
            "topic": "Ядерная физика (Строение атома)",
            "type": "Энергия ионизации",
            "question": f"Какая энергия ионизации атома с зарядом ядра {Z} (в эВ) для водородоподобного атома?",
            "options": self._generate_options(E, 50),
            "correct": str(E),
            "formula": "E = 13.6·Z² эВ",
            "hint": f"13.6·{Z}² = {E} эВ"
        }

    def nuc_at5(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Строение атома)",
            "type": "Квантовые числа",
            "question": "Сколько электронов может находиться на энергетическом уровне с главным квантовым числом n=3?",
            "options": ["2", "8", "18", "32"],
            "correct": "18",
            "formula": "N = 2n²",
            "hint": "2·3² = 18"
        }

    def nuc_rad1(self, qid):
        A = random.randint(210, 230)
        Z = random.randint(82, 90)
        A_new = A - 4
        Z_new = Z - 2
        return {
            "id": qid,
            "topic": "Ядерная физика (Радиоактивность)",
            "type": "Альфа-распад",
            "question": f"Ядро {A}{Z} претерпевает α-распад. Какие массовое число и заряд у нового ядра?",
            "options": [f"A={A_new}, Z={Z_new}", f"A={A - 4}, Z={Z - 2}", f"A={A}, Z={Z - 2}", f"A={A - 4}, Z={Z}"],
            "correct": f"A={A_new}, Z={Z_new}",
            "formula": "A→A-4, Z→Z-2",
            "hint": f"{A}-4={A_new}, {Z}-2={Z_new}"
        }

    def nuc_rad2(self, qid):
        A = random.randint(50, 100)
        Z = random.randint(25, 45)
        Z_new = Z + 1
        return {
            "id": qid,
            "topic": "Ядерная физика (Радиоактивность)",
            "type": "Бета-распад",
            "question": f"Ядро {A}{Z} претерпевает β⁻-распад. Каков заряд нового ядра?",
            "options": [f"{Z + 1}", f"{Z - 1}", f"{Z}", f"{Z + 2}"],
            "correct": f"{Z_new}",
            "formula": "Z→Z+1",
            "hint": f"При β⁻-распаде Z увеличивается на 1: {Z}+1={Z_new}"
        }

    def nuc_rad3(self, qid):
        T = random.randint(2, 6)
        N0 = random.randint(100, 500)
        t = random.randint(1, 4)
        N = round(N0 * (0.5) ** (t / T), 1)
        return {
            "id": qid,
            "topic": "Ядерная физика (Радиоактивность)",
            "type": "Период полураспада",
            "question": f"Период полураспада изотопа {T} суток. Сколько останется ядер из {N0} через {t} суток?",
            "options": self._generate_options(N, 10),
            "correct": str(N),
            "formula": "N = N₀·(1/2)^(t/T)",
            "hint": f"{N0}·(0.5)^{t / T} = {N}"
        }

    def nuc_rad4(self, qid):
        T = random.randint(3, 8)
        tau = round(T / 0.693, 1)
        return {
            "id": qid,
            "topic": "Ядерная физика (Радиоактивность)",
            "type": "Время жизни",
            "question": f"Период полураспада изотопа {T} суток. Каково среднее время жизни ядра?",
            "options": self._generate_options(tau, 3),
            "correct": str(tau),
            "formula": "τ = T/ln 2",
            "hint": f"{T}/0.693 = {tau}"
        }

    def nuc_rad5(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Радиоактивность)",
            "type": "Виды распада",
            "question": "Какой вид радиоактивного распада не изменяет массовое число ядра?",
            "options": ["Бета-распад", "Альфа-распад", "Гамма-излучение", "Спонтанное деление"],
            "correct": "Бета-распад",
            "formula": "A = const при β-распаде",
            "hint": "При β-распаде A не меняется, меняется Z"
        }

    def nuc_react1(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Ядерные реакции)",
            "type": "Реакция",
            "question": "Что сохраняется в ядерных реакциях?",
            "options": ["Массовое число и заряд", "Масса", "Энергия", "Импульс"],
            "correct": "Массовое число и заряд",
            "formula": "A₁ + A₂ = A₃ + A₄, Z₁ + Z₂ = Z₃ + Z₄",
            "hint": "Сумма A и Z до и после реакции равны"
        }

    def nuc_react2(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Ядерные реакции)",
            "type": "Деление урана",
            "question": "Какая реакция лежит в основе работы ядерного реактора?",
            "options": ["Деление урана", "Синтез", "Распад", "Ионизация"],
            "correct": "Деление урана",
            "formula": "²³⁵U + n → ...",
            "hint": "Цепная реакция деления ²³⁵U"
        }

    def nuc_react3(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Ядерные реакции)",
            "type": "Синтез",
            "question": "Какая реакция является термоядерной?",
            "options": ["Слияние лёгких ядер", "Деление тяжёлых ядер", "Радиоактивный распад", "Фотоэффект"],
            "correct": "Слияние лёгких ядер",
            "formula": "²H + ³H → ⁴He + n",
            "hint": "Термоядерные реакции — синтез лёгких ядер"
        }

    def nuc_react4(self, qid):
        m1 = random.randint(2, 5)
        m2 = random.randint(2, 5)
        m3 = random.randint(3, 6)
        m4 = random.randint(3, 6)
        dm = abs(m1 + m2 - m3 - m4) / 1000
        E = round(dm * 931.5, 1)
        return {
            "id": qid,
            "topic": "Ядерная физика (Ядерные реакции)",
            "type": "Энергия реакции",
            "question": f"В реакции массы: {m1} а.е.м. + {m2} а.е.м. → {m3} а.е.м. + {m4} а.е.м. Какова энергия реакции?",
            "options": self._generate_options(E, 10),
            "correct": str(E),
            "formula": "E = Δm·931.5 МэВ",
            "hint": f"|({m1}+{m2}-{m3}-{m4})|·931.5 = {E} МэВ"
        }

    def nuc_react5(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Ядерные реакции)",
            "type": "Цепная реакция",
            "question": "Что необходимо для осуществления цепной реакции деления?",
            "options": ["Нейтроны", "Электроны", "Протоны", "Альфа-частицы"],
            "correct": "Нейтроны",
            "formula": "n + ²³⁵U → ... + 2-3n",
            "hint": "Цепную реакцию поддерживают нейтроны"
        }

    def nuc_bind1(self, qid):
        Z = random.randint(5, 10)
        N = random.randint(5, 10)
        A = Z + N
        mp = 1.00728
        mn = 1.00867
        my = round(Z * mp + N * mn - random.uniform(0.1, 0.3), 3)
        dm = round(Z * mp + N * mn - my, 3)
        return {
            "id": qid,
            "topic": "Ядерная физика (Энергия связи)",
            "type": "Дефект массы",
            "question": f"Ядро {A}{Z} имеет массу {my} а.е.м. Каков дефект массы? (m_p={mp}, m_n={mn})",
            "options": self._generate_options(dm, 0.001),
            "correct": str(dm),
            "formula": "Δm = Z·m_p + N·m_n - m_я",
            "hint": f"{Z}·{mp}+{N}·{mn}-{my} = {dm}"
        }

    def nuc_bind2(self, qid):
        dm = round(random.uniform(0.1, 0.5), 2)
        E = round(dm * 931.5, 1)
        return {
            "id": qid,
            "topic": "Ядерная физика (Энергия связи)",
            "type": "Энергия связи",
            "question": f"Дефект массы ядра составляет {dm} а.е.м. Какова энергия связи ядра?",
            "options": self._generate_options(E, 50),
            "correct": str(E),
            "formula": "E_св = Δm·931.5 МэВ",
            "hint": f"{dm}·931.5 = {E} МэВ"
        }

    def nuc_bind3(self, qid):
        A = random.randint(20, 50)
        E = round(random.uniform(7, 9), 1)
        E_ud = round(E / A, 3)
        return {
            "id": qid,
            "topic": "Ядерная физика (Энергия связи)",
            "type": "Удельная энергия",
            "question": f"Ядро с массовым числом {A} имеет энергию связи {E} МэВ. Какова удельная энергия связи?",
            "options": self._generate_options(E_ud, 0.01),
            "correct": str(E_ud),
            "formula": "ε = E_св/A",
            "hint": f"{E}/{A} = {E_ud} МэВ/нуклон"
        }

    def nuc_bind4(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Энергия связи)",
            "type": "Максимум",
            "question": "У какого элемента максимальная удельная энергия связи?",
            "options": ["Железо", "Уран", "Водород", "Гелий"],
            "correct": "Железо",
            "formula": "ε_max ≈ 8.8 МэВ (Fe)",
            "hint": "Максимум у ядер средней массы (Fe)"
        }

    def nuc_bind5(self, qid):
        return {
            "id": qid,
            "topic": "Ядерная физика (Энергия связи)",
            "type": "Стабильность",
            "question": "Как связана энергия связи со стабильностью ядра?",
            "options": ["Чем больше E_св, тем стабильнее", "Чем меньше E_св, тем стабильнее", "Не связаны",
                        "Обратная зависимость"],
            "correct": "Чем больше E_св, тем стабильнее",
            "formula": "E_св ↑ → стабильность ↑",
            "hint": "Большая энергия связи — более стабильное ядро"
        }
import streamlit as st


def init_session_state():
    if 'scores' not in st.session_state:
        st.session_state.scores = {
            'respiratory': 0,
            'nervous': 0,
            'cardiovascular': 0,
            'liver': 0,
            'coagulation': 0,
            'renal': 0
        }
    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0


def calculate_respiratory_score():
    st.subheader('1. Респираторный индекс PaO2/FiO2')
    pao2 = st.slider('PaO2 в мм.рт.ст.', 1, 250, 1)
    fio2 = st.slider('FiO2 в %', 21, 100, 21)
    respiratory_index = pao2 / (fio2 / 100)

    if respiratory_index > 400:
        score = 0
    elif 300 < respiratory_index <= 400:
        score = 1
    elif 200 < respiratory_index <= 300:
        score = 2
    elif 100 < respiratory_index <= 200:
        score = 3
    else:
        score = 4

    st.session_state.scores['respiratory'] = score

def calculate_nervous_score():
    st.subheader('2. Шкала комы Глазго (ШКГ)')
    gcs = st.slider('Общий балл ШКГ (3-15)', 3, 15, 15)

    if gcs == 15:
        score = 0
    elif 13 <= gcs <= 14:
        score = 1
    elif 10 <= gcs <= 12:
        score = 2
    elif 6 <= gcs <= 9:
        score = 3
    else:
        score = 4

    st.session_state.scores['nervous'] = score


def calculate_cardiovascular_score():
    st.subheader('3. Сердечно-сосудистая система')
    option = st.selectbox(
        'Выберите вариант',
        ('Норма', 'АДср < 70 мм.рт.ст', 'Допамин ≤ 5 или добутамин в любой дозе',
         'Допамин > 5 или адреналин ≤ 0.1', 'Допамин > 15 или адреналин > 0.1')
    )

    score_map = {
        'Норма': 0,
        'АДср < 70 мм.рт.ст': 1,
        'Допамин ≤ 5 или добутамин в любой дозе': 2,
        'Допамин > 5 или адреналин ≤ 0.1': 3,
        'Допамин > 15 или адреналин > 0.1': 4
    }

    st.session_state.scores['cardiovascular'] = score_map[option]


def calculate_liver_score():
    st.subheader('4. Билирубин в сыворотке крови')
    bilirubin = st.slider('Билирубин (мкмоль/л)', 0, 400, 0)

    if bilirubin < 20:
        score = 0
    elif 20 <= bilirubin <= 32:
        score = 1
    elif 33 <= bilirubin <= 101:
        score = 2
    elif 102 <= bilirubin <= 204:
        score = 3
    else:
        score = 4

    st.session_state.scores['liver'] = score


def calculate_coagulation_score():
    st.subheader('5. Уровень тромбоцитов')
    platelets = st.slider('Тромбоциты (×10⁹/л)', 0, 500, 0)

    if platelets > 150:
        score = 0
    elif 100 < platelets <= 150:
        score = 1
    elif 50 < platelets <= 100:
        score = 2
    elif 20 < platelets <= 50:
        score = 3
    else:
        score = 4

    st.session_state.scores['coagulation'] = score


def calculate_renal_score():
    st.subheader('6. Почечная функция')
    option = st.selectbox(
        'Выберите вариант',
        ('< 110 мкмоль/л', '110-170 мкмоль/л', '171-299 мкмоль/л',
         '300-440 мкмоль/л или диурез < 500 мл/сут',
         '> 440 мкмоль/л или диурез < 200 мл/сут')
    )

    score_map = {
        '< 110 мкмоль/л': 0,
        '110-170 мкмоль/л': 1,
        '171-299 мкмоль/л': 2,
        '300-440 мкмоль/л или диурез < 500 мл/сут': 3,
        '> 440 мкмоль/л или диурез < 200 мл/сут': 4
    }

    st.session_state.scores['renal'] = score_map[option]


def show_results():
    st.header("Результаты оценки SOFA")

    st.session_state.total_score = sum([
        st.session_state.scores['respiratory'],
        st.session_state.scores['nervous'],
        st.session_state.scores['cardiovascular'],
        st.session_state.scores['liver'],
        st.session_state.scores['coagulation'],
        st.session_state.scores['renal']
    ])

    st.subheader(f"Общий балл SOFA: {st.session_state.total_score}")

    if st.session_state.total_score == 0:
        st.success("Нет органной дисфункции")
    elif 1 <= st.session_state.total_score <= 6:
        st.warning("Легкая/умеренная органная дисфункция")
    elif 7 <= st.session_state.total_score <= 11:
        st.error("Тяжелая органная дисфункция")
    else:
        st.error("Крайне тяжелая органная дисфункция (высокий риск летальности)")


def main():
    st.title("Шкала SOFA (Sequential Organ Failure Assessment)")
    init_session_state()

    with st.form("sofa_form"):
        calculate_respiratory_score()
        calculate_nervous_score()
        calculate_cardiovascular_score()
        calculate_liver_score()
        calculate_coagulation_score()
        calculate_renal_score()

        submitted = st.form_submit_button("Рассчитать общий балл SOFA")

    if submitted:
        show_results()

        if st.button("Сбросить все данные"):
            init_session_state()
            st.rerun()


if __name__ == "__main__":
    main()

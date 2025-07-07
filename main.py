import streamlit as st

st.title("Шкала SOFA (Sequential Organ Failure Assessment)")

respiratory_score = 0
nervous_score = 0
cardiovascular_score = 0
liver_score = 0
coagulation_score = 0
renal_score = 0

st.subheader('1. Респираторный индекс PaO2/FiO2')
pao2 = st.slider('PaO2 в мм.рт.ст.', 1, 250, 1)
fio2 = st.slider('FiO2 в %', 21, 100, 21)
respiratory_index = pao2 / (fio2 / 100)

if respiratory_index > 400:
    respiratory_score = 0
elif 300 < respiratory_index <= 400:
    respiratory_score = 1
elif 200 < respiratory_index <= 300:
    respiratory_score = 2
elif 100 < respiratory_index <= 200:
    respiratory_score = 3
elif respiratory_index <= 100:
    respiratory_score = 4

st.write(f"Респираторный индекс: {respiratory_index:.1f} → {respiratory_score} балл(ов)")

st.subheader('2. Шкала комы Глазго (ШКГ)')
gcs = st.slider('Общий балл ШКГ (3-15)', 3, 15, 15)

if gcs == 15:
    nervous_score = 0
elif 13 <= gcs <= 14:
    nervous_score = 1
elif 10 <= gcs <= 12:
    nervous_score = 2
elif 6 <= gcs <= 9:
    nervous_score = 3
elif gcs < 6:
    nervous_score = 4

st.write(f"ШКГ: {gcs} → {nervous_score} балл(ов)")

st.subheader('3. Систолическое АД, мм.рт.ст')
systolic_blood_pressure = st.selectbox('Выберите ответ',
     ('Норма', 'АДср < 70 мм.рт.ст ', 'Допамин ≤ 5 или любая доза добутамина',
      'Допамин > 5 или адреналин ≤ 0.1 или НА ≤ 0.1',
      'Допамин > 15 или адреналин > 0.1 или НА > 0.1'))

if systolic_blood_pressure == 'Норма':
    cardiovascular_score = 0
elif systolic_blood_pressure == 'АДср < 70 мм.рт.ст ':
    cardiovascular_score = 1
elif systolic_blood_pressure == 'Допамин ≤ 5 или любая доза добутамина':
    cardiovascular_score = 2
elif systolic_blood_pressure == 'Допамин > 5 или адреналин ≤ 0.1 или НА ≤ 0.1':
    cardiovascular_score = 3
elif systolic_blood_pressure == 'Допамин > 15 или адреналин > 0.1 или НА > 0.1':
    cardiovascular_score = 4

st.write(f"Сердечно-сосудистая система → {cardiovascular_score} балл(ов)")

st.subheader('4. Билирубин в сыворотке крови')
bilirubin = st.slider('Билирубин (мкмоль/л)', 0, 400, 0)

if bilirubin < 20:
    liver_score = 0
elif 20 <= bilirubin <= 32:
    liver_score = 1
elif 33 <= bilirubin <= 101:
    liver_score = 2
elif 102 <= bilirubin <= 204:
    liver_score = 3
elif bilirubin > 204:
    liver_score = 4

st.write(f"Билирубин: {bilirubin} мкмоль/л → {liver_score} балл(ов)")

st.subheader('5. Уровень тромбоцитов')
platelets = st.slider('Тромбоциты (×10⁹/л)', 0, 500, 0)

if platelets > 150:
    coagulation_score = 0
elif 100 < platelets <= 150:
    coagulation_score = 1
elif 50 < platelets <= 100:
    coagulation_score = 2
elif 20 < platelets <= 50:
    coagulation_score = 3
elif platelets <= 20:
    coagulation_score = 4

st.write(f"Тромбоциты: {platelets}×10⁹/л → {coagulation_score} балл(ов)")

st.subheader('5. Креатинин, мкмоль/л или диурез')
creatinine = st.selectbox('Выберите ответ',
     ('< 110', '110 - 170', '171 - 299',
      '300 - 400 или диурез < 500 мл/сутки',
      '< 440 или диурез < 200 мл/сутки'))

if creatinine == '< 110':
    renal_score = 0
elif creatinine == '110 - 170':
    renal_score = 1
elif creatinine == '171 - 299':
    renal_score = 2
elif creatinine == '300 - 400 или диурез < 500 мл/сутки':
    renal_score = 3
elif creatinine == '< 440 или диурез < 200 мл/сутки':
    renal_score = 4

st.write(f" Почечная функция → {renal_score} балл(ов)")

total_score = respiratory_score + nervous_score + cardiovascular_score + liver_score + coagulation_score + renal_score

st.header("Результаты оценки SOFA")
st.subheader(f"Общий балл SOFA: {total_score}")

if total_score == 0:
    st.success("Нет органной дисфункции")
elif 1 <= total_score <= 6:
    st.warning("Легкая/умеренная органная дисфункция")
elif 7 <= total_score <= 11:
    st.error("Тяжелая органная дисфункция")
else:
    st.error("Крайне тяжелая органная дисфункция (высокий риск летальности)")

def calculate_sofa_scores(params):
    scores = {}

    respiratory_index = params['pao2'] / (params['fio2'] / 100)
    if respiratory_index > 400:
        scores['respiratory'] = 0
    elif 300 < respiratory_index <= 400:
        scores['respiratory'] = 1
    elif 200 < respiratory_index <= 300:
        scores['respiratory'] = 2
    elif 100 < respiratory_index <= 200:
        scores['respiratory'] = 3
    else:
        scores['respiratory'] = 4

    gcs = params['gcs']
    if gcs == 15:
        scores['nervous'] = 0
    elif 13 <= gcs <= 14:
        scores['nervous'] = 1
    elif 10 <= gcs <= 12:
        scores['nervous'] = 2
    elif 6 <= gcs <= 9:
        scores['nervous'] = 3
    else:
        scores['nervous'] = 4

    cv_options = {
        'Норма': 0,
        'АДср < 70': 1,
        'Допамин ≤ 5': 2,
        'Допамин > 5': 3,
        'Допамин > 15': 4
    }
    scores['cardiovascular'] = cv_options.get(params['cardiovascular'], 0)

    bilirubin = params['bilirubin']
    if bilirubin < 20:
        scores['liver'] = 0
    elif 20 <= bilirubin <= 32:
        scores['liver'] = 1
    elif 33 <= bilirubin <= 101:
        scores['liver'] = 2
    elif 102 <= bilirubin <= 204:
        scores['liver'] = 3
    else:
        scores['liver'] = 4

    platelets = params['platelets']
    if platelets > 150:
        scores['coagulation'] = 0
    elif 100 < platelets <= 150:
        scores['coagulation'] = 1
    elif 50 < platelets <= 100:
        scores['coagulation'] = 2
    elif 20 < platelets <= 50:
        scores['coagulation'] = 3
    else:
        scores['coagulation'] = 4

    r_options = {
        '< 110 мкмоль/л': 0,
        '110-170 мкмоль/л': 1,
        '171-299 мкмоль/л': 2,
        '300-440 мкмоль/л': 3,
        '> 440 мкмоль/л': 4
    }
    scores['renal'] = r_options.get(params['renal'], 0)
    total = sum(scores.values())

    if total == 0:
        diagnosis = "Нет органной дисфункции"
    elif 1 <= total <= 6:
        diagnosis = "Легкая/умеренная органная дисфункция"
    elif 7 <= total <= 11:
        diagnosis = "Тяжелая органная дисфункция"
    else:
        diagnosis = "Крайне тяжелая органная дисфункция (высокий риск летальности)"

    return {
        'scores': scores,
        'total': total,
        'diagnosis': diagnosis
    }


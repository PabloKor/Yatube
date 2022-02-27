import datetime as dt


def year(request):
    """
    Добавляет переменную с текущим годом.
    """
    current_year = dt.datetime.now().year
    return {'current_year': current_year}

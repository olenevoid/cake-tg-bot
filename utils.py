from datetime import datetime, date, time, timedelta
from tg_bot import settings


def split_to_sublists(items: list, chunk_size: int = 2):
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def get_available_dates():
    """Возвращает список из 14 ближайших дат для доставки.
    Учитывает текущее время (если сейчас вечер, то сегодняшний день не предлагаем).
    """
    now = datetime.now()
    start_date = now.date()
    
    # Если сейчас после времени EVENING_HOUR, начинаем с завтра
    if now.hour >= settings.EVENING_HOUR:
        start_date += timedelta(days=1)
    
    dates = []
    for i in range(14):
        current_date = start_date + timedelta(days=i)
        dates.append(current_date)
    
    return dates


def get_available_times(delivery_date: date):
    """Возвращает список доступного времени для доставки на указанную дату.
    Учитывает рабочее время пекарни и минимальное время на приготовление и доставку.
    """
    now = datetime.now()
    
    # Рассчитываем минимальное общее время
    min_time_total = timedelta(
        hours=settings.MIN_PREPARATION_TIME_HOURS + settings.MIN_DELIVERY_TIME_HOURS
    )
    
    # Если дата доставки - сегодня
    if delivery_date == now.date():
        # Проверяем, не слишком ли поздно для заказа на сегодня
        # Рассчитываем крайнее время, до которого можно принять заказ на сегодня
        latest_order_time = datetime.combine(delivery_date, time(settings.WORK_HOURS_END, 0)) - min_time_total
        if now > latest_order_time:
            return []  # Слишком поздно для заказа на сегодня
        
        # Начальное время = текущее время + минимальное общее время
        start_time_dt = now + min_time_total
        
        # Округляем до ближайших 30 минут в большую сторону
        minutes = start_time_dt.minute
        if minutes % 30 != 0:
            start_time_dt += timedelta(minutes=(30 - minutes % 30))
        
        start_time = start_time_dt.time()
    else:
        # Если дата не сегодня, начинаем с начала рабочего дня
        start_time = time(settings.WORK_HOURS_START, 0)
    
    # Убедимся, что начальное время не раньше начала рабочего дня
    if start_time < time(settings.WORK_HOURS_START, 0):
        start_time = time(settings.WORK_HOURS_START, 0)
    
    # Убедимся, что начальное время не позже конца рабочего дня
    if start_time >= time(settings.WORK_HOURS_END, 0):
        return []
    
    # Генерируем время с шагом 30 минут
    times = []
    current_time = datetime.combine(delivery_date, start_time)
    end_time = datetime.combine(delivery_date, time(settings.WORK_HOURS_END, 0))
    
    while current_time <= end_time:
        times.append(current_time.time())
        current_time += timedelta(minutes=30)
    
    return times


def is_within_24_hours(given_date, given_time):
    given_datetime = datetime.combine(given_date, given_time)
    current_datetime = datetime.now()

    time_difference = abs(current_datetime - given_datetime)

    return time_difference <= timedelta(hours=24)

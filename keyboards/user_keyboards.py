import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BeautyCity_bot.settings")

import django

django.setup()

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import datetime as dt

CALL_US_BUTTON = ('Позвонить нам', 'call_us')

from bot.models import *

def start_keyboard():
    buttons_data = [
        ('Записаться', 'Оставить отзыв'),
        ('О нас',)
    ]

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text) for text in row] for row in buttons_data
        ],
        resize_keyboard=True
    )


def what_can_be_stored_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Читать 🔍',
                    url='https://telegra.ph/Pravila-hraneniya-04-20'
                )
            ]
        ]
    )


def type_service_keyboard():
    services = [
        ('Мейкап', 'service Мейкап'),
        ('Покраска волос', 'service Покраска волос'),
        ('Маникюр', 'service Маникюр'),
        CALL_US_BUTTON
    ]

    serices_m = Service.objects.all()
    services = list()
    for service in serices_m:
        services.append((service.name, f'service {service.id}'))
    services.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in services
        ],
    )


def masters_keyboard(service):
    service_m = Service.objects.get(pk=service)
    print(f'{service_m=}')
    masters_m = service_m.services.all()
    masters = list()
    for master in masters_m:
        masters.append((master.name, f'master {master.id}'))
    # masters = [('Ольга', 'master Ольга'), ('Татьяна', 'master Татьяна')]
    masters.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in masters
        ],
    )


def date_work_master_keyboard(master):
    master = Specialist.objects.get(pk=master)
    date_m = master.specialist.all()
    date_list = list()
    for date_element in date_m:
        date_list.append((str(date_element.date), f'date {date_element.date}'))
    date_list.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in date_list
        ],
    )


def time_work_master_keyboard(master, date):
    master = Specialist.objects.get(pk=master)
    # time_m = master.specialist.filter(date=date)
    print(master)
    time_list = list()
    for time_element in time_m:
        time_list.append((str(time_element.date), f'time {time_element.date}'))
    time_list.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in time_list
        ],
    )



def calculate_work_shifts(first_shift):
    now = dt.date.today()
    work_shifts_buttons = []
    work_shifts = [first_shift, first_shift + dt.timedelta(days=1)]
    while now > work_shifts[0] or now > work_shifts[1]:
        first_shift += dt.timedelta(days=4)
        work_shifts = [first_shift, first_shift + dt.timedelta(days=1)]
    while now + dt.timedelta(days=14) > work_shifts[0] or now > work_shifts[1]:
        work_shifts_buttons.append(
            (work_shifts[0].strftime('%d.%m.%Y'), f'date {work_shifts[0].strftime("%d.%m.%Y")}')
        )
        work_shifts_buttons.append(
            (work_shifts[1].strftime('%d.%m.%Y'), f'date {work_shifts[0].strftime("%d.%m.%Y")}')
        )
        first_shift += dt.timedelta(days=4)
        work_shifts = [first_shift, first_shift + dt.timedelta(days=1)]
    return work_shifts_buttons


def master_work_shifts_keyboard(master):
    # Даты выхода на работу впервые для мастеров Ольга и Татьяна
    # Мастера работают по графику 2/2
    date_format = '%d.%m.%Y'
    first_shift_olga = dt.datetime.strptime('10.01.2016', date_format).date()
    first_shift_tatiana = dt.datetime.strptime('13.01.2016', date_format).date()
    if master == 'Ольга':
        first_shift = first_shift_olga
        work_shifts_buttons = calculate_work_shifts(first_shift)
        work_shifts_buttons.append(CALL_US_BUTTON)
    else:
        first_shift = first_shift_tatiana
        work_shifts_buttons = calculate_work_shifts(first_shift)
        work_shifts_buttons.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in work_shifts_buttons
        ],
    )


def time_keyboard():
    time = []
    for hour in range(8, 20):
        time.append((str(hour) + ':00', f'time {str(hour) + ":00"}'))
        if hour < 20:
            time.append((str(hour) + ':30', f'time {str(hour) + ":30"}'))
    time.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in time
        ],
    )


def pay_keyboard():
    buttons_data = [
        ('Да', 'pay_yes'),
        ('Нет', 'pay_no')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def extend_rental_period_keyboard():
    periods = [
        ('1 месяц', 'extend_one_month'),
        ('3 месяца', 'extend_tree_month'),
        ('6 месяцев', 'extend_six_month'),
        ('12 месяцев', 'extend_twelve_month')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in periods
        ]
    )


def generate_pick_up_things_keyboard():
    buttons_data = [
        ('Заберу сам(а)', 'pick_up_myself'),
        ('Доставить на дом', 'deliver_home')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def generate_pick_up_cells_keyboard(user_cells):
    buttons = []
    for cell in user_cells:
        buttons.append((f'{cell}', f'pick_up_cell_{cell}'))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons
        ]
    )


def agree_keyboard():
    buttons_data = [
        ('Согласен с правилами', 'agree')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )

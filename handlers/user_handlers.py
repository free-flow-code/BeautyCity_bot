from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery, FSInputFile, pre_checkout_query, successful_payment, LabeledPrice
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.message import ContentType
from aiogram.methods.send_invoice import SendInvoice

from config_data.config import my_table, load_config, PRICES, PHOTOS
from keyboards import user_keyboards
from lexicon.lexicon_ru import LEXICON_RU

from database import database_funcs
from utils.utils import entry_to_database, get_qrcode

router = Router()

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BeautyCity_bot.settings")

import django

django.setup()

from bot.models import *


class MyCellsState(StatesGroup):
    cell_number = State()
    all_things = State()  # True клиент заберет все вещи, если часть - False


class GetUserInfo(StatesGroup):
    new_user = State()
    service = State()  # Тип косметической процедуры
    master = State()  # Специалист, к которому происходит запись
    date = State()  # Дата посещения
    time = State()  # Время посещения
    name = State()  # Имя, которое ввел клиент
    phone = State()  # Телефон клиента
    pay = State()  # Оплатил ли клиент процедуру сразу (True/False)
    pay_yes = State()
    pay_no = State()


class GetCommentInfo(StatesGroup):
    text = State()
    user_name = State()
    save = State()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=user_keyboards.start_keyboard()
    )
    await state.clear()


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/help'],
    )


@router.message(Text(contains=['Что можно хранить']))
async def process_what_can_be_stored(message: Message):
    await message.answer(
        text='Ознакомиться с правилами хранения:',
        reply_markup=user_keyboards.what_can_be_stored_keyboard()
    )


# --------------------------------------------------------------------------

@router.message(Text(contains=['О нас']))
async def about(message: Message):
    services = Service.objects.all()
    text = LEXICON_RU['about']
    for service in services:
        text = f'{text}\n- {service.name}'
    await message.answer(
        text=text,
        reply_markup=user_keyboards.start_keyboard()
    )


# --------------------------------------------------------------------------


@router.message(Text(contains=['Оставить отзыв']))
async def set_text_comment(message: Message, state: FSMContext):
    await message.answer(
        text='Напишите отзыв:'
    )
    await state.set_state(GetCommentInfo.text)


@router.message(GetCommentInfo.text)
async def set_user_name_comment(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.answer(
        text='Ваше имя:'
    )
    await state.set_state(GetCommentInfo.save)


@router.message(GetCommentInfo.save)
async def save_comment(message: Message, state: FSMContext):
    user_name = message.text
    user_data = await state.get_data()
    await state.update_data(user_name=user_name)
    comment = Comment.objects.create()
    comment.text = user_data['text']
    comment.user_name = user_name
    comment.save()

    await message.answer(
        text='Спасибо об отзыве о нашем салоне красоты!',
        reply_markup=user_keyboards.start_keyboard()

    )
    await state.clear()


# --------------------------------------------------------------------------


@router.message(Text(contains=['Записаться']))
async def sign_up(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['rules'],
        reply_markup=user_keyboards.agree_keyboard()
    )
    user_id = int(message.from_user.id)
    await state.update_data(user_id=user_id)
    await state.set_state(GetUserInfo.new_user)


@router.callback_query(Text(text=['call_us']))
async def call_us(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Мы рады звонку в любое время\n8(800) 555 35 35'
    )


@router.callback_query(Text(text=['agree']), GetUserInfo.new_user)
async def get_service_type(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Выберите услугу:',
        reply_markup=user_keyboards.type_service_keyboard()
    )
    await state.update_data(service=callback.data)
    await state.set_state(GetUserInfo.service)
    await callback.answer()


@router.callback_query(Text(startswith=['service']), GetUserInfo.service)
async def get_master(callback: CallbackQuery, state: FSMContext):
    service = callback.data.split()[1]
    await state.update_data(service=service)

    await callback.message.edit_text(
        text='К какому мастеру вы хотите записаться?',
        reply_markup=user_keyboards.masters_keyboard(service)
    )
    await state.set_state(GetUserInfo.master)
    await callback.answer()


@router.callback_query(Text(startswith=['master']), GetUserInfo.master)
async def get_procedure_date(callback: CallbackQuery, state: FSMContext):
    master = callback.data.split()[1]
    await state.update_data(master=master)

    await callback.message.edit_text(
        text='Выберите дату:',
        reply_markup=user_keyboards.date_work_master_keyboard(master)
    )
    await state.set_state(GetUserInfo.date)
    await callback.answer()


@router.callback_query(Text(startswith=['date']), GetUserInfo.date)
async def get_procedure_time(callback: CallbackQuery, state: FSMContext):
    date = callback.data.split()[1]
    user_data = await state.get_data()
    await state.update_data(date=date)

    master_id = user_data['master']
    service_id = user_data['service']
    await callback.message.edit_text(
        text='Выберите время:',
        reply_markup=user_keyboards.time_work_master_keyboard(master_id, service_id, date)
    )
    await state.set_state(GetUserInfo.time)
    await callback.answer()


@router.callback_query(Text(startswith=['time_slot']), GetUserInfo.time)
async def get_user_name(callback: CallbackQuery, state: FSMContext):
    time_slot = callback.data.split()[1]
    await state.update_data(time_slot=time_slot)

    await callback.message.edit_text(
        text='Введите свое имя:'
    )
    await state.set_state(GetUserInfo.name)
    await callback.answer()


@router.message(GetUserInfo.name)
async def get_phone_number(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    await message.answer(
        text='Введите ваш номер телефона для связи:'
    )
    await state.set_state(GetUserInfo.phone)


@router.message(GetUserInfo.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    user_data = await state.get_data()
    date = user_data['date']
    await message.answer(
        text=f'Спасибо за запись! До встречи {date} по адресу address.\nХотите оплатить сразу?',
        reply_markup=user_keyboards.pay_keyboard()
    )

    await state.set_state(GetUserInfo.pay)


@router.callback_query(Text(contains=['pay_no']))
async def check_pay(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user, created = User.objects.get_or_create(telegram_id=user_data['user_id'])
    if created:
        user.name = user_data['name']
        user.telegram_id = user_data['user_id']
        user.phone = user_data['phone']
        user.save()
    date = user_data['date']
    time_slot = user_data['time_slot']
    await state.update_data(pay=False)
    schedule = Schedule.objects.create(date=user_data['date'],
                                       timeslot=user_data['time_slot'],
                                       user=user,
                                       specialist_id=int(user_data['master']),
                                       services_id=int(user_data['service'])
                                       )
    schedule.save()
    await callback.message.edit_text(
        text=f"Спасибо за запись! До встречи {date} {time_slot} по адресу address"
    )
    await state.clear()


@router.callback_query(Text(contains=['pay_yes']))
async def process_storage_conditions(message: Message, bot: Bot, state: FSMContext):
    user_data = await state.get_data()
    service = Service.objects.get(pk=user_data['service'])
    price = [LabeledPrice(label=str(service.name), amount=int(service.price * 100))]
    await state.update_data(amount=service.price)
    await bot.send_invoice(
        message.from_user.id,
        title=service.name,
        description='Оплата косметической поцедуры.',
        provider_token=load_config().payment_token.p_token,
        currency='rub',
        photo_url=PHOTOS[f'{service.name}'],
        is_flexible=False,
        prices=price,
        start_parameter='example',
        payload='test-invoice-payload'
    )

    await state.set_state(GetUserInfo.pay_yes)


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: pre_checkout_query.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message()
async def successful_payment(message: Message, state: FSMContext):
    if message.successful_payment:
        user_data = await state.get_data()
        user, created = User.objects.get_or_create(telegram_id=user_data['user_id'])
        if created:
            user.name = user_data['name']
            user.telegram_id = user_data['user_id']
            user.phone = user_data['phone']
            user.save()
        schedule = Schedule.objects.create(
            date=user_data['date'],
            timeslot=user_data['time_slot'],
            user=user,
            specialist_id=int(user_data['master']),
            services_id=int(user_data['service']),
            pay=True,
            amount=user_data['amount']
        )
        schedule.save()
        await state.clear()

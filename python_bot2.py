from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import get_all_products, is_included, add_user

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb2 = InlineKeyboardMarkup(resize_keyboard=True)
buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ], resize_keyboard=True)  # Для задания 14_3
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')  # Для задания 14_3
button_reg = KeyboardButton(text='Регистрация')
kb.add(button1, button2, button3, button_reg)
button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.add(button3, button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):# Для задания 14_5
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(text='Регистрация')# Для задания 14_5
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):', parse_mode='HTML')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)# Для задания 14_5
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()
    if is_included(str(data['username'])) is False:  # функция для проверки существования пользователя
        await message.answer('Введите свой email:', parse_mode='HTML')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя:', parse_mode='HTML')
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)# Для задания 14_5
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:', parse_mode='HTML')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(str(data['username']), str(data['email']), int(data['age']))
    await message.answer('Регистрация прошла успешно!', parse_mode='HTML')
    await state.finish()



@dp.message_handler(text='Купить')  # Для задания 14_3
async def get_buying_list(message):
    products = get_all_products()
    for product in products:
        product_id, title, description, price = product  # распаковываем кортеж
        # Формируем путь к изображению для каждого продукта (например, images/Product{id}.jpg)
        image_path = f'files/Друг{product_id}.jpg'
        with open(image_path, 'rb') as img:
            await message.answer_photo(img, f"Название: {title} | Описание: {description} | Цена: {price}")
    await message.answer('Выберите друга для дружбы:', reply_markup=buy_kb)


@dp.callback_query_handler(text='product_buying')  # Для задания 14_3
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин:\n 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте\n\nЭтот бот предназначен для расчетов калорий, '
                         'основанных на вашей банковской карте\n\n'
                         '(это шутка! НЕ передавайте НИКОМУ данные своей банковской карты\n'
                         'этими данными могут воспользоваться мошенники)', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    try:
        age = int(message.text)
        if age <= 0:
            raise ValueError("Возраст должен быть положительным числом.")
        await state.update_data(age=age)
        await message.answer('Введите свой рост в см:')
        await UserState.growth.set()
    except ValueError as e:
        await message.answer(f"Ошибка ввода возраста: {e}\nПопробуйте снова:")
        return


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    try:
        growth = int(message.text)
        if growth <= 0:
            raise ValueError('Рост должен быть положительным числом.')
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес в кг:')
        await UserState.weight.set()
    except ValueError as e:
        await message.answer(f"Ошибка ввода веса: {e}\nПопробуйте снова:")
        return


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state):
    try:
        weight = int(message.text)
        if weight <= 0:
            raise ValueError('Вес должен быть положительным числом.')
        await state.update_data(weight=message.text)
        data = await state.get_data()
        age = int(data['age'])
        growth = int(data['growth'])
        weight = int(data['weight'])
        calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5
        await message.answer(f'Ваша норма калорий: {calories:.2f}')
        await state.finish()
    except ValueError as e:
        await message.answer(f"Ошибка ввода роста: {e}\nПопробуйте снова:")
        return


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

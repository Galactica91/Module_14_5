from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions

from pyexpat.errors import messages

api = "7775779452:AAEATs0Fe0bP-tyd7DfnOmL3nOPUGEWIEI4"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button7 = KeyboardButton(text='Регистрация')
kb.row(button, button2, button3, button7)

kb2 = InlineKeyboardMarkup()
inline_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.row(inline_button, inline_button2)

kb3 = InlineKeyboardMarkup()
inline_button3 = InlineKeyboardButton(text='Product-1', callback_data='product_buying')
inline_button4 = InlineKeyboardButton(text='Product-2', callback_data='product_buying')
inline_button5 = InlineKeyboardButton(text='Product-3', callback_data='product_buying')
inline_button6 = InlineKeyboardButton(text='Product-4', callback_data='product_buying')
kb3.row(inline_button3, inline_button4, inline_button5, inline_button6)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Это онлайн космитический интернет-магазин')

@dp.message_handler(commands=['Start'])
async def command_start(message):
    await message.answer(f"Привет {message.from_user.username}! Я бот помогающий твоему здоровью. Выберите, что Вас интересует.", reply_markup=kb)

@dp.message_handler(text="Рассчитать")
async def show_calculate_options(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    calories = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])) - 161
    await message.answer(f"Норма Ваших калорий составляет - {calories} в сутки")
    await state.finish()

@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    for i in range(1, 5):
        with open(f'product{i}.png', "rb") as img:
            await message.answer(f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100} рублей.')
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=kb3)

@dp.callback_query_handler(lambda call: call.data == "product_buying")
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

#@dp.message_handler()
#async def all_messages(message):
#    await message.answer("Введите команду /start, чтобы запустить бота")

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    user = message.text
    if not crud_functions.is_included(user):
        await message.answer("Пользователь существует, введите другое имя:")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=user)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    age = int(data.get('age'))
    crud_functions.add_user(username, email, age)
    await state.finish()
    await message.answer(
        f"Регистрация завершена!\n Пользователь {username},\n email: {email},\n возраст: {str(age)} добавлен.")

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
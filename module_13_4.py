from aiogram.filters.command import Command, CommandStart
from aiogram import Bot, Dispatcher, types,F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7363453523525324")
dp = Dispatcher()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()



@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer('Здравствуйте! Вас приветствует калькулятор подсчета калорий! Напишите "Калории" для начала расчета!')




@dp.message(F.text == "Калории")
async def set_age(message: types.Message, state: FSMContext):
    await message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)



@dp.message(UserState.age)
async def set_growth(message: types.Message,  state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: types.Message,  state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: types.Message,  state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age_ = int(data['age'])
    growth_ = int(data['growth'])
    weight_ = int(data['weight'])

    await message.answer(f"Ваша норма калорий:{ (weight_*10) + (6.25 * growth_) -  (5* age_) + 5 }")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


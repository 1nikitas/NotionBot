# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, types, executor
import time
import pickle
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from telethon import TelegramClient

from Database import Database_Notion as db1
import random


"""
TelegramClient(Support_mobile_phone, App api_id, App api_hash)
"""

token_id =  token_id
bot = Bot(token=token_id)
memory = MemoryStorage()
dp = Dispatcher(bot, storage=memory)
db = db1('Notion.db')
access_id = [54962694, 218735730, 5124158760, 582897416]

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пройти регистрацию🤝")
        ]
    ], resize_keyboard=True
)


class register(StatesGroup):
    tg_id = State()
    email = State()


@dp.message_handler(Command("start"))
async def getUsers(message: types.Message):
    await getUsers1()
    if db.user_exists_tg(message.from_user.id) and db.user_exists(message.from_user.id):
        await message.answer("Ты уже зарегестрирован!")

    else:
        await message.answer("Тебя привествует Crypto_Pushkin_bot 😃\n"
                             "Тебе доступна регистрация 🙌", reply_markup=keyboard_menu)


@dp.message_handler(Command("get_users"))
async def getUsers(message: types.Message):
    if message.from_user.id in access_id:
        client =  TelegramClient("1", 13042603, "2e2890a7d217c47948afec4234160f01")
        participants = []
        """
        -100 + (1790651075) (channel_id where bot is admin)
        """
        db.zero_users(0)
        async with client:
            for user in await client.get_participants(-1001587727026):
                participants.append(str(user.id))
                db.add_user_tg(int(user.id))
        await message.answer("\n".join(participants))
    else:
        await message.answer("У вас нет доступа к этой функции")


async def getUsers1():
    client =  TelegramClient("1", 15465531, "9ff33616247248afe167b5de803740ba", auto_reconnect=True)
    """
    -100 + (1790651075) (channel_id where bot is admin)
    """
    db.zero_users()
    async with client:
        for user in await client.get_participants(-1001587727026):
            db.add_user_tg(int(user.id))




@dp.message_handler(text="Пройти регистрацию🤝")
async def register_(message: types.Message):
    await message.answer("Ты перешел в меню регистрации.\n"
                         "Введи свой email, чтобы мы добавили тебя в среду обучения ⚠")
    await register.email.set()



@dp.message_handler(state = register.email)
async def state1(message: types.Message, state: FSMContext):

    answer = message.text

    await state.update_data(email = answer)
    answer = message.from_user.id
    await state.update_data(tg_id = answer)
    data = await state.get_data()

    tg_id = data.get('tg_id')
    email = data.get('email')

    await state.finish()

    if db.user_exists_tg(tg_id):
        db.add_user(email, tg_id)
        await message.answer(f'Регистрация прошла успешно! ✅')
        await message.answer(f'Идет процесс добавления в среду обучения! 🔜')
        await invite(message, email)

    else:
        await message.answer("У вас нет платной подписки!")





# @dp.message_handler(Command('invite'))
async def invite(message: types.Message, email):
    options = Options()
    msg = await message.answer(f'Осталось: 15 секунд')
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome( executable_path='/home/notionBot/chromedriver', options=options) # chrome_options=options

    urls = [
        "https://www.notion.so/cryptopushnila/1d151949882b497baddde4775bb788f2",
        "https://www.notion.so/cryptopushnila/791cf2103c0e4dcb8917c7840516558f",
        "https://www.notion.so/cryptopushnila/PUSHKIN-CRYPTO-ACADEMY-8f006ca832344569af9cb33cbeb3ee72",
        "https://www.notion.so/cryptopushnila/8f0cb4a682bf4da497961579bbd1e908"

    ]


    try:
        for url in urls:
            time.sleep(3)
            driver.get('https://www.notion.so/')
            time.sleep(2)
            await msg.edit_text(f'Осталось: 13 секунд')
            # pickle.dump(driver.get_cookies(), open("cookies", "wb"))
            # print("ok!")

            for cookie in pickle.load(open("cookies", "rb")):
                driver.add_cookie(cookie)
            await msg.edit_text(f'Осталось: 11 секунд')
            time.sleep(2)
            driver.refresh()
            time.sleep(3)
            await msg.edit_text(f'Осталось: 9 секунд')
            driver.get(url)
            time.sleep(3)
            share = driver.find_element(By.XPATH, value="//div[normalize-space()='Share']")
            share.click()
            await msg.edit_text(f'Осталось: 7 секунд')
            time.sleep(3)
            input_field = driver.find_element(By.XPATH, value="//div[contains(text(),'Add emails, people, integrations...')]")
            input_field.click()
            time.sleep(3)
            await msg.edit_text(f'Осталось: 5 секунд')
            inputting = driver.find_element(By.XPATH, value="//input[@placeholder='Add emails, people, integrations...']")
            inputting.send_keys(f'{email}')
            time.sleep(2)
            await msg.edit_text(f'Осталось: 3 секунды')
            invite_button = driver.find_element(By.XPATH, value="//div[normalize-space()='Invite']")
            invite_button.click()
            time.sleep(2)
            await msg.edit_text(f'Осталось: 2 секунды')
            list_access = driver.find_element(By.XPATH, value="//body//div[@id='notion-app']//div[@class='notion-scroller vertical']//div[@class='notion-scroller vertical']//div//div//div[1]//div[1]//div[1]//div[3]//div[1]//span[1]")
            list_access.click()
            time.sleep(3)
            await msg.edit_text(f'Успешно!')
            view = driver.find_element(By.XPATH, value="//span[normalize-space()='Cannot edit or share with others.']")
            view.click()
            time.sleep(3)

    except Exception:
        for url in urls:
            time.sleep(3)
            driver.get('https://www.notion.so/')
            time.sleep(2)
            await msg.edit_text(f'Осталось: 13 секунд')
            # pickle.dump(driver.get_cookies(), open("cookies", "wb"))
            # print("ok!")

            for cookie in pickle.load(open("cookies", "rb")):
                driver.add_cookie(cookie)
            await msg.edit_text(f'Осталось: 11 секунд')
            time.sleep(2)
            driver.refresh()
            time.sleep(3)
            await msg.edit_text(f'Осталось: 9 секунд')
            driver.get(url)
            time.sleep(3)
            share = driver.find_element(By.XPATH, value="//div[normalize-space()='Share']")
            share.click()
            await msg.edit_text(f'Осталось: 7 секунд')
            time.sleep(3)
            input_field = driver.find_element(By.XPATH,
                                              value="//div[contains(text(),'Add emails, people, integrations...')]")
            input_field.click()
            time.sleep(3)
            await msg.edit_text(f'Осталось: 5 секунд')
            inputting = driver.find_element(By.XPATH,
                                            value="//input[@placeholder='Add emails, people, integrations...']")
            inputting.send_keys(f'{email}')
            time.sleep(2)
            await msg.edit_text(f'Осталось: 3 секунды')
            invite_button = driver.find_element(By.XPATH, value="//div[normalize-space()='Invite']")
            invite_button.click()
            time.sleep(2)
            await msg.edit_text(f'Осталось: 2 секунды')
            list_access = driver.find_element(By.XPATH,
                                              value="//body//div[@id='notion-app']//div[@class='notion-scroller vertical']//div[@class='notion-scroller vertical']//div//div//div[1]//div[1]//div[1]//div[3]//div[1]//span[1]")
            list_access.click()
            time.sleep(3)
            await msg.edit_text(f'Успешно!')
            view = driver.find_element(By.XPATH, value="//span[normalize-space()='Cannot edit or share with others.']")
            view.click()
            time.sleep(3)
    await message.answer("Добро пожаловать в команду!"
                         "\nhttps://www.notion.so/cryptopushnila/PUSHKIN-CRYPTO-ACADEMY-8f006ca832344569af9cb33cbeb3ee72")

@dp.message_handler(Command("update_notion"))
async def search(message: types.Message):
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")

    db.zero_users()
    await getUsers1()
    db.email_zero()
    db.tg_in_notion()
    users = [user[0] for user in db.id_selector()]
    print(users)
    msg = await message.answer(f"Найдено {len(users)}")
    if len(users) == 0:
        await msg.edit_text("Пользователи удалены успешны!")
    else:
        msg = await message.answer("Идет удаление!")
        for user in range(len(users)):
            try:
                await msg.edit_text(f'Осталось: 13 секунд')
                driver = webdriver.Chrome( executable_path='/home/notionBot/chromedriver', chrome_options=options)
                driver.get('https://www.notion.so/')
                time.sleep(3)
                await msg.edit_text(f'Осталось: 10 секунд')
                for cookie in pickle.load(open("cookies", "rb")):
                    driver.add_cookie(cookie)
                time.sleep(5)
                driver.refresh()
                time.sleep(5)
                driver.get("https://www.notion.so/cryptopushnila/5a26e1cc0e634f00b765df61f3e20e02")
                time.sleep(3)
                await msg.edit_text(f'Осталось: 8 секунд')
                find = driver.find_element(By.XPATH, value="//div[contains(text(),'Settings & Members')]")
                find.click()
                time.sleep(3)
                search_fild = driver.find_element(By.XPATH, value="//input[@placeholder='Filter by email or name…']")
                search_fild.send_keys(f'{users[user]}')
                pages = driver.find_element(By.XPATH, value="//span[@class='notranslate']")
                pages.click()
                await msg.edit_text(f'Осталось: 5 секунд')
                time.sleep(2)
                remove = driver.find_element(By.XPATH, value="//div[contains(text(),'Remove from workspace')]")
                remove.click()
                time.sleep(2)

                await msg.edit_text(f'Осталось: 3 секунд')
                accept = driver.find_element(By.XPATH, value="//div[normalize-space()='Remove']")
                accept.click()
                time.sleep(4)
                db.delete_from_notion(email=users[user])
                await msg.edit_text(f"{users[user]} удален успешно!")
            except Exception:
                msg = await message.answer("Еще одна попытка запущена!")
                driver = webdriver.Chrome( executable_path='/home/notionBot/chromedriver', chrome_options=options)
                driver.get('https://www.notion.so/')
                time.sleep(3)
                await msg.edit_text(f'Осталось: 13 секунд')
                for cookie in pickle.load(open("cookies", "rb")):
                    driver.add_cookie(cookie)
                time.sleep(5)
                driver.refresh()
                time.sleep(5)
                await msg.edit_text(f'Осталось: 10 секунд')
                driver.get("https://www.notion.so/cryptopushnila/5a26e1cc0e634f00b765df61f3e20e02")
                time.sleep(3)
                find = driver.find_element(By.XPATH, value="//div[contains(text(),'Settings & Members')]")
                find.click()
                time.sleep(3)
                await msg.edit_text(f'Осталось: 7 секунд')
                find1 = driver.find_element(By.XPATH, value="//div[contains(text(),'Guests')]")
                find1.click()
                time.sleep(3)
                search_fild = driver.find_element(By.XPATH, value="//input[@placeholder='Filter by email or name…']")
                search_fild.send_keys(f'{users[user]}')
                pages = driver.find_element(By.XPATH, value="//div[contains(text(),'1 page')]")
                pages.click()
                await msg.edit_text(f'Осталось: 5 секунд')
                time.sleep(2)
                remove = driver.find_element(By.XPATH, value="//div[normalize-space()='Remove']")
                remove.click()
                time.sleep(2)
                await msg.edit_text(f'Осталось: 3 секунд')
                accept = driver.find_element(By.XPATH, value="/html[1]/body[1]/div[1]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]")
                accept.click()
                time.sleep(4)
                db.delete_from_notion(email=users[user])
                await msg.edit_text(f"{users[user]} удален успешно!")

    await message.answer("Участники успешно обновлены!")


def main():
    executor.start_polling(dp, skip_updates=True)


while True:
    try:
        main()
    except Exception:
        pass
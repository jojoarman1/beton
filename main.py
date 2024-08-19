from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, MediaGroup
import logging

API_TOKEN = '6601504690:AAH5PE8Dy7ks7KqOnw7cg4GO-6MP7symM-o'  # Замените на ваш токен

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

image_message_ids = {}
TARGET_USER_ID = 7343742150  # Замените на ID пользователя
user_data = {}  # Словарь для хранения данных пользователя
user_steps = {}  # Словарь для отслеживания шагов
questions = [
    "Как вас зовут?",
    "Ваш контактный телефон?",
    "Ваше сообщение"
]
cities_info = {
    'surgut': (
        "<b>Сургут</b>\n\n"
        "<b>Инженерный центр \"Теплоотдача\"</b>\n\n"
        "<b>Адрес:</b> г. Сургут, Нефтеюганское шоссе, дом 72/1\n\n"
        "<b>Телефон:</b> 8-800-551-31-73\n\n"
        "<b>Сайт:</b> <a href='http://tplda.com'>tplda.com</a>"
    ),
    'biysk': (
        "<b>Бийск</b>\n\n"
        "<b>ООО «Аква Лига»</b>\n\n"
        "<b>Адрес:</b> г. Бийск, ул. Шишкова, д. 5\n\n"
        "<b>Телефон:</b> +7 (3854) 55 54 45, +7 (962) 802 00 66"
    ),
    'bryansk': (
        "<b>Брянск</b>\n\n"
        "<b>САМОРЕЗЫ</b>\n\n"
        "<b>Адрес:</b> г. Брянск, п. Путевка, ул. Рославльская, д. 1 стр. 2\n\n"
        "<b>Телефон:</b> +7 (4832) 65-11-11, +7 (4832) 65-12-12\n\n"
        "<b>Сайт:</b> <a href='http://samorezi.com'>samorezi.com</a>"
    ),
    'volgograd': (
        "<b>Волгоград</b>\n\n"
        "<b>ООО «Сантехкомплект»</b>\n\n"
        "<b>Адрес:</b> г. Волгоград, ул. Козловская, д. 40а\n\n"
        "<b>Телефон:</b> +7 (8442) 97 45 56, +7 (8442) 97 54 85"
    ),
    'gorno_altaysk': (
        "<b>Горно-Алтайск</b>\n\n"
        "<b>ООО «Аква Лига»</b>\n\n"
        "<b>Адрес:</b> г. Горно-Алтайск, пр. Коммунистический 60\n\n"
        "<b>Телефон:</b> +7 (38822) 9 45 15, +7 (983) 325 35 45"
    ),
    'ekaterinburg': (
        "<b>Екатеринбург</b>\n\n"
        "<b>СанТерм-Теплые полы Отопление Водоснабжение</b>\n\n"
        "<b>Адрес:</b> г. Екатеринбург, ул. Черкасская 9, офис 101, склад №23, №24\n\n"
        "<b>Телефон:</b> +7 (343) 201 05 00, +7 (919) 399 05 00\n\n"
        "<b>Электронная почта:</b> <a href='mailto:santerm01@mail.ru'>santerm01@mail.ru</a>\n\n"
        "<b>Сайт:</b> <a href='http://santerm-ural.ru'>santerm-ural.ru</a>"
    ),
    'izhevsk': (
        "<b>Ижевск</b>\n\n"
        "<b>Магазин «Водяной»</b>\n"
        "<b>Адрес:</b> г. Ижевск, ул. Мельничная, 34б, оф. 2\n"
        "<b>Телефон:</b> +7 (3412) 56 73 76, +7 (912) 746 19 08\n\n"
        "<b>Сайт:</b> <a href='http://сантехник-ижевск.рф'>сантехник-ижевск.рф</a>\n\n"
        "<b>Экватор Сервис</b>\n"
        "<b>Адрес:</b> г. Ижевск, ул. Володарского, д. 75, корпус \"Б\"\n"
        "<b>Телефон:</b> +7 (3412) 27 17 78, +7 (912) 751 27 66"
    ),
    'irkutsk': (
        "<b>Иркутск</b>\n\n"
        "<b>ООО «Солана»</b>\n\n"
        "<b>Адрес:</b> г. Иркутск, ул. Карла Либнехта, 94, оф. 402 (БЦ \"Silver\")\n\n"
        "<b>Телефон:</b> +7 (3952) 436-595"
    ),
    'lipetsk': (
        "<b>Липецк</b>\n\n"
        "<b>ИП Яковлев</b>\n\n"
        "<b>Адрес:</b> г. Липецк, Поперечный пр., д. 1\n\n"
        "<b>Телефон:</b> +7 (4742) 24 01 99\n\n"
        "<b>Сайт:</b> <a href='http://vantus48.ru'>vantus48.ru</a>\n\n"
        "<b>Электронная почта:</b> <a href='mailto:mail@vantus48.ru'>mail@vantus48.ru</a>"
    ),
    'moscow': (
        "<b>Москва</b>\n\n"
        "<b>Собственный склад</b>\n\n"
        "<b>Адрес:</b> Московская область, Ленинский район, д. Боброво 47 (6 км от МКАД по Варшавскому шоссе)\n"
        "<b>Телефон:</b> 8 950 730 95 36, 8 800 100 42 05"
    ),
    'novorossiysk': (
        "<b>Новороссийск</b>\n\n"
        "<b>Собственный склад</b>\n\n"
        "<b>Телефон:</b> +7 (989) 774 96 30"
    ),
    'perm': (
        "<b>Пермь</b>\n\n"
        "<b>ООО «Сантехопт»</b>\n"
        "<b>Адрес:</b> г. Пермь, ул. Героев Хасана, 77a\n"
        "<b>Телефон:</b> +7 (342) 214 71 47\n"
        "<b>Режим работы:</b> ПН — ПТ: с 9:00 до 21:00, СБ — ВС: с 9:00 до 19:00\n\n"
        "<b>ООО «Сантехопт»</b>\n"
        "<b>Адрес:</b> г. Пермь, ул. Яблочкова, 48\n"
        "<b>Телефон:</b> +7 (342) 214 07 77\n"
        "<b>Режим работы:</b> ПН — ПТ: с 8:00 до 19:00, СБ: с 10:00 до 18:00, ВС: с 8:00 до 15:00\n\n"
        "<b>Дом Котлов</b>\n"
        "<b>Адрес:</b> г. Пермь, ул. Героев Хасана, 105, корпус 70\n"
        "<b>Телефон:</b> +7 (342) 240 45 85\n"
        "<b>Сайт:</b> <a href='http://dom-kotlov.ru'>dom-kotlov.ru</a>"
    ),
    'samara': (
        "<b>Самара</b>\n\n"
        "<b>ГК «Артикул»</b>\n"
        "<b>Адрес:</b> г. Самара, 19 км Московского шоссе, 11, дом 4-Б\n"
        "<b>Телефон:</b> +7 (927) 263 04 84\n"
        "<b>Электронная почта:</b> <a href='mailto:rogova@artihold.ru'>rogova@artihold.ru</a>\n\n"
        "<b>ГК «Артикул»</b>\n"
        "<b>Адрес:</b> Самарская область, Сергиевский район, пос. Сургут, ул. Ново-Садовая, 1 (База ООО \"БПО\")\n"
        "<b>Телефон:</b> +7 (927) 263 04 84\n"
        "<b>Электронная почта:</b> <a href='mailto:rogova@artihold.ru'>rogova@artihold.ru</a>"
    ),
    'simferopol': (
        "<b>Симферополь</b>\n\n"
        "<b>Термопласт-Симферополь</b>\n\n"
        "<b>Телефон:</b> +7 (978) 146 13 49"
    ),
    'cheboksary': (
        "<b>Чебоксары</b>\n\n"
        "<b>ООО «Портнов и К»</b>\n"
        "<b>Адрес:</b> г. Чебоксары, ул. Гладкова, 15а (вещевой рынок \"Ярмарка\", 1 ряд 17-18 место)\n"
        "<b>Телефон:</b> +7 (905) 199 32 55, +7 (903) 322 77 92, +7 (927) 668 95 26\n\n"
        "<b>ООО «Портнов и К»</b>\n"
        "<b>Адрес:</b> г. Чебоксары, ул. Болгарстроя 9/11 (магазин \"ВладаТорг\")\n"
        "<b>Телефон:</b> +7 (905) 199 93 79"
    ),
    'chelyabinsk': (
        "<b>Челябинск</b>\n\n"
        "<b>ООО «Термопласт»</b>\n"
        "<b>Адрес:</b> 454902 г. Челябинск, поселок Шершни, ул. Центральная, 3 «Б» (На территории Челябинского "
        "электромеханического завода)\n\n"
        "<b>Телефон:</b> +7 (351) 214 01 00, +7 (351) 271 87 20\n\n"
        "<b>Режим работы:</b> ПН — ПТ: с 9:00 до 18:00, СБ, ВС — выходные\n\n"
        "<b>Электронная почта:</b> <a href='mailto:sale@termo-plast.ru'>sale@termo-plast.ru</a>"
    )
}


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Продукция", callback_data='products'),
        InlineKeyboardButton(text="Где купить", callback_data='where_to_buy'),
        InlineKeyboardButton(text="О компании", callback_data='infocomp'),
        InlineKeyboardButton(text="Проекты", callback_data='projects'),
        InlineKeyboardButton(text="Блог", url='https://penoschit.ru/blog/'),  # Кнопка "Блог" со ссылкой
        InlineKeyboardButton(text="Контакты", callback_data='contacts'),
        InlineKeyboardButton(text="Консультация", callback_data='dillers')
    ]
    keyboard.add(*buttons)

    with open('image/LOGOPENO.png', 'rb') as photo:
        await message.answer_photo(photo=photo,
                                   caption="Пенощит - с 2007 года - производство изделий из пенопласта\n\n"
                                           "Наш сайт - https://penoschit.ru/",
                                   reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'contacts')
async def process_contacts_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='back_to_main')
    keyboard.add(back_button)

    new_text = (
        "<b>АДРЕС:</b>\n"
        "г. Челябинск, ул. Центральная, д. 3Б\n\n"
        "<b>РЕЖИМ РАБОТЫ:</b>\n"
        "Пн. – Пт.: с 8:00 до 17:00\n"
        "Сб - Вс: выходные\n\n"
        "<b>ТЕЛЕФОН:</b>\n"
        "8 (800) 551-08-96\n\n"
        "<b>E-MAIL:</b>\n"
        "<a href='mailto:sale@penoschit.ru'>sale@penoschit.ru</a>"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'products')
async def process_products_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Маты для теплого водяного пола", callback_data='mats'),
        InlineKeyboardButton(text="Теплораспределительные пластины", callback_data='plates'),
        InlineKeyboardButton(text="Утеплитель для труб", callback_data='insulation'),
        InlineKeyboardButton(text="Назад", callback_data='back_to_main')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(caption="Выберите категорию продукции:",
                                              reply_markup=keyboard)
    await callback_query.answer()


# Обработчик для показа типов матов
@dp.callback_query_handler(lambda c: c.data == 'mats')
async def process_mats_callback(callback_query: CallbackQuery):
    # Удаление ранее отправленных изображений
    if callback_query.message.chat.id in image_message_ids:
        for message_id in image_message_ids[callback_query.message.chat.id]:
            try:
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_id)
            except Exception as e:
                logging.error(f"Ошибка при удалении сообщения: {e}")
        del image_message_ids[callback_query.message.chat.id]

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Стандартные", callback_data='mats_standard'),
        InlineKeyboardButton(text="Формованные", callback_data='mats_shaped'),
        InlineKeyboardButton(text="Назад", callback_data='products')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(caption="Выберите тип матов для теплого водяного пола:",
                                              reply_markup=keyboard)
    await callback_query.answer()


# Обработчик для показа типов стандартных матов
@dp.callback_query_handler(lambda c: c.data == 'mats_standard')
async def process_mats_standard_callback(callback_query: CallbackQuery):
    # Удаление ранее отправленных изображений
    if callback_query.message.chat.id in image_message_ids:
        for message_id in image_message_ids[callback_query.message.chat.id]:
            try:
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_id)
            except Exception as e:
                logging.error(f"Ошибка при удалении сообщения: {e}")
        del image_message_ids[callback_query.message.chat.id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="WF16 100 мм", callback_data='wf16_100mm'),
        InlineKeyboardButton(text="WF16 150 мм", callback_data='wf16_150mm'),
        InlineKeyboardButton(text="WF16 30 мм", callback_data='wf16_30mm'),
        InlineKeyboardButton(text="WF16 40 мм", callback_data='wf16_40mm'),
        InlineKeyboardButton(text="WF16 50 мм", callback_data='wf16_50mm'),
        InlineKeyboardButton(text="WF16 60 мм", callback_data='wf16_60mm'),
        InlineKeyboardButton(text="WF16 70 мм", callback_data='wf16_70mm'),
        InlineKeyboardButton(text="WF16 80 мм", callback_data='wf16_80mm'),
        InlineKeyboardButton(text="WF16 90 мм", callback_data='wf16_90mm'),
        InlineKeyboardButton(text="WF20 100 мм", callback_data='wf20_100mm'),
        InlineKeyboardButton(text="WF20 150 мм", callback_data='wf20_150mm'),
        InlineKeyboardButton(text="WF20 30 мм", callback_data='wf20_30mm'),
        InlineKeyboardButton(text="WF20 40 мм", callback_data='wf20_40mm'),
        InlineKeyboardButton(text="WF20 50 мм", callback_data='wf20_50mm'),
        InlineKeyboardButton(text="WF20 60 мм", callback_data='wf20_60mm'),
        InlineKeyboardButton(text="WF20 70 мм", callback_data='wf20_70mm'),
        InlineKeyboardButton(text="WF20 80 мм", callback_data='wf20_80mm'),
        InlineKeyboardButton(text="WF20 90 мм", callback_data='wf20_90mm'),
        InlineKeyboardButton(text="Назад", callback_data='mats')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(caption="Выберите тип стандартных матов для теплого водяного пола:",
                                              reply_markup=keyboard)
    await callback_query.answer()


# Создаем обработчики для каждого типа мата

async def send_mats_info(callback_query, mat_name, description, image_paths):
    # Удаление ранее отправленных изображений
    if callback_query.message.chat.id in image_message_ids:
        for message_id in image_message_ids[callback_query.message.chat.id]:
            try:
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_id)
            except Exception as e:
                logging.error(f"Ошибка при удалении сообщения: {e}")
        del image_message_ids[callback_query.message.chat.id]

    # Клавиатура с кнопкой "Назад"
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='mats_standard')
    keyboard.add(back_button)

    # Обновление сообщения с информацией о продукте
    await callback_query.message.edit_caption(caption=f"<b>{mat_name}</b>\n\n{description}", parse_mode="HTML",
                                              reply_markup=keyboard)

    # Отправка группы изображений
    media = MediaGroup()
    for image_path in image_paths:
        media.attach_photo(open(image_path, 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохранение ID отправленных сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]

    await callback_query.answer()


# Пример использования для каждого мата

@dp.callback_query_handler(lambda c: c.data == 'wf16_100mm')
async def process_wf16_100mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 100 мм",
        description=(
            "Описание мата для водяного теплого пола с шагом 100 мм и диаметром трубы 16 мм.\n"
            "Монтажный мат для водяного теплого пола Пенощит оригинал!!!"
            "Произведен на заводе изделий из пенополистирола. Удобный и практичный материал для систем водяных теплых "
            "полов с трубой теплоносителя диаметром 16 мм.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 100\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 100.jpg',
            'image/WF16 100(2).jpg',
            'image/WF16 100(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf16_150mm')
async def process_wf16_150mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 150 мм",
        description=(
            "Теплоизоляционный монтажный мат Пенощит для водяного теплого пола. Удобный и практичный материал для "
            "систем водяных теплых полов с трубой теплоносителя диаметром 16 мм.\n\n"
            "Основа подложки в 130 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Толщина теплоизоляции, мм — 150\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 150.jpg',
            'image/WF16 150(2).jpg',
            'image/WF16 150(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf16_30mm')
async def process_wf16_30mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 30 мм",
        description=(
            "Монтажный мат для водяного теплого пола Пенощит оригинал!!! Произведен на заводе изделий из "
            "пенополистирола. Удобный и практичный материал для систем водяных теплых полов с трубой теплоносителя "
            "диаметром 16 мм.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Толщина теплоизоляции, мм — 30\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 30.jpg',
            'image/WF16 30(2).jpg',
            'image/WF16 30(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf16_40mm')
async def process_wf16_40mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 40 мм",
        description=(
            "Подходит для более плотной укладки труб, обеспечивая высокую эффективность обогрева.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Толщина теплоизоляции, мм — 40\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 40.jpg',
            'image/WF16 40(2).jpg',
            'image/WF16 40(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf16_50mm')
async def process_wf16_50mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 50 мм",
        description=(
            "Монтажный мат для водяного теплого пола Пенощит оригинал!!!"
            "Произведен на заводе изделий из пенополистирола. Удобный и практичный материал для систем водяных теплых "
            "полов с трубой теплоносителя диаметром 16 мм.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 50\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 50.jpg',
            'image/WF16 50(2).jpg',
            'image/WF16 50(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf16_60mm')
async def process_wf16_60mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 60 мм",
        description=(
            "Основа подложки в 30 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 60\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 60.jpg',
            'image/WF16 60(2).jpg',
            'image/WF16 60(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf16_70mm')
async def process_wf16_70mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 70 мм",
        description=(
            "Основа подложки в 30 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 70\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 70.jpg',
            'image/WF16 70(2).jpg',
            'image/WF16 70(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf16_80mm')
async def process_wf16_80mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 80 мм",
        description=(
            "Основа подложки в 30 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 80\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 80.jpg',
            'image/WF16 80(2).jpg',
            'image/WF16 80(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf16_90mm')
async def process_wf16_90mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF16 90 мм",
        description=(
            "Монтажный мат для водяного теплого пола Пенощит оригинал!!! Произведен на заводе изделий из "
            "пенополистирола. Удобный и практичный материал для систем водяных теплых полов с трубой теплоносителя "
            "диаметром 16 мм."
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 16\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 90\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF16 90.jpg',
            'image/WF16 90(2).jpg',
            'image/WF16 90(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_100mm')
async def process_wf20_100mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 100 мм",
        description=(
            "Основа подложки в 80 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 100\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 100.jpg',
            'image/WF20 100(2).jpg',
            'image/WF20 100(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_150mm')
async def process_wf20_150mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 150 мм",
        description=(
            "Основа подложки в 130 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 150\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 150.jpg',
            'image/WF20 150(2).jpg',
            'image/WF20 150(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_30mm')
async def process_wf20_30mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 30 мм",
        description=(
            "Подходит для укладки труб в небольших помещениях, обеспечивая равномерное распределение тепла.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 30\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 30.jpg',
            'image/WF20 30(2).jpg',
            'image/WF20 30(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_40mm')
async def process_wf20_40mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 40 мм",
        description=(
            "Основа подложки в 30 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 40\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 40.jpg',
            'image/WF20 40(2).jpg',
            'image/WF20 40(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_50mm')
async def process_wf20_50mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 50 мм",
        description=(
            "Основа подложки в 30 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 50\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 50.jpg',
            'image/WF20 50(2).jpg',
            'image/WF20 50(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_60mm')
async def process_wf20_60mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 60 мм",
        description=(
            "Основа подложки в 40 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 60\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 60.jpg',
            'image/WF20 60(2).jpg',
            'image/WF20 60(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_70mm')
async def process_wf20_70mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 70 мм",
        description=(
            "Основа подложки в 50 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 70\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 70.jpg',
            'image/WF20 70(2)).jpg',
            'image/WF20 70(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_80mm')
async def process_wf20_80mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 80 мм",
        description=(
            "Основа подложки в 60 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 80\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 80.jpg',
            'image/WF20 80(2).jpg',
            'image/WF20 80(1).jpg'
        ]
    )


@dp.callback_query_handler(lambda c: c.data == 'wf20_90mm')
async def process_wf20_90mm_callback(callback_query: CallbackQuery):
    await send_mats_info(
        callback_query,
        mat_name="Мат для теплого водяного пола WF20 90 мм",
        description=(
            "Основа подложки в 70 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
            "плитой водяного теплого пола.\n\n"
            "<b>Характеристики</b>\n"
            "Диаметр трубы, мм — 20\n"
            "Материал — ПСБ-С 35 ТУ\n"
            "Толщина теплоизоляции, мм — 90\n"
            "Расположение бобышек — Сплошное\n"
            "Размеры, мм — 1000x1000"
        ),
        image_paths=[
            'image/WF20 90.jpg',
            'image/WF20 90(2).jpg',
            'image/WF20 90(1).jpg'
        ]
    )


# формированный
@dp.callback_query_handler(lambda c: c.data == 'tb_wf16_50mm')
async def process_tb_wf16_50mm_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='mats_shaped')
    keyboard.add(back_button)

    new_text = (
        "<b>Мат для теплого водяного пола TB WF16 50 мм</b>\n\n"
        "Теплоизоляционный монтажный мат Пенощит для водяного теплого пола. Удобный и практичный материал для систем "
        "водяных теплых полов с трубой теплоносителя диаметром 16 мм.\n\n"
        "Маты Пенощит это сочетание эффективной теплоизоляции, плотной основы и удобной монтажной конструкции. "
        "Основа подложки в 30 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
        "плитой водяного теплого пола. Монтажные проемы расположены с шагом 50 мм и надежно фиксируют трубу "
        "диаметром 16 мм. Это позволяет значительно увеличить скорость и качество монтажа труб теплоносителя. Нет "
        "необходимости в дополнительном креплении трубы. Расход трубы соответствует расчетному. При бетонных "
        "работах риск нарушения укладки труб сведен к минимуму.\n\n"
        "<b>Характеристики</b>\n"
        "Диаметр трубы, мм — 16\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Материал — ПСБ-С 35 ТУ\n"
        "Расположение бобышек — Шахматное\n"
        "Длина, мм — 1000\n"
        "Ширина, мм — 1000"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    # Добавьте пути к вашим 8 изображениям
    media.attach_photo(open('image/fomovani1.jpg', 'rb'))
    media.attach_photo(open('image/fomovani2.jpg', 'rb'))
    media.attach_photo(open('image/fomovani3.jpg', 'rb'))
    media.attach_photo(open('image/fomovani4.jpg', 'rb'))
    media.attach_photo(open('image/fomovani5.jpg', 'rb'))
    media.attach_photo(open('image/fomovani6.jpg', 'rb'))
    media.attach_photo(open('image/fomovani7.jpg', 'rb'))
    media.attach_photo(open('image/fomovani8.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'mats_shaped')
async def process_mats_shaped_callback(callback_query: CallbackQuery):
    if callback_query.message.chat.id in image_message_ids:
        for message_id in image_message_ids[callback_query.message.chat.id]:
            try:
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_id)
            except Exception as e:
                logging.error(f"Ошибка при удалении сообщения: {e}")
        del image_message_ids[callback_query.message.chat.id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="TB WF16 50 мм", callback_data='tb_wf16_50mm'),
        InlineKeyboardButton(text="Назад", callback_data='mats')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(caption="Выберите тип формованных матов для теплого водяного пола:",
                                              reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'plates')
async def process_plates_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих сообщений с изображениями, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            await bot.delete_message(chat_id, message_id)
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Теплораспределительная пластина Пенощит 1х0,13 м", callback_data='plate_penoschit'),
        InlineKeyboardButton(text="Назад", callback_data='products')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(
        caption="Выберите тип теплораспределительных пластин:",
        reply_markup=keyboard
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'plate_penoschit')
async def process_plate_penoschit_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='plates')
    keyboard.add(back_button)

    new_text = (
        "<b>Теплораспределительная пластина Пенощит 1х0,13 м</b>\n\n"
        "Теплораспределительные пластины для водяного теплого пола в системе сухих теплых полов.\n\n"
        "Пластины изготовлены из оцинкованной стали, имеют омега-образный профиль, позволяющий плотно охватить "
        "поверхность труб диаметром 16 мм.\n\n"
        "Пластины распределяют до 95% теплового потока, что существенно увеличивает теплоотдачу трубы водяного "
        "пола.\n\n"
        "Специальные ребра жесткости (по три с каждой стороны) усиливают конструкцию и компенсируют тепловое "
        "расширение металла.\n\n"
        "Тепловая мощность системы 50-200 Вт/м², в зависимости от типа напольного покрытия и способа укладки трубы "
        "(минимальный шаг укладки 150 мм).\n\n"
        "Упаковка гофрокартон. В упаковке 30 шт. (30 метров).\n\n"
        "Размер пластины: 1 000 × 132 × 0,35—0,40 мм\n"
        "Диаметр трубы: 16 мм\n"
        "Материал: оцинкованная сталь\n\n"
        "<b>Характеристики</b>\n"
        "Диаметр трубы, мм — 16\n"
        "Материал — оцинкованная сталь\n"
        "Толщина, мм — 0.3\n"
        "Длина, мм — 1000\n"
        "Ширина, мм — 132"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/teleplast1.jpg', 'rb'))
    media.attach_photo(open('image/teleplast2.jpg', 'rb'))
    media.attach_photo(open('image/teleplast3.jpg', 'rb'))
    media.attach_photo(open('image/teleplast4.jpg', 'rb'))
    media.attach_photo(open('image/teleplast5.jpg', 'rb'))
    media.attach_photo(open('image/teleplast6.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'insulation')
async def process_insulation_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Стандартные", callback_data='insulation_standard'),
        InlineKeyboardButton(text="Формованные", callback_data='insulation_shaped'),
        InlineKeyboardButton(text="Назад", callback_data='products')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(caption="Выберите тип утеплителя для труб:", reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'insulation_shaped')
async def process_insulation_shaped_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Утеплитель для труб из ППС F 108х50 мм 1000 мм",
                             callback_data='pipe_insulation_f108'),
        InlineKeyboardButton(text="Назад", callback_data='insulation')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(
        caption="Выберите конкретный утеплитель:",
        reply_markup=keyboard
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_f108')
async def process_pipe_insulation_f108_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_shaped')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС F 108х50 мм 1000 мм</b>\n\n"
        "Утеплитель для наружной канализационной трубы диаметром 110 -114 мм. Формованная скорлупа Пенощит обеспечит "
        "бесперебойную работу наружных систем водоотведения"
        "и канализации вашего объекта, при нештатных ситуациях, таких как бесснежная Зима или аномальный мороз. Шуба "
        "из скорлупы Пенощит гарантированно способствует доставке"
        "транспортируемой среды к месту назначения, оберегая вашу систему от неприятных ситуаций.\n\n"
        "Запатентованная технология не имеет аналогов и является собственной разработкой компании.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 108\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС F 108х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС F 108х50(1).jpg', 'rb'))
    media.attach_photo(open('image/ППС F 108х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС F 108х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС F 108х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС F 108х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС F 108х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС F 108х50(7).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'insulation_standard')
async def process_insulation_standard_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="ППС 102х50 мм 1000 мм", callback_data='pipe_insulation_102'),
        InlineKeyboardButton(text="ППС 114х50 мм 1000 мм", callback_data='pipe_insulation_114'),
        InlineKeyboardButton(text="ППС 121х50 мм 1000 мм", callback_data='pipe_insulation_121'),
        InlineKeyboardButton(text="ППС 127х50 мм 1000 мм", callback_data='pipe_insulation_127'),
        InlineKeyboardButton(text="ППС 133х50 мм 1000 мм", callback_data='pipe_insulation_133'),
        InlineKeyboardButton(text="ППС 159х50 мм 1000 мм", callback_data='pipe_insulation_159'),
        InlineKeyboardButton(text="ППС 168х50 мм 1000 мм", callback_data='pipe_insulation_168'),
        InlineKeyboardButton(text="ППС 219х50 мм 1000 мм", callback_data='pipe_insulation_219'),
        InlineKeyboardButton(text="ППС 25х50 мм 1000 мм", callback_data='pipe_insulation_25'),
        InlineKeyboardButton(text="ППС 273х50 мм 1000 мм", callback_data='pipe_insulation_273'),
        InlineKeyboardButton(text="ППС 325х50 мм 1000 мм", callback_data='pipe_insulation_325'),
        InlineKeyboardButton(text="ППС 34х50 мм 1000 мм", callback_data='pipe_insulation_34'),
        InlineKeyboardButton(text="ППС 45х50 мм 1000 мм", callback_data='pipe_insulation_45'),
        InlineKeyboardButton(text="ППС 51х50 мм 1000 мм", callback_data='pipe_insulation_51'),
        InlineKeyboardButton(text="ППС 57х50 мм 1000 мм", callback_data='pipe_insulation_57'),
        InlineKeyboardButton(text="ППС 69х50 мм 1000 мм", callback_data='pipe_insulation_69'),
        InlineKeyboardButton(text="ППС 76х50 мм 1000 мм", callback_data='pipe_insulation_76'),
        InlineKeyboardButton(text="ППС 89х50 мм 2000 мм", callback_data='pipe_insulation_89'),
        InlineKeyboardButton(text="Назад", callback_data='insulation')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(caption="Выберите утеплитель для труб из ППС:", reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_102')
async def process_pipe_insulation_f102_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 102х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 102\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 102х50(1).jpg', 'rb'))
    media.attach_photo(open('image/ППС F 108х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 102х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 102х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 102х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 102х50(7).jpg', 'rb'))
    media.attach_photo(open('image/ППС 102х50(40.jpg', 'rb'))
    media.attach_photo(open('image/ППС 102х50.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_114')
async def process_pipe_insulation_f114_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 114х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 114\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_121')
async def process_pipe_insulation_f121_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 121х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 121\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_127')
async def process_pipe_insulation_f127_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 127х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 127\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_133')
async def process_pipe_insulation_f133_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 133х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 133\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 133х50(1).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_159')
async def process_pipe_insulation_f159_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 159х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 159\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 133х50(1).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_168')
async def process_pipe_insulation_f168_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 168х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 168\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 133х50(1).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_219')
async def process_pipe_insulation_f219_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 219х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 219\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 133х50(1).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_25')
async def process_pipe_insulation_f25_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 25х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 25\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_273')
async def process_pipe_insulation_f273_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 273х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 273\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 133х50(1).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_325')
async def process_pipe_insulation_f325_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 325х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 325\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 133х50(1).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 133х50.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_34')
async def process_pipe_insulation_f34_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 34х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 34\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_45')
async def process_pipe_insulation_f45_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 45х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 45\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_51')
async def process_pipe_insulation_f51_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 51х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 51\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_57')
async def process_pipe_insulation_f57_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 57х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 57\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_69')
async def process_pipe_insulation_f69_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 69х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 69\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_76')
async def process_pipe_insulation_f76_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 76х50 мм 1000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 76\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'pipe_insulation_89')
async def process_pipe_insulation_f89_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Удаление предыдущих изображений, если они есть
    if chat_id in image_message_ids:
        for message_id in image_message_ids[chat_id]:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")
        del image_message_ids[chat_id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='insulation_standard')
    keyboard.add(back_button)

    new_text = (
        "<b>Утеплитель для труб из ППС 89х50 мм 2000 мм</b>\n\n"
        "Срок эксплуатации подтвержденный экспериментально (BASF) более 40 лет. "
        "Рабочие температуры от — 180 до +90 градусов Цельсия. "
        "При защите от прямых солнечных лучей срок хранения не ограничен.\n\n"
        "<b>Характеристики:</b>\n"
        "Диаметр трубы, мм — 89\n"
        "Толщина теплоизоляции, мм — 50\n"
        "Срок эксплуатации — более 40 лет\n"
        "Рабочая температура — от -180°С до +90°С"
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/ППС 114х50.jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(6).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(5).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(4).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(3).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(2).jpg', 'rb'))
    media.attach_photo(open('image/ППС 114х50(1).jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    # Сохраняем ID сообщений с изображениями
    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]


@dp.callback_query_handler(lambda c: c.data == 'infocomp')
async def process_infocomp_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='back_to_main')
    keyboard.add(back_button)

    new_text = ("<b>Лицензии и сертификаты</b>\n\nВся продукция торговой марки Пенощит проходит обязательную "
                "сертификацию продукции по ГОСТ, что гарантирует высокое качество и соблюдение российских стандартов.")

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    # Создаем альбом с несколькими изображениями
    media = MediaGroup()
    media.attach_photo(open('image/1license.jpg', 'rb'))
    media.attach_photo(open('image/2license.jpg', 'rb'))

    # Отправляем альбом
    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'back_to_main')
async def back_to_main(callback_query: CallbackQuery):
    if callback_query.message.chat.id in image_message_ids:
        for message_id in image_message_ids[callback_query.message.chat.id]:
            try:
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_id)
            except Exception as e:
                logging.error(f"Ошибка при удалении сообщения: {e}")
        del image_message_ids[callback_query.message.chat.id]

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Продукция", callback_data='products'),
        InlineKeyboardButton(text="Где купить", callback_data='where_to_buy'),
        InlineKeyboardButton(text="О компании", callback_data='infocomp'),
        InlineKeyboardButton(text="Проекты", callback_data='projects'),
        InlineKeyboardButton(text="Блог", url='https://penoschit.ru/blog/'),  # Кнопка "Блог" со ссылкой
        InlineKeyboardButton(text="Контакты", callback_data='contacts'),
        InlineKeyboardButton(text="Консультация", callback_data='dillers')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(
        caption="Пенощит - с 2007 года - производство изделий из пенопласта\n\nНаш сайт - https://penoschit.ru//",
        reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'projects')
async def process_projects_callback(callback_query: CallbackQuery):
    if callback_query.message.chat.id in image_message_ids:
        for message_id in image_message_ids[callback_query.message.chat.id]:
            try:
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_id)
            except Exception as e:
                logging.error(f"Ошибка при удалении сообщения: {e}")
        del image_message_ids[callback_query.message.chat.id]

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="Монтаж и укладка теплого пола с матами Пенощит WF16-50 от компании «ТРИА Комплекс инженерных "
                 "систем» г. Москва",
            callback_data='project1'),
        InlineKeyboardButton(text="Монтаж теплых полов в деревянном доме", callback_data='project2'),
        InlineKeyboardButton(text="Монтаж теплоизоляционных матов на ледовой арене г. Кыштым",
                             callback_data='project3'),
        InlineKeyboardButton(text="Назад", callback_data='back_to_main')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(caption="Выберите проект:", reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'project1')
async def process_project1_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='projects')
    keyboard.add(back_button)

    new_text = (
        "<b>Необходимо было смонтировать систему теплых водяных полов в подвальном помещении загородного дома "
        "площадью 400 кв.м.</b>\n\n"
        "Пенощит WF16-50 представляет собой обычный пенопласт или пенополистирол плотностью от 21 кг/м³ до 25 кг/м³. "
        "Эта продукция имеет все необходимые сертификаты.\n"
        "Для работы была спроектирована монтажа системы напольного отопления по помещениям подвала с использованием "
        "монтажных матов для теплого водяного пола Пенощит.\n\n"
        "Пенополистирол обеспечивает эффективную теплоизоляцию, удобная монтажная конструкция из форм выступов и "
        "проемов надежно фиксирует трубы, а плотная основа пенополистирола позволяет свободно ходить по матам и "
        "работать (трубы не выскакивают, бобышки не разрушаются).\n\n"
        "Основа подложки в 30 мм обеспечивает необходимую тепловую изоляцию между несущим перекрытием и бетонной "
        "плитой водяного «теплого пола»."
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    media.attach_photo(open('image/pro1.jpg', 'rb'))
    media.attach_photo(open('image/pro1.1.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'project2')
async def process_project2_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='projects')
    keyboard.add(back_button)

    new_text = (
        "<b>Монтаж теплых полов в деревянном доме.</b>\n\n"
        "Необходимо произвести монтаж водяных теплых полов в качестве системы отопления в частном деревянном доме. "
        "Сложность проекта заключается в том, что на деревянные перекрытия нет возможность положить бетонную "
        "стяжку.\n\n"
        "<b>Проект монтажа системы отопления деревянного дома с помощью теплых водяных полов</b>\n\n"
        "Так как деревянные основания не предназначены для большой нагрузки в виде цементной стяжки, требуется "
        "выполнить укладку теплого водяного пола сухим способом. Для этого были применены теплоизолирующие маты "
        "Пенощит WF16-50 и теплораспределительные пластины Пенощит.\n\n"
        "Проект выполнен в короткий срок, так как не требуется ждать высыхания бетонной стяжки, которое занимает "
        "минимум 30 дней. Система теплых водяных полов, благодаря использованию теплораспределительных пластин, "
        "в полной мере обогревает деревянный дом."
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    # Добавьте пути к вашим 9 изображениям
    media.attach_photo(open('image/pro2.jpg', 'rb'))
    media.attach_photo(open('image/pro2.1.jpg', 'rb'))
    media.attach_photo(open('image/pro2.2.jpg', 'rb'))
    media.attach_photo(open('image/pro2.3.jpg', 'rb'))
    media.attach_photo(open('image/pro2.4.jpg', 'rb'))
    media.attach_photo(open('image/pro2.5.jpg', 'rb'))
    media.attach_photo(open('image/pro2.6.jpg', 'rb'))
    media.attach_photo(open('image/pro2.7.jpg', 'rb'))
    media.attach_photo(open('image/pro2.8.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'project3')
async def process_project3_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='projects')
    keyboard.add(back_button)

    new_text = (
        "<b>Монтаж теплоизоляционных матов на ледовой арене г. Кыштым</b>\n\n"
        "Необходимо было выполнить теплоизоляцию для ледовой арены с искусственным льдом в г. Кыштым. В пазы матов "
        "должны помещаться трубы с хладагентом, обеспечивающие охлаждение ледового покрытия.\n\n"
        "<b>Нестандартный проект с использованием матов для теплого пола в качестве теплоизоляции для ледовой "
        "арены.</b>\n\n"
        "Трубы хладагента имеют диаметр, отличающийся от труб теплого пола, под которые предназначены стандартные "
        "маты. Для проекта конструкция матов была изменена, чтобы вместить трубы диаметром 25 мм.\n\n"
        "Учитывая вес ледового покрытия и песка, нужно было сохранить плотность материала и увеличить общий слой "
        "теплоизоляции с помощью экструдированного пенополистирола.\n\n"
        "Задача крепления труб диаметром 25 мм с шагом 75 мм была решена с помощью измененных матов Пенощит. "
        "Изменения не повлияли на плотность материала, что подтверждается его прочностью под большой нагрузкой."
    )

    await callback_query.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=keyboard)

    media = MediaGroup()
    # Добавьте пути к вашим 9 изображениям
    media.attach_photo(open('image/pro3.jpg', 'rb'))
    media.attach_photo(open('image/pro3.1.jpg', 'rb'))
    media.attach_photo(open('image/pro3.2.jpg', 'rb'))
    media.attach_photo(open('image/pro3.3.jpg', 'rb'))
    media.attach_photo(open('image/pro3.4.jpg', 'rb'))
    media.attach_photo(open('image/pro3.5.jpg', 'rb'))
    media.attach_photo(open('image/pro3.6.jpg', 'rb'))
    media.attach_photo(open('image/pro3.7.jpg', 'rb'))
    media.attach_photo(open('image/pro3.8.jpg', 'rb'))

    message = await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

    image_message_ids[callback_query.message.chat.id] = [msg.message_id for msg in message]

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'where_to_buy')
async def process_where_to_buy_callback(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Сургут", callback_data='surgut'),
        InlineKeyboardButton(text="Бийск", callback_data='biysk'),
        InlineKeyboardButton(text="Брянск", callback_data='bryansk'),
        InlineKeyboardButton(text="Волгоград", callback_data='volgograd'),
        InlineKeyboardButton(text="Горно-Алтайск", callback_data='gorno_altaysk'),
        InlineKeyboardButton(text="Екатеринбург", callback_data='ekaterinburg'),
        InlineKeyboardButton(text="Ижевск", callback_data='izhevsk'),
        InlineKeyboardButton(text="Иркутск", callback_data='irkutsk'),
        InlineKeyboardButton(text="Липецк", callback_data='lipetsk'),
        InlineKeyboardButton(text="Москва", callback_data='moscow'),
        InlineKeyboardButton(text="Новороссийск", callback_data='novorossiysk'),
        InlineKeyboardButton(text="Пермь", callback_data='perm'),
        InlineKeyboardButton(text="Самара", callback_data='samara'),
        InlineKeyboardButton(text="Симферополь", callback_data='simferopol'),
        InlineKeyboardButton(text="Чебоксары", callback_data='cheboksary'),
        InlineKeyboardButton(text="Челябинск", callback_data='chelyabinsk'),
        InlineKeyboardButton(text="Назад", callback_data='back_to_main')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(caption="Выберите город, где можно купить продукцию:",
                                              reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data in cities_info)
async def process_city_callback(callback_query: CallbackQuery):
    city_info = cities_info[callback_query.data]
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="Назад", callback_data='where_to_buy')
    keyboard.add(back_button)

    # Указываем parse_mode="HTML" для обработки разметки
    await callback_query.message.edit_caption(caption=city_info, reply_markup=keyboard, parse_mode="HTML")
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'back_to_main')
async def back_to_main(callback_query: CallbackQuery):
    if callback_query.message.chat.id in image_message_ids:
        for message_id in image_message_ids[callback_query.message.chat.id]:
            try:
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_id)
            except Exception as e:
                logging.error(f"Ошибка при удалении сообщения: {e}")
        del image_message_ids[callback_query.message.chat.id]

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Продукция", callback_data='products'),
        InlineKeyboardButton(text="Где купить", callback_data='where_to_buy'),
        InlineKeyboardButton(text="О компании", callback_data='infocomp'),
        InlineKeyboardButton(text="Проекты", callback_data='projects'),
        InlineKeyboardButton(text="Блог", url='https://penoschit.ru/blog/'),  # Кнопка "Блог" со ссылкой
        InlineKeyboardButton(text="Контакты", callback_data='contacts'),
        InlineKeyboardButton(text="Консультация", callback_data='dillers')
    ]
    keyboard.add(*buttons)

    await callback_query.message.edit_caption(
        caption="Пенощит - с 2007 года - производство изделий из пенопласта\n\nНаш сайт - https://penoschit.ru/",
        reply_markup=keyboard)
    await callback_query.answer()


# Обработчик для кнопки "Консультация"
@dp.callback_query_handler(lambda c: c.data == 'dillers')
async def process_dillers_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Инициализация данных пользователя и текущего шага
    user_data[chat_id] = {}
    user_steps[chat_id] = 0

    # Сохранение ID сообщения с кнопкой "Консультация" для последующего удаления
    user_data[chat_id]['message_ids'] = [callback_query.message.message_id]

    # Отправка первого вопроса
    await ask_question(chat_id)
    await callback_query.answer()


# Обработчики для ответов на вопросы
@dp.message_handler(lambda message: message.chat.id in user_data)
async def handle_answers(message: types.Message):
    chat_id = message.chat.id
    step = user_steps[chat_id]

    # Сохранение ответа на текущий вопрос
    if step == 0:
        user_data[chat_id]['name'] = message.text
    elif step == 1:
        user_data[chat_id]['phone'] = message.text
    elif step == 2:
        user_data[chat_id]['message'] = message.text

    # Сохраняем ID сообщения с ответом пользователя для последующего удаления
    user_data[chat_id]['message_ids'].append(message.message_id)

    user_steps[chat_id] += 1  # Переход к следующему вопросу

    if user_steps[chat_id] < len(questions):
        await ask_question(chat_id)  # Отправляем следующий вопрос
    else:
        await confirm_data(chat_id)  # Все вопросы заданы, предлагаем отправить данные


async def ask_question(chat_id):
    step = user_steps[chat_id]
    keyboard = InlineKeyboardMarkup(row_width=1)
    if step > 0:
        back_button = InlineKeyboardButton(text="Назад", callback_data='go_back')
        keyboard.add(back_button)

    # Отправляем следующий вопрос
    question_message = await bot.send_message(
        chat_id=chat_id,
        text=f"{questions[step]}:",
        reply_markup=keyboard
    )

    # Сохраняем ID сообщения с вопросом для последующего удаления
    user_data[chat_id]['message_ids'].append(question_message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'go_back')
async def go_back(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_steps[chat_id] -= 1  # Переход на предыдущий вопрос
    await ask_question(chat_id)
    await callback_query.answer()


async def confirm_data(chat_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    send_button = InlineKeyboardButton(text="Отправить", callback_data='send_data')
    edit_button = InlineKeyboardButton(text="Редактировать", callback_data='edit_data')
    keyboard.add(send_button, edit_button)

    text = (
        f"Проверьте введенные данные:\n\n"
        f"<b>Имя:</b> {user_data[chat_id]['name']}\n"
        f"<b>Телефон:</b> {user_data[chat_id]['phone']}\n"
        f"<b>Сообщение:</b> {user_data[chat_id]['message']}\n\n"
        "Если все верно, нажмите 'Отправить'."
    )

    confirm_message = await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=keyboard)
    user_data[chat_id]['message_ids'].append(confirm_message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'send_data')
async def send_data(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    data = user_data.get(chat_id)

    logging.info(f"Data to send: {data}")

    if data:
        # Получение username пользователя
        username = callback_query.from_user.username
        username_text = f"<b>Username:</b> @{username}\n" if username else ""

        text = (
            f"Новая заявка:\n\n"
            f"{username_text}"
            f"<b>Имя:</b> {data['name']}\n"
            f"<b>Телефон:</b> {data['phone']}\n"
            f"<b>Сообщение:</b> {data['message']}"
        )

        # Отправка сообщения с данными заявки
        await bot.send_message(chat_id=TARGET_USER_ID, text=text, parse_mode="HTML")

        # Удаление всех сообщений пользователя и вопросов
        for message_id in user_data[chat_id].get('message_ids', []):
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception as e:
                logging.error(f"Ошибка при удалении сообщения: {e}")

        # Очищаем данные пользователя
        user_data.pop(chat_id, None)
        user_steps.pop(chat_id, None)

        # Переход в главное меню, вызывая send_welcome
        await send_welcome(callback_query.message)

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'edit_data')
async def edit_data(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_steps[chat_id] = 0  # Возвращаемся к первому вопросу
    await ask_question(chat_id)
    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

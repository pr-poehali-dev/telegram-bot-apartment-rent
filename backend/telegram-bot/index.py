import json
import os
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor

TELEGRAM_TOKEN = "8107172432:AAEfZlmEo2i2_9w0JClHO0mgTv11oGAhQuk"
PAYMENT_CARD = "2200702117990650"
APARTMENT_PHOTO = "https://cdn.poehali.dev/projects/c5b06ca4-39bb-4041-bf85-1b585378500e/files/d18eeb22-f3a5-492f-90b4-74329736b1ee.jpg"

PRICES = {
    "1_day": 2500,
    "2_days": 3500,
    "3_days": 1500,
    "weekend": 4500
}

def get_db_connection():
    """Создание подключения к базе данных"""
    return psycopg2.connect(os.environ['DATABASE_URL'])

def send_message(chat_id: int, text: str, reply_markup=None):
    """Отправка сообщения через Telegram API"""
    import urllib.request
    import urllib.parse
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def send_photo(chat_id: int, photo_url: str, caption: str, reply_markup=None):
    """Отправка фото через Telegram API"""
    import urllib.request
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    data = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error sending photo: {e}")
        return None

def handle_start(chat_id: int, user_data: dict):
    """Обработка команды /start"""
    keyboard = {
        "inline_keyboard": [
            [{"text": "🏠 Посмотреть квартиру", "callback_data": "view_apartment"}],
            [{"text": "💰 Узнать цены", "callback_data": "view_prices"}],
            [{"text": "📅 Забронировать", "callback_data": "book_start"}],
            [{"text": "📞 Контакты", "callback_data": "contacts"}]
        ]
    }
    
    welcome_text = (
        f"Привет, {user_data.get('first_name', 'друг')}! 👋\n\n"
        "Сдаю уютную квартиру посуточно.\n"
        "Выбери действие:"
    )
    
    send_message(chat_id, welcome_text, keyboard)

def handle_view_apartment(chat_id: int):
    """Показать фото квартиры и описание"""
    caption = (
        "🏠 <b>Уютная квартира посуточно</b>\n\n"
        "✨ Характеристики:\n"
        "• Современный ремонт\n"
        "• Wi-Fi высокая скорость\n"
        "• Полностью оборудованная кухня\n"
        "• Чистое постельное белье\n"
        "• Уютная атмосфера\n\n"
        "📍 Удобное расположение\n"
        "🚗 Парковка рядом"
    )
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "💰 Узнать цены", "callback_data": "view_prices"}],
            [{"text": "📅 Забронировать", "callback_data": "book_start"}],
            [{"text": "◀️ Назад", "callback_data": "start"}]
        ]
    }
    
    send_photo(chat_id, APARTMENT_PHOTO, caption, keyboard)

def handle_view_prices(chat_id: int):
    """Показать цены"""
    prices_text = (
        "💰 <b>Цены на проживание</b>\n\n"
        f"1 сутки — {PRICES['1_day']}₽\n"
        f"2 суток — {PRICES['2_days']}₽\n"
        f"3 суток — {PRICES['3_days']}₽\n"
        f"Выходные (пт-вс) — {PRICES['weekend']}₽\n\n"
        "✅ В стоимость входит:\n"
        "• Чистое белье и полотенца\n"
        "• Wi-Fi интернет\n"
        "• Все коммунальные услуги\n"
        "• Чай, кофе, сахар"
    )
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📅 Забронировать", "callback_data": "book_start"}],
            [{"text": "◀️ Назад", "callback_data": "start"}]
        ]
    }
    
    send_message(chat_id, prices_text, keyboard)

def handle_book_start(chat_id: int):
    """Начать процесс бронирования"""
    keyboard = {
        "inline_keyboard": [
            [{"text": "1 сутки — 2500₽", "callback_data": "book_1_day"}],
            [{"text": "2 суток — 3500₽", "callback_data": "book_2_days"}],
            [{"text": "3 суток — 1500₽", "callback_data": "book_3_days"}],
            [{"text": "Выходные — 4500₽", "callback_data": "book_weekend"}],
            [{"text": "◀️ Назад", "callback_data": "start"}]
        ]
    }
    
    text = (
        "📅 <b>Бронирование квартиры</b>\n\n"
        "Выберите тариф:"
    )
    
    send_message(chat_id, text, keyboard)

def handle_booking(chat_id: int, user_data: dict, period: str):
    """Обработка бронирования"""
    price = PRICES.get(period, 0)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    check_in = datetime.now().date() + timedelta(days=1)
    
    if period == "1_day":
        check_out = check_in + timedelta(days=1)
        period_text = "1 сутки"
    elif period == "2_days":
        check_out = check_in + timedelta(days=2)
        period_text = "2 суток"
    elif period == "3_days":
        check_out = check_in + timedelta(days=3)
        period_text = "3 суток"
    else:
        check_out = check_in + timedelta(days=3)
        period_text = "Выходные"
    
    user_id = user_data.get('id', 0)
    username = user_data.get('username', '')
    first_name = user_data.get('first_name', '')
    
    cur.execute(
        "INSERT INTO bookings (user_id, username, first_name, check_in, check_out, price, status) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (
            user_id,
            username,
            first_name,
            check_in,
            check_out,
            price,
            'pending'
        )
    )
    
    booking_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    payment_text = (
        f"✅ <b>Бронирование №{booking_id}</b>\n\n"
        f"📅 Период: {period_text}\n"
        f"📆 Заезд: {check_in.strftime('%d.%m.%Y')}\n"
        f"📆 Выезд: {check_out.strftime('%d.%m.%Y')}\n"
        f"💰 Сумма: {price}₽\n\n"
        f"💳 <b>Для оформления оплатите на карту:</b>\n"
        f"<code>{PAYMENT_CARD}</code>\n\n"
        "После оплаты свяжитесь со мной для подтверждения."
    )
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📞 Связаться", "callback_data": "contacts"}],
            [{"text": "◀️ В главное меню", "callback_data": "start"}]
        ]
    }
    
    send_message(chat_id, payment_text, keyboard)

def handle_contacts(chat_id: int):
    """Показать контакты"""
    text = (
        "📞 <b>Контакты</b>\n\n"
        "По всем вопросам:\n"
        "• Telegram: @Vgcidj\n"
        "• Быстрый ответ гарантирован\n\n"
        "📍 <b>Расположение:</b>\n"
        "г. Мелитополь, Запорожская область\n\n"
        "🕐 Заезд: после 14:00\n"
        "🕐 Выезд: до 12:00\n\n"
        "⚠️ <b>Правила проживания:</b>\n"
        "• Максимум 4 человека\n"
        "• Без домашних животных\n"
        "• Не курить в помещении\n"
        "• Соблюдать тишину после 23:00"
    )
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "◀️ В главное меню", "callback_data": "start"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def handler(event: dict, context) -> dict:
    """Обработчик webhook-запросов от Telegram"""
    
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    try:
        body_str = event.get('body', '{}')
        if isinstance(body_str, str):
            body = json.loads(body_str)
        else:
            body = body_str
        
        if 'message' in body:
            message = body['message']
            chat_id = message['chat']['id']
            user_data = message['from']
            text = message.get('text', '')
            
            if text == '/start':
                handle_start(chat_id, user_data)
        
        elif 'callback_query' in body:
            callback = body['callback_query']
            chat_id = callback['message']['chat']['id']
            user_data = callback['from']
            data = callback['data']
            
            if data == 'start':
                handle_start(chat_id, user_data)
            elif data == 'view_apartment':
                handle_view_apartment(chat_id)
            elif data == 'view_prices':
                handle_view_prices(chat_id)
            elif data == 'book_start':
                handle_book_start(chat_id)
            elif data.startswith('book_'):
                period = data.replace('book_', '')
                handle_booking(chat_id, user_data, period)
            elif data == 'contacts':
                handle_contacts(chat_id)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'ok': True}),
            'isBase64Encoded': False
        }
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error: {e}\n{error_details}")
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)}),
            'isBase64Encoded': False
        }
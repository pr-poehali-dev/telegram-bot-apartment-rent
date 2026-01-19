import urllib.request
import json

TELEGRAM_TOKEN = "8107172432:AAEfZlmEo2i2_9w0JClHO0mgTv11oGAhQuk"
WEBHOOK_URL = "https://functions.poehali.dev/d71d3052-e88c-4ba3-845e-aef9588860d8"

def set_webhook():
    """Установка webhook для Telegram бота"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    data = {
        "url": WEBHOOK_URL,
        "drop_pending_updates": True
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Webhook установлен: {result}")
            return result
    except Exception as e:
        print(f"Ошибка установки webhook: {e}")
        return None

def get_webhook_info():
    """Получить информацию о webhook"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
    
    try:
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Webhook info: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
    except Exception as e:
        print(f"Ошибка получения webhook info: {e}")
        return None

def delete_webhook():
    """Удалить webhook"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
    
    try:
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Webhook удален: {result}")
            return result
    except Exception as e:
        print(f"Ошибка удаления webhook: {e}")
        return None

if __name__ == "__main__":
    print("Настройка Telegram бота...")
    print(f"Token: {TELEGRAM_TOKEN}")
    print(f"Webhook URL: {WEBHOOK_URL}")
    print("\n1. Удаляем старый webhook (если есть)...")
    delete_webhook()
    print("\n2. Устанавливаем новый webhook...")
    set_webhook()
    print("\n3. Проверяем статус webhook...")
    get_webhook_info()
    print("\n✅ Готово! Бот настроен и работает.")
    print("Теперь можно писать боту в Telegram!")

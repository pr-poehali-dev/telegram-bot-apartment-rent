import json
import urllib.request

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
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def get_webhook_info():
    """Получить информацию о webhook"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
    
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))

def handler(event: dict, context) -> dict:
    """Автоматическая настройка webhook для Telegram бота"""
    
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    try:
        set_result = set_webhook()
        
        webhook_info = get_webhook_info()
        
        response_data = {
            "success": True,
            "webhook_set": set_result,
            "webhook_info": webhook_info,
            "bot_url": f"https://t.me/{webhook_info.get('result', {}).get('url', '').split('/')[-1] if webhook_info.get('ok') else 'bot'}",
            "message": "Бот полностью настроен и работает!"
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data, ensure_ascii=False),
            'isBase64Encoded': False
        }
    
    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }, ensure_ascii=False),
            'isBase64Encoded': False
        }

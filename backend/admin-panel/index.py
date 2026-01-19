import json
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Создание подключения к базе данных"""
    return psycopg2.connect(os.environ['DATABASE_URL'])

def get_all_bookings():
    """Получить все бронирования"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("""
        SELECT 
            id,
            user_id,
            username,
            first_name,
            check_in,
            check_out,
            price,
            status,
            created_at
        FROM bookings
        ORDER BY created_at DESC
    """)
    
    bookings = cur.fetchall()
    cur.close()
    conn.close()
    
    result = []
    for booking in bookings:
        result.append({
            'id': booking['id'],
            'user_id': booking['user_id'],
            'username': booking['username'],
            'first_name': booking['first_name'],
            'check_in': booking['check_in'].strftime('%Y-%m-%d') if booking['check_in'] else None,
            'check_out': booking['check_out'].strftime('%Y-%m-%d') if booking['check_out'] else None,
            'price': booking['price'],
            'status': booking['status'],
            'created_at': booking['created_at'].strftime('%Y-%m-%d %H:%M:%S') if booking['created_at'] else None
        })
    
    return result

def update_booking_status(booking_id: int, status: str):
    """Обновить статус бронирования"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE bookings SET status = %s WHERE id = %s",
        (status, booking_id)
    )
    
    conn.commit()
    cur.close()
    conn.close()

def handler(event: dict, context) -> dict:
    """API для админ-панели управления бронированиями"""
    
    method = event.get('httpMethod', 'GET')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    try:
        if method == 'GET':
            bookings = get_all_bookings()
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': True,
                    'bookings': bookings,
                    'total': len(bookings)
                }, ensure_ascii=False),
                'isBase64Encoded': False
            }
        
        elif method == 'POST':
            body_str = event.get('body', '{}')
            if isinstance(body_str, str):
                body = json.loads(body_str)
            else:
                body = body_str
            
            booking_id = body.get('booking_id')
            new_status = body.get('status')
            
            if not booking_id or not new_status:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'success': False,
                        'error': 'booking_id и status обязательны'
                    }, ensure_ascii=False),
                    'isBase64Encoded': False
                }
            
            update_booking_status(booking_id, new_status)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': True,
                    'message': 'Статус обновлён'
                }, ensure_ascii=False),
                'isBase64Encoded': False
            }
        
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Method not allowed'}, ensure_ascii=False),
                'isBase64Encoded': False
            }
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error: {e}\n{error_details}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False),
            'isBase64Encoded': False
        }

import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')

users = dynamodb.Table('Users')
sessions = dynamodb.Table('Sessions')
feedback = dynamodb.Table('Feedback')

def lambda_handler(event, context):

    method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')
    path = event.get('path', '')

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*'
    }

    # =========================
    # CORS
    # =========================
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': 'OK'
        }

    # =========================
    # LOGIN
    # =========================
    elif path.endswith('/login') and method == 'POST':
        body = json.loads(event.get('body') or "{}")

        email = body.get('email', '').strip().lower()
        password = body.get('password')

        res = users.scan()

        user = None
        for u in res['Items']:
            if u.get('email', '').strip().lower() == email:
                user = u
                break

        if not user:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'msg': 'User not found'})
            }

        if user.get('password') != password:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'msg': 'Wrong password'})
            }

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(user)
        }

    # =========================
    # ADD SESSION
    # =========================
    elif path.endswith('/add-session') and method == 'POST':
        body = json.loads(event.get('body') or "{}")

        if not body.get('title'):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'msg': 'Title required'})
            }

        sessions.put_item(Item={
            'session_id': str(uuid.uuid4()),
            'title': body.get('title')
        })

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'msg': 'Session added'})
        }

    # =========================
    # DELETE SESSION (FIXED)
    # =========================
    elif '/session/' in path and method == 'DELETE':
        session_id = path.split('/')[-1]

        if not session_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'msg': 'Session ID required'})
            }

        sessions.delete_item(Key={
            'session_id': session_id
        })

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'msg': 'Session deleted'})
        }

    # =========================
    # GET SESSIONS
    # =========================
    elif path.endswith('/sessions') and method == 'GET':
        res = sessions.scan()

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(res['Items'])
        }

    # =========================
    # SUBMIT FEEDBACK
    # =========================
    elif path.endswith('/feedback') and method == 'POST':
        body = json.loads(event.get('body') or "{}")

        if not body.get('email') or not body.get('session_id') or not body.get('message'):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'msg': 'All fields required'})
            }

        feedback.put_item(Item={
            'id': str(uuid.uuid4()),
            'email': body.get('email').strip().lower(),
            'session_id': body.get('session_id'),
            'message': body.get('message')
        })

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'msg': 'Saved'})
        }

    # =========================
    # GET FEEDBACK
    # =========================
    elif path.endswith('/feedback') and method == 'GET':
        res = feedback.scan()

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(res['Items'])
        }

    # =========================
    # ANALYTICS
    # =========================
    elif path.endswith('/analytics') and method == 'GET':
        res = feedback.scan()
        items = res.get('Items', [])

        total_feedback = len(items)

        session_count = {}

        for f in items:
            sid = f.get('session_id')
            if not sid:
                continue

            session_count[sid] = session_count.get(sid, 0) + 1

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'total_feedback': total_feedback,
                'session_wise': session_count
            })
        }

    # =========================
    # INVALID
    # =========================
    else:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'msg': 'Invalid route',
                'path': path,
                'method': method
            })
        }
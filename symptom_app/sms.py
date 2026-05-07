import requests

def send_sms(phone, message):
    url = "https://www.fast2sms.com/dev/bulkV2"

    # ensure 10-digit number
    phone = str(phone)[-10:]

    payload = {
        "route": "v3",
        "sender_id": "TXTIND",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": phone,
    }

    headers = {
        "authorization": "YOUR_API_KEY_HERE",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    # ✅ DEBUG OUTPUT (correct place)
    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)

    return response.json()
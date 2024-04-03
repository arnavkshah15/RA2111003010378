from flask import Flask, request, jsonify
import requests
import time
from collections import deque

app = Flask(__name__)

SIZE = 10
noofwindow = deque(maxlen=SIZE)

URL = "http://20.244.56.144/test/"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzEyMTUyMjM3LCJpYXQiOjE3MTIxNTE5MzcsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6Ijc5MDRjMWVmLTg4NGItNDczNC1iYjZkLTljYmMwODM3ZDE3OSIsInN1YiI6ImFrMDMzOUBzcm1pc3QuZWR1LmluIn0sImNvbXBhbnlOYW1lIjoiU2hhaCBNYXJ0IiwiY2xpZW50SUQiOiI3OTA0YzFlZi04ODRiLTQ3MzQtYmI2ZC05Y2JjMDgzN2QxNzkiLCJjbGllbnRTZWNyZXQiOiJyS2VpSXdHd0dhekhMUktYIiwib3duZXJOYW1lIjoiQXJuYXYiLCJvd25lckVtYWlsIjoiYWswMzM5QHNybWlzdC5lZHUuaW4iLCJyb2xsTm8iOiJSQTIxMTEwMDMwMTAzNzgifQ.Ty5eKdWYMP0PmCUTQF3EzodSVvLISFjuxrOPYNOUcNY"


def fetch(number_id):
    try:
        endpoint = f"{URL}/{number_id}" 
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        numbers = response.json()["numbers"]
        return numbers
    except requests.exceptions.RequestException as e:
        print("Error in fetching", e)
        return []


def process_and_store_numbers(numbers):
    for number in numbers:
        if number not in noofwindow:
            if len(noofwindow) >= SIZE:
                noofwindow.popleft()
            noofwindow.append(number)


@app.route('/numbers/<number_id>')
def get_numbers(number_id):
    try:
        start_time = time.time()

        numbers = fetch(number_id)
        process_and_store_numbers(numbers)

        avg = sum(noofwindow) / len(noofwindow) if noofwindow else 0

        response_data = {
            "numbers": numbers,
            "windowPrevState": list(noofwindow)[:-len(numbers)],
            "windowCurrState": list(noofwindow),
            "avg": avg
        }

        response_time = time.time() - start_time
        if response_time > 0.5:
            print("Response time exceeded")

        return jsonify(response_data)

    except Exception as e:
        print("Error:", e)
        return "Server Error", 500


if __name__ == '__main__':
    app.run(debug=True, port=9876)

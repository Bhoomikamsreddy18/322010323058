from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def fetch_numbers(url):
    try:
        response = requests.get('http://20.244.56.144/numbers/primes')
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
    except Exception as e:
        print(f"Error fetching numbers from {url}: {e}")
    return []


@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('http://20.244.56.144/numbers/primes')
    all_numbers = []

    for url in urls:
        print(f"numbers: {'http://20.244.56.144/numbers/primes'}")
        numbers = fetch_numbers("http://20.244.56.144/numbers/primes")
        print(f"Numbers fetched: {numbers}")
        all_numbers.extend(numbers)

    unique_sorted_numbers = sorted(list(set(all_numbers)))
    print(f" {unique_sorted_numbers}")

    return jsonify(numbers=unique_sorted_numbers)


if __name__ == '__main__':
    app.run(host='localhost', port=3000)

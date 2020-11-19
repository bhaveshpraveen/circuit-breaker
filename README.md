Install requests and flask (to mock server's failure and success messages)
```python
pip install requests
pip install Flask
```

Let's create some endpoints to mock the server
```python
# main.py
import random

from flask import Flask
app = Flask(__name__)


@app.route('/success')
def success_endpoint():
    return {
        "msg": "Call to this endpoint was a smashing success."
    }, 200


@app.route('/failure')
def faulty_endpoint():
    return {
        "msg": "I will fail."
    }, 500


@app.route('/random')
def fail_randomly_endpoint():
    r = random.randint(0, 1)
    if r == 0:
        return {
            "msg": "Success msg"
        }, 200

    return {
        "msg": "I will fail (sometimes)."
    }, 200

```

Run the development server
```python
 export FLASK_APP=main.py; flask run
```
By default it runs on port 5000


Create a file `cirbreaker.py`
```python
# cirbreaker.py
import requests


faulty_endpoint = "http://localhost:5000/failure"
success_endpoint = "http://localhost:5000/success"
random_status_endpoint = "http://localhost:5000/random"


def make_request(url):
    response = requests.get(url)
    print(f"Status code = {response.status_code}")
    print(f"Content={response.content}")


def main():
    make_request(success_endpoint)


if __name__ == "__main__":
    main()
```

Run this file now:
```bash
$ python cirbreaker.py
Status code = 200
Content=b'{"msg":"Call to this endpoint was a smashing success."}\n'
```

There are times when the endpoint might fail in production for various reasons. So, let's add a retry mechanism. 
```python
import http

import requests


faulty_endpoint = "http://localhost:5000/failure"
success_endpoint = "http://localhost:5000/success"
random_status_endpoint = "http://localhost:5000/random"


def make_request(url):
    # Retry 5 times before giving up.
    for i in range(0, 5):
        response = requests.get(url)
        if response.status_code == http.HTTPStatus.OK:
            print(f"Call to {url} succeed with status code = {response.status_code}")
            return
        print(f"Call to {url} failed with status code: {response.status_code}.\nRetrying.....")

    raise Exception(f"Call to {url} failed even after multiple retries")


def main():
    make_request(success_endpoint)
    make_request(faulty_endpoint)


if __name__ == "__main__":
    main()
```

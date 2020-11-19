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
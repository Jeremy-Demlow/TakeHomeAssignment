import pandas as pd
import requests
import json


def send_request(file_path, url, total):
    test_data = pd.read_csv(file_path)
    sample_data = test_data.head(total)
    sample_json_batch = sample_data.to_json(orient="records")
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"data": json.loads(sample_json_batch)})
    response = requests.post(url, headers=headers, data=data)
    return response


def main():
    file_path = "statefarm/files/data/exercise_26_test.csv"
    url_simple = "http://0.0.0.0:1313/batch_predict_simple"
    url = "http://0.0.0.0:1313/batch_predict"

    print("Sending small batch request...")
    response_simple = send_request(file_path, url_simple, 2)
    print("Status Code:", response_simple.status_code)
    print("Response Body:", response_simple.json())

    print("\nSending large batch request...")
    response = send_request(file_path, url, 5000)
    print("Status Code:", response.status_code)
    print("Hiding full response of 5,000")


if __name__ == "__main__":
    main()

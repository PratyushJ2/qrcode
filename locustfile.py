# Runs with this line locust -f locustfile.py --headless --host=http:// -u 100 -r 10 -t 1m

from locust import HttpUser, task, between, events
import random

class QRUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def save_qr(self):
        payload = {"qrdata": f"QR-{random.randint(1000, 9999)}"}
        headers = {"Content-Type": "application/json"}

        response = self.client.post("/random", json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Failed: {response.status_code}, {response.text}")

# Stop on first failure
@events.request.add_listener
def stop_on_failure(request_type, name, response_time, response_length, response=None, exception=None, context=None, **kwargs):
    if exception:
        env = kwargs.get("environment")
        if env and env.runner:
            total_requests = env.stats.total.num_requests
            print(f"\nStopping test due to failure on {name}: {exception}")
            print(f"Total requests handled before failure: {total_requests}")
            env.runner.quit()

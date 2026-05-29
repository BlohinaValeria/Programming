from locust import HttpUser, task, between

class HabrUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://habr.com"
    def on_start(self):
        print("Habr load test started")
    
    @task
    def load_main_page(self):
        with self.client.get("/ru", catch_response=True) as response:
            if response.status_code == 200:
                print("Page loaded: /ru")
                response.success()
            else:
                error_msg = f"Failed to load /ru: Status code {response.status_code}"
                print(error_msg)
                response.failure(error_msg)
    
    def on_stop(self):
        print("Habr load test finished")

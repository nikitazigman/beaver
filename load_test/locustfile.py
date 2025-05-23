from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(5)
    def get_script(self):
        self.client.get("/api/v1/code_documents/code_document/")

    @task
    def get_tags(self):
        self.client.get("/api/v1/tags/")

    @task
    def get_languages(self):
        self.client.get("/api/v1/languages/")

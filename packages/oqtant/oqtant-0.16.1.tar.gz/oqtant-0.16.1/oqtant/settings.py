from pydantic import BaseSettings


class Settings(BaseSettings):
    auth0_base_url: str = "https://coldquanta-dev.us.auth0.com"
    auth0_client_id: str = "ZzQdn5ZZq1dmpP5N55KINr33u47RBRiu"
    auth0_scope: str = "offline_access bec_dev_service:client"
    auth0_audience: str = "https://albert-dev.coldquanta.com/oqtant"
    signin_local_callback_url: str = "http://localhost:8080"
    base_url: str = "https://albert-dev.coldquanta.com/api/jobs"
    max_ind_var: int = 2
    max_job_batch_size: int = 30

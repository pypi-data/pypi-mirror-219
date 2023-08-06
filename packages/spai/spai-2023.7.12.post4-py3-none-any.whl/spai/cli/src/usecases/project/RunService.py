from pydantic import BaseModel


class RunService:
    def __init__(self, repo):
        self.repo = repo

    class Inputs(BaseModel):
        user: dict
        service: str
        files: dict
        data: dict

    class Outputs(BaseModel):
        message: str

    def __call__(self, inputs: Inputs) -> Outputs:
        message = self.repo.run_service(
            inputs.user, inputs.service, inputs.files, inputs.data
        )
        return self.Outputs(message=message)

class Job:
    def __init__(
        self,
        company:str,
        salary:int,
        location: str,
        remote: bool = False
        ):
        self.company = company
        self.salary = salary
        self.location = location
        self.remote = remote

    def __str__(self):
        return f"{self.company} | {self.salary} | {self.location} | {self.remote}"

    def is_suitable(
        self, 
        minimum_salary: int, 
        location: str, 
        remote: bool
        ) -> bool:
        return (
            self.salary >= minimum_salary
            and self.location == location
            and self.remote == remote
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "company": self.company,
            "salary": self.salary,
            "location": self.location,
            "remote": self.remote
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Job":
        return cls(
            data["company"],
            data["salary"],
            data["location"],
            data["remote"]
        )
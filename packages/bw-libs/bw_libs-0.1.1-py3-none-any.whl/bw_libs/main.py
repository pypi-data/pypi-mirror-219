from pydantic import BaseModel


class Company(BaseModel):
    identifier: int
    name: str


def is_the_same(c1: Company, c2: Company):
    return c1.identifier == c2.identifier

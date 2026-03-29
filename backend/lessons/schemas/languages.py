from pydantic import BaseModel


class LanguagesPair(BaseModel):
    lang1_id: int
    lang2_id: int

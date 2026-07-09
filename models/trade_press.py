from pydantic import BaseModel


class TradePressArticle(BaseModel):
    title: str
    url: str
    content: str
    source: str | None = None
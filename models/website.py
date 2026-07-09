from pydantic import BaseModel


class WebsiteContent(BaseModel):
    url: str
    content: str
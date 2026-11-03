from pydantic import HttpUrl,BaseModel


class URLCreate(BaseModel):
    long_url: HttpUrl

class URLResponse(BaseModel):
    short_url: str


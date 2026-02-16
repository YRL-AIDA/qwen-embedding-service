from typing import Dict, List, Union

from pydantic import BaseModel



class Message(BaseModel):
    type: str

    text: Union[str, None] = None
    image: Union[str, None] = None
    image_url: Union[str, None] = None



class EmbedRequest(BaseModel):
    messages: List[Message]

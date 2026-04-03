from typing import Annotated, List, Union

from pydantic import BaseModel, ConfigDict


# Request
class EmbedRequest(BaseModel):
    messages: List[Message]



class Message(BaseModel):
    model_config = ConfigDict(extra='ignore')

    type: str
    text: Union[str, None] = None
    image: Union[str, None] = None
    image_url: Union[str, None] = None



# Response
class EmbedSuccessResponse(BaseModel):
    messages: List[MessageEmbedding]



class MessageEmbedding(BaseModel):
    message_id: int
    embedding: List[float]

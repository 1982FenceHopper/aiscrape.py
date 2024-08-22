from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional

### Processing Schemas

class news_schema(BaseModel):
    """The schema to follow for removing all HTML tags to return the raw text in a news article, from a raw HTML document."""
    
    entry: Optional[str] = Field(..., description="Title of the news article")
    content: Optional[str] = Field(..., description="For this, remove all the HTML/CSS tags surrounding the news article")
    # input_document: Optional[str] = Field(..., description="The exact verbatim contents of the input document")
    # token_input: Optional[int] = Field(..., description="Number of tokens in the input")
    # token_worked: Optional[int] = Field(..., description="Number of tokens that was taken in processing")
    # word_tokens: Optional[bool] = Field(..., description="Whether or not the input was considered in terms of word tokens, if false, then letter tokens were used")
    
class encyclopedia_schema(BaseModel):
    """The schema to follow for removing all HTML tags to return the raw text in an encyclopedia entry, from a raw HTML document."""
    
    entry: Optional[str] = Field(..., description="Title of the encyclopedia entry")
    content: Optional[str] = Field(..., description="For this, remove all the HTML/CSS tags surrounding the encyclopedia text")
    # input_document: Optional[str] = Field(..., description="The exact verbatim contents of the input document")
    # token_input: Optional[int] = Field(..., description="Number of tokens in the input")
    # token_worked: Optional[int] = Field(..., description="Number of tokens that was taken in processing")
    # word_tokens: Optional[bool] = Field(..., description="Whether or not the input was considered in terms of word tokens, if false, then letter tokens were used")
    
### Choice Schemas

class best_choice_schema(BaseModel):
    """Use this to provide the best choice between summaries"""
    
    choice: Optional[int] = Field(..., description="The entry that seems more informational to any subject wanting to learn from it. Indexing starts from 0")
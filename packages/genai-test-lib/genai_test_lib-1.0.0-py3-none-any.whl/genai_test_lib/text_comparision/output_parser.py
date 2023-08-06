from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


class OutputParser(BaseModel):
    comparison_score: float = Field(description="comparison_score")
    keywords: List[str] = Field(description="keywords")
    reason: str = Field(description="reason")
    def to_dict(self):
        return {
            "comparison_score": self.comparison_score,
            "keywords": self.keywords,
            "reason": self.reason,
        }
output_res_parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=OutputParser)
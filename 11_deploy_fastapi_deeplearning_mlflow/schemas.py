from pydantic import BaseModel


class Comment(BaseModel):
    comment: str

    class Config:
        schema_extra = {
            "example": {
                "comment": "Among the many lovely details of this film are views about the gender barriers in the Middle East and the customs of a city that, while modern, is still a culture of men. As Juliette and Tareq wander the streets of Cairo we recognize subtleties that exist, subtleties that director Nadda never forces. The gorgeous cinematography is by Luc Montpellier and the musical score is by Niall Byrne. This film is more a poem than a story, a welcome change from the usual youngster-oriented love stories and more of a mature episode of ageless flirtation."
            }
        }
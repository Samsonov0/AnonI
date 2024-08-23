from pydantic import BaseModel


class ExtraPathSettings(BaseModel):
    exclude_middlewares: tuple[str | None, ...] = [None]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

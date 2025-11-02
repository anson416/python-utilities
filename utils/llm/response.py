from typing import Annotated, Any

from pydantic import BaseModel, Field, validate_call
from typing_extensions import Self

ZERO_SHOT_COT_REASONING = '"Let\'s think step by step. <<FILL_IN>>"'


class ResponseModelParsingError(RuntimeError):
    pass


class ResponseModel(BaseModel, validate_assignment=True, strict=True):
    @classmethod
    def to_str(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def from_str(cls, text: str) -> Self:
        raise NotImplementedError()


class JsonResponseModel(ResponseModel):
    @classmethod
    @validate_call
    def to_str(
        cls,
        _indent: Annotated[int, Field(ge=0)] = 2,
        _depth: Annotated[int, Field(ge=1)] = 1,
        **substitutions: Any,
    ) -> str:
        output = "{\n"
        for i, (name, field) in enumerate(cls.model_fields.items()):
            output += " " * (_indent * _depth)
            output += f'"{name}": '
            if issubclass(field.annotation, JsonResponseModel):
                output += field.annotation.to_str(
                    _depth=_depth + 1, _indent=_indent, **substitutions
                )
            elif issubclass(field.annotation, bool):
                output += substitutions.get(name, "true/false")
            elif issubclass(field.annotation, (float, int)):
                output += substitutions.get(name, "<<FILL_IN>>")
            elif issubclass(field.annotation, str):
                output += substitutions.get(name, '"<<FILL_IN>>"')
            else:
                raise RuntimeError(f"Unsupported type: {field.annotation}")
            output += f"{',' if i < len(cls.model_fields) - 1 else ''}\n"
        output += " " * (_indent * (_depth - 1)) + "}"
        return output

    @classmethod
    @validate_call
    def from_str(cls, text: str) -> Self:
        from .parser import JsonParser

        parsed = JsonParser()(text)
        if parsed is None:
            raise ResponseModelParsingError(
                "No JSON object could be extracted"
            )
        try:
            return cls.model_validate(parsed)
        except Exception as e:
            raise ResponseModelParsingError(
                f"Failed to parse response into {cls.__name__}: {str(e)}"
            ) from e

from typing import Type

class Validator:
    def validate(self, value) -> tuple[bool, list[str]]:
        return True, []
    
class Transformer:
    def transform(self, value):
        raise NotImplementedError("Override me!")
    
class Field:
    def __init__(self, *, null: bool = False, default = None):
        self._value = default
        self._validators: list[Validator] = []
        self._transformers: list[Transformer] = []
        self._errors: list[str] = []
        self._null = null
        self._valid: bool | None = None

    def __validate(self):
        self._valid = True
        if self._value is None:
            if not self._null:
                self._valid = False
                self._errors.append("Field is required.")
            return  # don't bother running validators on None
        for validator in self._validators:
            valid, errors, = validator.validate(self._value)
            if not valid:
                self._valid = False
                self._errors.extend(errors)
        if self._valid:
            for transformer in self._transformers:
                self._value = transformer.transform(self._value)

    def value(self):
        if self.valid():
            return self._value

    def load(self, value):
        self._errors = []
        self._valid = None
        if value is not None:
            self._value = value

    def valid(self) -> bool:
        if self._valid is None:
            self.__validate()
        return self._valid

    def errors(self) -> list[str] | None:
        if self._valid is None:
            self.__validate()
        return self._errors
    
class BooleanTransformer(Transformer):
    def transform(self, value):
        return True if value else False

class BooleanField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._transformers.append(
            BooleanTransformer()
        )

class IntValidator(Validator):
    def __init__(self, *, min_value: int | None = None, max_value: int | None = None):
        super().__init__()
        self.__min_value = min_value
        self.__max_value = max_value
    
    def validate(self, value) -> tuple[bool, list[str]]:
        valid, errors = super().validate(value)
        try:
            value = int(value)
            if self.__min_value is not None and value < self.__min_value:
                valid = False
                errors.append("Value is too small.")
            if self.__max_value is not None and value > self.__max_value:
                valid = False
                errors.append("Value is too large.")
        except:
            valid = False
            errors.append("Value cannot be converted to an integer.")
        return valid, errors

class IntTransformer:
    def transform(self, value):
        return int(value)

class IntField(Field):
    def __init__(
        self,
        *,
        min_value: int | None = None,
        max_value: int | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._validators.append(
            IntValidator(
                min_value=min_value,
                max_value=max_value,
            )
        )
        self._transformers.append(
            IntTransformer()
        )

class FloatValidator(Validator):
    def __init__(self, *, min_value: float | None = None, max_value: float | None = None):
        super().__init__()
        self.__min_value = min_value
        self.__max_value = max_value
    
    def validate(self, value) -> tuple[bool, list[str]]:
        valid, errors = super().validate(value)
        try:
            value = float(value)
            if self.__min_value is not None and value < self.__min_value:
                valid = False
                errors.append("Value is too small.")
            if self.__max_value is not None and value > self.__max_value:
                valid = False
                errors.append("Value is too large.")
        except:
            valid = False
            errors.append("Value cannot be converted to a float.")
        return valid, errors

class FloatTransformer:
    def transform(self, value):
        return float(value)

class FloatField(Field):
    def __init__(
        self,
        *,
        min_value: float | None = None,
        max_value: float | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._validators.append(
            FloatValidator(
                min_value=min_value,
                max_value=max_value,
            )
        )
        self._transformers.append(
            FloatTransformer()
        )

class StringValidator(Validator):
    def __init__(self, *, min_length: int | None = None, max_length: int | None = None):
        super().__init__()
        self.__min_length = min_length
        self.__max_length = max_length

    def validate(self, value) -> tuple[bool, list[str]]:
        valid, errors = super().validate(value)
        try:
            value = str(value)
            if self.__min_length is not None and len(value) < self.__min_length:
                valid = False
                errors.append("Value is too short.")
            if self.__max_length is not None and len(value) > self.__max_length:
                valid = False
                errors.append("Value is too long.")
        except:
            valid = False
            errors.append("Value cannot be converted to a string.")
        return valid, errors

class StringTransformer:
    def transform(self, value):
        return str(value)

class StringField(Field):
    def __init__(
        self,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._validators.append(
            StringValidator(
                min_length=min_length,
                max_length=max_length,
            )
        )
        self._transformers.append(
            StringTransformer()
        )

class ArrayValidator(Validator):
    def __init__(self, *, element_field: Field, min_size: int | None = None, max_size: int | None = None):
        super().__init__()
        self.__element_field = element_field
        self.__min_size = min_size
        self.__max_size = max_size

    def __validate_element(self, element_value) -> tuple[bool, list[str]]:
        self.__element_field.load(element_value)
        return self.__element_field.valid(), self.__element_field.errors()

    def validate(self, value) -> tuple[bool, list[str]]:
        valid, errors = super().validate(value)
        try:
            value = list(value)
            if self.__min_size is not None and len(value) < self.__min_size:
                valid = False
                errors.append("Array is too small.")
            if self.__max_size is not None and len(value) > self.__max_size:
                valid = False
                errors.append("Array is too large.")
            for e in value:
                element_valid, element_errors = self.__validate_element(e)
                if not element_valid:
                    valid = False
                    errors.extend(element_errors)
        except:
            valid = False
            errors.append("Value cannot be converted to an array.")
        return valid, errors
    
class ArrayTransformer(Transformer):
    def __init__(self, *, element_field: Field):
        self.__element_field = element_field

    def __transform_element(self, element_value):
        self.__element_field.load(element_value)
        return self.__element_field.value()

    def transform(self, value):
        return list(self.__transform_element(e) for e in list(value))

class ArrayField(Field):
    def __init__(
        self,
        *,
        element_field: Field,
        min_size: int | None = None,
        max_size: int | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._validators.append(
            ArrayValidator(
                element_field=element_field,
                min_size=min_size,
                max_size=max_size,
            )
        )
        self._transformers.append(
            ArrayTransformer(
                element_field=element_field,
            )
        )

class DictValidator(Validator):
    def __init__(self, *, element_field: Field, min_size: int | None = None, max_size: int | None = None):
        super().__init__()
        self.__element_field = element_field
        self.__min_size = min_size
        self.__min_size = max_size

    def __validate_element(self, element_value) -> tuple[bool, list[str]]:
        self.__element_field.load(element_value)
        return self.__element_field.valid(), self.__element_field.errors()

    def validate(self, value) -> tuple[bool, list[str]]:
        valid, errors = super().validate(value)
        try:
            value = dict(value)
            if self.__min_size is not None and len(value) < self.__min_size:
                valid = False
                errors.append("Dict is too small.")
            if self.__min_size is not None and len(value) > self.__min_size:
                valid = False
                errors.append("Dict is too large.")
            for e in value.values():
                element_valid, element_errors = self.__validate_element(e)
                if not element_valid:
                    valid = False
                    errors.extend(element_errors)
        except:
            valid = False
            errors.append("Value cannot be converted to a dict.")
        return valid, errors
    
class DictTransformer(Transformer):
    def __init__(self, *, element_field: Field):
        self.__element_field = element_field

    def __transform_element(self, element_value):
        self.__element_field.load(element_value)
        return self.__element_field.value()

    def transform(self, value):
        return dict((k, self.__transform_element(v)) for k, v in dict(value).items())

class DictField(Field):
    def __init__(
        self,
        *,
        element_field: Field,
        min_size: int | None = None,
        max_size: int | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._validators.append(
            DictValidator(
                element_field=element_field,
                min_size=min_size,
                max_size=max_size,
            )
        )
        self._transformers.append(
            DictTransformer(
                element_field=element_field,
            )
        )
    
class JSONObject:
    def __init__(self):
        self._fields: dict[str, Field] = {}
        self._errors: dict[str, list[str]] = {}
        self._valid: bool | None = None

    def __validate(self):
        self._valid = True
        for key, field in self._fields.items():
            if not field.valid():
                self._valid = False
                self._errors[key] = field.errors()

    def value(self) -> dict | None:
        return dict((k, v.value()) for k, v in self._fields.items())

    def load(self, json_raw: dict):
        self._errors = {}
        self._valid = None
        for key, field in self._fields.items():
            field.load(json_raw.get(key))

    def valid(self) -> bool:
        if self._valid is None:
            self.__validate()
        return self._valid

    def errors(self) -> dict[str, list[str]] | None:
        if self._valid is None:
            self.__validate()
        return self._errors

class ObjectTransformer(Transformer):
    def __init__(self, *, cls: Type[JSONObject]):
        super().__init__()
        self.__cls = cls

    def transform(self, value):
        obj = self.__cls()
        obj.load(value)
        return obj.value()

class ObjectField(Field):
    def __init__(
        self,
        *,
        cls: Type[JSONObject],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._transformers.append(ObjectTransformer(cls=cls))


# class TestObject2(JSONObject):
#     def __init__(self):
#         super().__init__()

#         self._fields["int"] = IntField()

#         self._fields["float"] = FloatField()

# class TestObject(JSONObject):
#     def __init__(self):
#         super().__init__()

#         self._fields["int"] = IntField()

#         self._fields["float"] = FloatField()

#         self._fields["str"] = StringField()

#         self._fields["arr[int]"] = ArrayField(
#             element_field=FloatField()
#         )

#         self._fields["obj"] = TestObject2()


# if __name__ == "__main__":
#     a = TestObject()
#     a.load(
#         {
#             "int": 1,
#             "float": 2.5,
#             "str": "abc",
#             "arr[int]": [1,2,3],
#             "obj": {
#                 "int": "2",
#                 "float": "3",
#             }
#         }
#     )
#     print(a.valid())
#     print(a.errors())
#     print(a.value())
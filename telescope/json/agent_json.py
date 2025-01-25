from telescope.utils.validated_json import JSONObject, IntField, FloatField, StringField, ArrayField, DictField, ObjectField, BooleanField

class CPU(JSONObject):
    def __init__(self):
        super().__init__()

        self._fields["count"] = IntField(min_value=0)

        self._fields["physical"] = IntField(min_value=0)

        self._fields["usage"] = ArrayField(
            element_field=FloatField(min_value=0),
        )

        self._fields["freq_mhz"] = ArrayField(
            element_field=FloatField(min_value=0),
        )

class Memory(JSONObject):
    def __init__(self):
        super().__init__()

        self._fields["total_kb"] = IntField(min_value=0)

        self._fields["free_kb"] = IntField(min_value=0)

        self._fields["used_kb"] = IntField(min_value=0)

        self._fields["available_kb"] = IntField(min_value=0)

class Storage(JSONObject):
    def __init__(self):
        super().__init__()

        self._fields["device"] = StringField(min_length=1, max_length=64)

        self._fields["total_kb"] = IntField(min_value=0)

        self._fields["free_kb"] = IntField(min_value=0)

        self._fields["used_kb"] = IntField(min_value=0)

        self._fields["utilization"] = FloatField(min_value=0)

class Temperature(JSONObject):
    def __init__(self):
        super().__init__()
        self._fields["name"] = StringField(max_length=128)

        self._fields["temp_c"] = FloatField(min_value=0)

class Fan(JSONObject):
    def __init__(self):
        super().__init__()
        self._fields["name"] = StringField(max_length=128)

        self._fields["rpm"] = FloatField(min_value=0)

class Battery(JSONObject):
    def __init__(self):
        super().__init__()
        self._fields["charge"] = FloatField(min_value=0)

        self._fields["standby"] = BooleanField()

class AgentDataBody(JSONObject):
    def __init__(self):
        super().__init__()

        self._fields["load"] = ArrayField(
            element_field=FloatField(min_value=0),
        )

        self._fields["cpu"] = ObjectField(
            cls=CPU,
        )

        self._fields["memory"] = ObjectField(
            cls=Memory
        )

        self._fields["storage"] = DictField(
            element_field=ObjectField(cls=Storage)
        )

        self._fields["temps"] = DictField(
            element_field=ArrayField(
                element_field=ObjectField(cls=Temperature)
            )
        )

        self._fields["fans"] = DictField(
            element_field=ArrayField(
                element_field=ObjectField(cls=Fan)
            )
        )


class AgentData(JSONObject):
    def __init__(self):
        super().__init__()

        self._fields["version"] = StringField(
            max_length=16,
        )
        
        self._fields["agent_id"] = StringField(
            min_length=16,
            max_length=16,
        )

        self._fields["agent_secret"] = StringField(
            min_length=32,
            max_length=32,
        )

        self._fields["body"] = ObjectField(
            cls=AgentDataBody
        )
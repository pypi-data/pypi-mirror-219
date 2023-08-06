import json


class Template:

    def __init__(self):
        self.attribute_name = ""
        self.template_id = ""
        self.sanitized_name = ""
        self.attribute_type = ""
        self.data_type = ""
        self.description = None
        self.interpolation = None
        self.uom = None

    def to_json(self):
        return json.dumps(self.build())

    def build(self):

        payload = {
            "name": self.attribute_name,
            "templateId": self.template_id,
            "sanitizedName": self.sanitized_name,
            "attributeType": self.attribute_type,
            "dataType": self.data_type
        }

        if self.description is not None:
            payload["description"] = self.description

        if self.interpolation is not None:
            payload["interpolationMethod"] = self.interpolation

        if self.uom is not None:
            payload["uom"] = self.uom

        return payload

    def __str__(self):

        return str(self.build())

"""
version: 2.8
added: set_bubble
"""


import json
import os
import shortuuid


class Annotation:

    def __init__(self, category, parent = None):
        self.id = shortuuid.uuid()
        self.parent = parent
        self.inputType = category.get('inputType')
        self.required = category.get('required', False)
        self.key = category.get('key')
        self.description = category.get('description', "")
        self.metadata = category.get('metadata')
        self.is_selected = False
        self.on_select = None
        self.data = None
        self.on_data = None

        if self.inputType and self.inputType != "text":
            self.children = []
            for choice in category['choices']:
                child = Annotation(choice, self)
                self.children.append(child)
                child.parent = self
        else:
            self.children = None

    def set_on_data(self, on_data):
        self.on_data = on_data

    def set_on_select(self, on_select):
        self.on_select = on_select

    def toggle(self):
        if self.is_selected:
            self.unset()
        else:
            self.set()

    def set(self, data=None):
        self.is_selected = True
        if self.inputType == "text":
            self.data = data
        elif self.inputType == "mutual":
            for child in self.children:
                if data is None or child.key != data:
                    child.unset()
                else:
                    child.set()
        if self.parent and self.parent.inputType == "mutual":
            for child in self.parent.children:
                if child.is_selected and child != self:
                    child.unset()
        if self.on_select:
            self.on_select(self.is_selected)
        if self.on_data:
            self.on_data(self.data)

    def unset(self):
        self.is_selected = False
        self.data = None
        if self.children:
            for child in self.children:
                child.unset()
        if self.on_select:
            self.on_select(self.is_selected)


    def set_bubble(self, data=None):
        self.is_selected = True
        if self.inputType == "text":
            self.data = data
        if self.parent is not None:
            self.parent.set_bubble()


    def __compile(self):
        if not self.is_selected:
            return None
        if self.inputType == "text":
            return { 'key': self.key, 'value': self.data }
        elif self.inputType == "mutual":
            for child in self.children:
                if child.is_selected:
                    return { 'key': self.key, 'value': child.__compile() }
        elif self.inputType in ["multiple", "property"]:
            data = []
            for child in self.children:
                if child.is_selected:
                    cc = child.__compile()
                    if cc is not None:
                        data.append(cc)
            return { 'key': self.key, 'value': data }
        elif self.inputType is None:
            return { 'key': self.key }

    def compile(self, value_first=False):
        data_obj = self.__compile()
        if value_first:
            return data_obj.get('value')
        return data_obj

    def __decompile(self, annotation):
        self.is_selected = True
        if self.inputType == "text":
            self.data = annotation.get('value')
        elif self.inputType in ["multiple", "property"]:
            for item in annotation.get('value'):
                for child in self.children:
                    if item.get('key') == child.key:
                        child.__decompile(item)
        elif self.inputType == "mutual":
            if annotation.get('value') is not None:
                for child in self.children:
                    if annotation.get('value').get('key') == child.key:
                        child.__decompile(annotation.get('value'))
                        break

    def __fireevents(self):
        if self.on_select:
            self.on_select(True)
        if self.inputType == "text":
            if self.on_data:
                self.on_data(self.data)
        elif self.inputType in ["multiple", "property", "mutual"]:
            for child in self.children:
                if child.is_selected:
                    child.__fireevents()

    def decompile(self, annotation, value_first=False):
        self.unset()
        self.__decompile({ 'value': annotation } if value_first else annotation)
        self.__fireevents()


    def __querySelector(self, annotation, tokens):
        token = tokens[0]
        parts = token.split(".")

        if annotation["key"] == parts[0] or parts[0] == "*":
            tokens = tokens[1:]
            if len(tokens) == 0:
                if len(parts) == 1:
                    return True if self.inputType is None else annotation["value"]
                elif parts[1] == "description":
                    return self.description
                elif parts[1] == "key":
                    return self.key
                elif parts[1] == "inputType":
                    return self.inputType

        if "value" in annotation:
            value = annotation["value"]
            if isinstance(value, list):
                for c in self.children:
                    for child in value:
                        if c.key == child["key"]:
                            result = c.__querySelector(child, tokens)
                            if result is not None:
                                return result
                            break
            elif isinstance(value, dict):
                for c in self.children:
                    if c.key == value["key"]:
                        return c.__querySelector(value, tokens)

        return None

    def querySelector(self, annotation, selector, value_first=False):
        tokens = selector.split(" ")
        if value_first:
            result = self.__querySelector(
                {"key": None, "value": annotation}, tokens)
        else:
            result = self.__querySelector(annotation, tokens)
        return None if result is None else result

    def __traverse(self, annotation, handler):
        handler(self, annotation)
        if "value" in annotation:
            value = annotation["value"]
            if isinstance(value, list):
                for c in self.children:
                    for child in value:
                        if c.key == child["key"]:
                            c.__traverse(child, handler)
            elif isinstance(value, dict):
                for c in self.children:
                    if c.key == value["key"]:
                        c.__traverse(value, handler)

    def traverse(self, annotation, handler, value_first=False):
        if value_first:
            self.__traverse({"key": None, "value": annotation}, handler)
        else:
            self.__traverse(annotation, handler)

    def get_all_nodes(self):
        nodes = [self]
        for c in self.children:
            nodes += c.get_all_nodes()
        return nodes

    def __queryMetadata(self, tokens):
        token = tokens[0]
        parts = token.split(".")

        if self.key == parts[0] or parts[0] == "*":
            tokens = tokens[1:]
            if len(tokens) == 0:
                if len(parts) == 1:
                    return self
                elif parts[1] == "data":
                    return self.is_selected if self.inputType is None else self.data;
                elif parts[1] == "description":
                    return self.description
                elif parts[1] == "key":
                    return self.key
                elif parts[1] == "inputType":
                    return self.inputType

        if isinstance(self.children, list):
            for c in self.children:
                result = c.__queryMetadata(tokens)
                if result is not None:
                    return result

        return None

    def queryMetadata(self, selector):
        tokens = selector.split(" ")
        result = self.__queryMetadata(tokens)
        return None if result is None else result


if __name__ == '__main__':
    va = Annotation({
        "inputType": "multiple",
        "choices": [
        {
            "key": "car",
            "inputType": "mutual",
            "description": "รถ",
            "metadata":
            {
                "a": 1,
                "b":
                {
                    "c": 2
                }
            },
            "choices": [
            {
                "key": "type",
                "inputType": "mutual",
                "description": "ประเภท",
                "choices": [
                {
                    "key": "car",
                    "description": "รถเก๋ง"
                },
                {
                    "key": "van",
                    "description": "รถตู้"
                }]
            },
            {
                "key": "lp_text",
                "inputType": "text",
                "description": "เลขทะเบียน"
            }]
        },
        {
            "key": "lp",
            "inputType": "property",
            "description": "ป้ายทะเบียน",
            "required": True,
            "choices": [
            {
                "key": "lp_color",
                "description": "มีสี"
            },
            {
                "key": "lp_type",
                "inputType": "mutual",
                "description": "ประเภทป้าย",
                "choices": [
                {
                    "key": "lpr",
                    "description": "ป้ายทะเบียนรถยนต์"
                },
                {
                    "key": "mlpr",
                    "description": "ป้ายทะเบียนรถมอไซด์"
                }]
            }]
        }]
    })

    va.queryMetadata("lp_text").set_bubble("1234")
    va.queryMetadata("lp_color").set_bubble()
    print(va.compile())
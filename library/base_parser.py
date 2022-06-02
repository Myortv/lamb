import re
from library.sql_master import get_value


class BaseParser:

    def __init__(self):
        self.fields = ()
        self.int_fields = ()
        self.bool_fields = ()
        self.relate_fields = dict()
        # self.relate_fields = {'type', 'notetype_relations'}

    def creation(self, text, **kwargs):
        if text is None:
            return None
        raw_data = re.split(r"\n\d{1,2}\.", text)[1:]
        data = dict()

        for i in self.fields:
            data[i] = raw_data.pop(0).strip()

        for i in self.int_fields:
            data[i] = int(data[i])

        for i in self.bool_fields:
            if data[i].lower() in {'yes', 'y', 'да', 'д', 'k', 'ok', 'к', 'ok', 'true', 't'}:
                data[i] = True
            else:
                data[i] = False

        for field in self.relate_fields:
            _, data[field] = get_value(
                self.relate_fields[field], (field, data[field]))

        data.update(**kwargs)
        return data


    def updation(self, text):
        if text is None:
            return None
        text = text.split('\n', 1)[1]

        field_key, content = text.split('.', 1)
        field = self.fields[int(field_key)-1]
        content = content.strip()

        del(text,field_key)

        if field in self.int_fields:
            content = int(content)

        elif field in self.bool_fields:
            if content.lower() in {'yes', 'y', 'да', 'д', 'k', 'ok', 'к', 'ok', 'true', 't'}:
                content = True
            else:
                content = False

        elif field in self.relate_fields:
            _, content = get_value(self.relate_fields[field], (field, content))

        return {field: content}

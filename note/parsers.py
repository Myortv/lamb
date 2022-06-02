from library.base_parser import BaseParser


class NoteParser(BaseParser):

    def __init__(self):
        self.fields = ('title', 'type', 'amount', 'content', 'is_public', 'character')
        self.int_fields = ('amount', 'character')
        self.bool_fields = ('is_public', )
        self.relate_fields = dict()

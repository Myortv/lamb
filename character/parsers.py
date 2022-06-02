from library.base_parser import BaseParser

class CharacterParser(BaseParser):

    def __init__(self):
        super().__init__()
        self.fields = ('name', 'age', 'race', 'signs', 'content')
        self.int_fields = ('age',)

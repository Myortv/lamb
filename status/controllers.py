from library.sql_master import get_value
from library.base_controllers import (
                        BaseController,
                        UpdateLineMixin,
                        IncrementationMixin
                    )

from conf.configs import DESCRIPTIONS

from .templates import status_template
# from parsers import

class LevelingController(BaseController, UpdateLineMixin, IncrementationMixin):
    def __init__(self, template=status_template):
        super().__init__(template=template)
        self.db = 'status'

    async def incrementate(self, url, char_id, field, gain):
        id, _ = get_value(self.db, ('character', char_id))
        url = f"{url}{id}/"
        return await super().incrementate(url, gain, field)

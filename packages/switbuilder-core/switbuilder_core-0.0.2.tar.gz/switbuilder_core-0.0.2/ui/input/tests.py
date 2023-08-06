import unittest

from ui.common.Button import Button
from ui.common.Icon import Icon
from ui.common.StaticAction import StaticAction
from ui.header.ContextMenuItem import ContextMenuItem
from ui.header.Header import Header
from ui.input.Input import Input
from ui.swit_response.Container import Container


class Test(unittest.TestCase):
    def test_valid_input(self):
        _input = Input(
            type='text_input',
            action_id='searchRecord',
            placeholder='Search',
            trigger_on_input=True
        )

        given = {'type': 'text_input',
                 'action_id': 'searchRecord',
                 'placeholder': 'Search',
                 'trigger_on_input': True}

        self.assertEqual(given, _input.dict(exclude_none=True))

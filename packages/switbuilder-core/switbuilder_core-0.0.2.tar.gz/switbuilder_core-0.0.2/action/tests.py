import datetime
import unittest

from action.constants import init_state, ViewIdTypes
from action.schemas import State
from ui.utils import compress_and_b64encode
from workspace.schemas import Workspace


class Test(unittest.TestCase):
    def test_state_from_init_state(self):
        s = State(**init_state)
        for key in init_state:
            self.assertEqual(getattr(s, key), init_state[key])

    def test_state_from_bytes(self):
        b = compress_and_b64encode(init_state)
        s = State.from_bytes(b)
        for key in init_state:
            self.assertEqual(getattr(s, key), init_state[key])

        self.assertEqual(b, s.to_bytes())

    def test_state_email_list_view(self):
        new_state_dict: dict = {
            **init_state,
            "email_list_view": {
                'new_view': {'view_id': ViewIdTypes.right_panel,
                             'state': '',
                             'header': {
                                 "title": "This is a view title",
                                 "subtitle": "Add a subtitle if needed",
                                 "context_menu": [
                                     {
                                         "label": "Menu item 1",
                                         "action_id": "2fc5573a-c439-4131-9c82-6ed78c1f1758"
                                     },
                                 ]
                             },
                             'body': {'elements': [
                                 {'type': 'text_input',
                                  'action_id': 'searchRecord',
                                  'placeholder': 'Search',
                                  'trigger_on_input': True},
                                 {'type': 'divider'},

                             ]}}
            }
        }
        b = compress_and_b64encode(new_state_dict)
        s = State(**new_state_dict)
        self.assertEqual(s.to_bytes(), b)
        byte_from_state = s.to_bytes()
        new_state = State.from_bytes(byte_from_state)
        self.assertEqual(new_state.email_list_view, new_state_dict["email_list_view"])

    def test_state_instance_save(self):
        state = State(**init_state)
        self.assertEqual(state.workspaces, [])
        self.assertEqual(state.channels, [])

        new_state = state.update({
            "workspaces": [
                Workspace(
                    admin_ids=["aa"],
                    color="aa",
                    created=datetime.datetime.now(),
                    domain="aa",
                    id="aa",
                    master_id="aa",
                    name="aa",
                    photo="aa"
                ),
                Workspace(
                    admin_ids=["bb"],
                    color="bb",
                    created=datetime.datetime.now(),
                    domain="bb",
                    id="bb",
                    master_id="bb",
                    name="bb",
                    photo="bb"
                )
            ]
        })

        self.assertEqual(len(new_state.workspaces), 2)
        byte = new_state.to_bytes()
        state_from_byte: State = State.from_bytes(byte)
        for workspace in state_from_byte.workspaces:
            self.assertIsInstance(workspace, Workspace)

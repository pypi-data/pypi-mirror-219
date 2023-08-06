from action.constants import ViewIdTypes, ActionIdTypes


class ActionId:
    def __init__(self, view_id_type: ViewIdTypes, action_id_type: ActionIdTypes, data: str):
        self.view_id_type = view_id_type
        self.action_id_type = action_id_type
        self.data = data

    def to_str(self) -> str:
        return f"{self.view_id_type.value}::{self.action_id_type.value}::{self.data}"

    @staticmethod
    def from_str(action_id: str) -> 'ActionId':
        view_id_type, action_id_type, data = action_id.split('::')
        return ActionId(ViewIdTypes(view_id_type), ActionIdTypes(action_id_type), data)

from collections import defaultdict

from src.type import DrawerHandler


class PathResolver:

    def __init__(self, id: str, paths: list[str]) -> None:
        self._id: str = id
        self.paths: list[str] = paths

    @property
    def combined_path(self) -> str:
        path: str = '/'.join(self.paths)
        return f'{self._id}/{path}'

    @property
    def id(self) -> str:
        return self._id

    @staticmethod
    def from_combined(combined_id: str) -> 'PathResolver':
        arr: list[str] = combined_id.split('/')
        return PathResolver(arr[0], arr[1:])


class ActivityRouter:

    def __init__(self) -> None:
        self.handler: dict[str, dict[str, DrawerHandler]] = defaultdict(dict)

    def register(self, view_ids: list[str], action_id: str):
        def decorator(func):
            for view_id in view_ids:
                self.handler[view_id][action_id] = func
            return func

        return decorator

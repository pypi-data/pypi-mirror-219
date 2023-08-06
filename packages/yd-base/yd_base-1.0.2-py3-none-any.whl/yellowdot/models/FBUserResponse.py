from dataclasses import dataclass


@dataclass(init=True, repr=True, eq=True, unsafe_hash=True, frozen=True)
class FBUsersResponse:
    users: list = None
    next_page_token: str = None
    has_next_page: bool = False
    page_index: str = 0
    page_size: int = 0

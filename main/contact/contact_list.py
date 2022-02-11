from typing import TypeVar, Generic


from .contact import Contact


C = TypeVar("C", bound=Contact)


class ContactList(Generic[C]):
    

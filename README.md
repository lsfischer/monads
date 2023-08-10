# Monads

Basic monad helper classes to help you write more strongly typed python

## Example usage
```python
from monads import Result
from enum import Enum
from dataclasses import dataclass

@dataclass
class User:
    user_id: str
    name: str
    
    
class UserFailureReason(Enum):
    USER_NOT_FOUND = "user_not_found"
    

def get_user(user_id: str) -> Result[User, UserFailureReason]:
    """ Retrieve the user from the DB given its ID """
    db_result = {"user_id": "1", "name": "John Doe"}
    
    if not db_result:
        return Result.error(UserFailureReason.USER_NOT_FOUND)
    
    user = User(db_result["user_id"], db_result["name"])
    return Result.ok(user)


get_user(user_id="1").map(lambda x: x.name).or_else_throw()
# Output: John Doe
```

However if the user was not present in our DB then 
```python
get_user(user_id="1").map(lambda x: x.name).or_else_throw()
# Output: NotImplementedError: No success value present, but contains an error instead: UserFailureReason.USER_NOT_FOUND
```

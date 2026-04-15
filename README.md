#  FastAPI

# Tools

- ruff
- uv
- fastapi
  
## Other

- [https://mockaroo.com/](https://mockaroo.com/)
- [https://chocolatey.org/](https://chocolatey.org/)

## Commands
- install uv: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- init project: `uv init  projectname`
- add fastapi: `uv add "fastapi[standard]"`
- run app: `uv run fastapi dev main.py`

## Types

### Alap típusok
- int
- float
- str
- bool
- list: `list[str]`
- tuple: `tuple[int, int, int]`
- dict: `dict[str, float]`
- set:  `set[bytes]`

### Egyéb típusok
- UUID
- datetime.datetime
- datetime.date
- datetime.time
- datetime.timedelta
- frozenset
- bytes
- Decimal

### Különleges típusok

- union: `str | int`
- optional: `str | None = None`
- class: `Person` típus
```python
class Person:
  def __init__(self,  name: str):
    self.name = name

```
- Annotated
```python
from typing import Annotated

"""
-------
"""
def say_hi(name: Annotated["str", "this is just a metadata"]) -> str:
  return f"Hi {name}"
```

# CRUD
- Create
- Read
- Update
- Delete
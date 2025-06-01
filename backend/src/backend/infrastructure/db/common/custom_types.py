from typing import Annotated

from sqlalchemy.orm import mapped_column


AutoIntPK = Annotated[int, mapped_column(primary_key=True, autoincrement=True, unique=True)]

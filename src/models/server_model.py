from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class Server(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    server_id: int = Field(sa_column=Column(BigInteger, unique=True, nullable=False))
    greetings: bool = False
    greetings_message: str | None = None
    greetings_card: bool = False
    greetings_channel_id: int | None = Field(
        default=None, sa_column=Column(BigInteger, nullable=True)
    )
    chatbot: bool = False
    chatbot_channel_id: int | None = Field(
        default=None, sa_column=Column(BigInteger, nullable=True)
    )
    chatbot_response: str = "mentions"  # all | mentions | replies | both
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_At: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        nullable=False,
    )

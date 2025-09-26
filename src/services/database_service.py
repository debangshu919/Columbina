from sqlmodel import SQLModel, create_engine

from configs import env

engine = create_engine(env.DATABASE_URL, echo=True)  # turn off echo in prod.

SQLModel.metadata.create_all(engine)

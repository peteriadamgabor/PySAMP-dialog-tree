from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

con_str = "postgresql+psycopg2://postgres:admin@localhost:5432/fayrpg"
options = {}  # {'options': '-csearch_path=fayrpg'}

LOADER_ENGINE = create_engine(con_str, connect_args=options, echo=False)
MAIN_ENGINE = create_engine(con_str, connect_args=options, echo=False)
PLAYER_ENGINE = create_engine(con_str, connect_args=options, echo=False)
HOUSE_ENGINE = create_engine(con_str, connect_args=options, echo=False)
ITEM_ENGINE = create_engine(con_str, connect_args=options, echo=False)
UTIL_ENGINE = create_engine(con_str, connect_args=options, echo=False)
VEHICLE_ENGINE = create_engine(con_str, connect_args=options, echo=False)

LOADER_SESSION = sessionmaker(LOADER_ENGINE)
MAIN_SESSION = sessionmaker(MAIN_ENGINE)
PLAYER_SESSION = sessionmaker(PLAYER_ENGINE)
HOUSE_SESSION = sessionmaker(HOUSE_ENGINE)
ITEM_SESSION = sessionmaker(ITEM_ENGINE)
UTIL_SESSION = sessionmaker(UTIL_ENGINE)
VEHICLE_SESSION = sessionmaker(VEHICLE_ENGINE)

from sqlalchemy import create_engine

con_str = "postgresql+psycopg2://postgres:admin@localhost:5432/fayrpg"
options = {'options': '-csearch_path=fayrpg'}

MAIN_ENGINE = create_engine(con_str, connect_args=options, echo=False)

PLAYER_ENGINE = create_engine(con_str,  connect_args=options, echo=False)

HOUSE_ENGINE = create_engine(con_str,  connect_args=options, echo=False)

ITEM_ENGINE = create_engine(con_str,  connect_args=options, echo=False)

UTIL_ENGINE = create_engine(con_str, connect_args=options, echo=False)

VEHICLE_ENGINE = create_engine(con_str, connect_args=options, echo=False)

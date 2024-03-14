from datetime import datetime
from typing import List, Set

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import DeclarativeBase, relationship

from python.server.database import LOADER_ENGINE


class Base(DeclarativeBase):
    pass


fraction_skins = Table(
    'fraction_skins',
    Base.metadata,
    Column('fraction_id', Integer, ForeignKey('fractions.id')),
    Column('skin_id', Integer, ForeignKey('skins.id'))
)


vehicle_model_fuels = Table(
    'vehicle_model_fuels',
    Base.metadata,
    Column('vehicle_model_id', Integer, ForeignKey('vehicle_models.id')),
    Column('fuel_type_id', Integer, ForeignKey('fuel_types.id'))
)


class Skin(Base):
    __tablename__ = 'skins'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    description: str = Column(String)
    price: int = Column(Integer)
    sex: bool = Column(Boolean)
    dl_id: int = Column(Integer)


class PermissionType(Base):
    __tablename__ = 'permission_types'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    code: str = Column(String)
    description: str = Column(String)


class CommandPermission(Base):
    __tablename__ = 'command_permissions'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    cmd_txt: str = Column(String)
    permission_type_id: int = Column(ForeignKey("permission_types.id"))
    permission_type: "PermissionType" = relationship("PermissionType")
    need_power: int = Column(Integer)


class RolePermission(Base):
    __tablename__ = 'role_permissions'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    role_id: int = Column(ForeignKey("roles.id"))
    permission_type_id: int = Column(ForeignKey("permission_types.id"))
    permission_type: "PermissionType" = relationship("PermissionType")
    power: int = Column(Integer)


class Role(Base):
    __tablename__ = 'roles'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    permissions: "RolePermission" = relationship("RolePermission", primaryjoin="Role.id == RolePermission.role_id")


class DutyLocation(Base):
    __tablename__ = 'fraction_duty_locations'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    fraction_id: int = Column(ForeignKey("fractions.id"))
    x: float = Column(Integer)
    y: float = Column(Integer)
    z: float = Column(Integer)
    size: float = Column(Integer)
    interior: int = Column(Integer)
    virtual_word: int = Column(Integer)
    in_game_id: int = Column(Integer)


class Fraction(Base):
    __tablename__ = 'fractions'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    acronym: str = Column(String)
    duty_everywhere: int = Column(Integer)
    skins: Set["Skin"] = relationship('Skin', secondary=fraction_skins)
    duty_points: Set["DutyLocation"] = relationship()


class PlayerParameter(Base):
    __tablename__ = 'player_parameters'
    __allow_unmapped__ = True

    player_id: int = Column(ForeignKey("players.id"), primary_key=True)
    fraction_skin_id: int = Column(ForeignKey("skins.id"))
    fraction_skin: "Skin" = relationship("Skin")


class ItemData(Base):
    __tablename__ = 'item_data'

    item_id = Column(ForeignKey("items.id"), primary_key=True)
    weapon_id: int = Column(Integer)
    type: int = Column(Integer)
    heal: int = Column(Integer)


class Item(Base):
    __tablename__ = 'items'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    max_amount: int = Column(Integer)
    min_price: int = Column(Integer)
    max_price: int = Column(Integer)
    volume: int = Column(Integer)
    sellable: bool = Column(Boolean)
    droppable: bool = Column(Boolean)
    is_stackable: bool = Column(String)
    data: "ItemData" = relationship("ItemData")


class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    item_id: int = Column(ForeignKey("items.id"))
    item: "Item" = relationship("Item")


class PlayerInventoryItem(Base):
    __tablename__ = 'player_inventor_items'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    player_id: int = Column(ForeignKey("players.id"))
    inventory_item_id: int = Column(ForeignKey("inventory_items.id"))
    inventory_item: InventoryItem = relationship()
    amount: int = Column(Integer)
    worn: bool = Column(Boolean)
    dead: bool = Column(Boolean)
    in_backpack: bool = Column(Boolean)


class PlayerModel(Base):
    __tablename__ = 'players'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    in_game_id: int = Column(Integer)
    name: str = Column(String)
    password: str = Column(String)
    money: float = Column(Float)
    skin_id: int = Column(ForeignKey("skins.id"))
    skin: "Skin" = relationship("Skin")
    sex: int = Column(Integer)
    played_time: int = Column("playedtime", Integer)
    birthdate: datetime.date = Column(Date)
    role_id: int = Column(ForeignKey("roles.id"))
    role: "Role" = relationship("Role")
    parameter: "PlayerParameter" = relationship()
    fraction_id: int = Column(ForeignKey("fractions.id"))
    fraction: "Fraction" = relationship()
    items: List["PlayerInventoryItem"] = relationship("PlayerInventoryItem")


class HouseType(Base):
    __tablename__ = 'house_types'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    enter_x: float = Column(Float)
    enter_y: float = Column(Float)
    enter_z: float = Column(Float)
    angle: float = Column(Float)
    interior: int = Column(Integer)
    description: str = Column(String)
    price: int = Column(Integer)


class HouseModel(Base):
    __tablename__ = 'houses'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    entry_x: float = Column(Float)
    entry_y: float = Column(Float)
    entry_z: float = Column(Float)
    angle: float = Column(Float)
    type: int = Column(Integer)
    locked: bool = Column(Boolean)
    price: int = Column(Integer)
    rent_date: datetime = Column(DateTime)
    owner_id: int = Column(ForeignKey("players.id"))
    owner: "PlayerModel" = relationship("PlayerModel")
    house_type_id: int = Column(ForeignKey("house_types.id"))
    house_type: "HouseType" = relationship("HouseType")


class FuelType(Base):
    __tablename__ = 'fuel_types'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    code: str = Column(String)


class VehicleModel(Base):
    __tablename__ = 'vehicle_models'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    real_name: str = Column(String)
    seats: int = Column(Integer)
    price: int = Column(Integer)
    trunk_capacity: int = Column(Integer)
    color_number: int = Column(Integer)
    tank_capacity: int = Column(Integer)
    consumption: int = Column(Integer)
    max_speed: int = Column(Integer)
    hood: bool = Column(Boolean)
    airbag: bool = Column(Boolean)
    allowed_fuel_types: List["FuelType"] = relationship('FuelType', secondary=vehicle_model_fuels)


class VehicleData(Base):
    __tablename__ = 'vehicles'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    in_game_id: int = Column(Integer)
    model_id: int = Column(Integer, ForeignKey("vehicle_models.id"))
    model: "VehicleModel" = relationship("VehicleModel")
    x: float = Column(Float)
    y: float = Column(Float)
    z: float = Column(Float)
    angle: float = Column(Float)
    color_1: int = Column(Integer)
    color_2: int = Column(Integer)
    fuel_type_id: int = Column(ForeignKey("fuel_types.id"))
    fuel_type: "FuelType" = relationship("FuelType", foreign_keys=[fuel_type_id])
    fill_type_id: int = Column(ForeignKey("fuel_types.id"))
    fill_type: "FuelType" = relationship("FuelType", foreign_keys=[fill_type_id])
    fuel_level: float = Column(Float)
    locked: bool = Column(Boolean)
    health: float = Column(Float)
    plate: str = Column(String)
    panels_damage: int = Column(Integer)
    doors_damage: int = Column(Integer)
    lights_damage: int = Column(Integer)
    tires_damage: int = Column(Integer)


class Teleport(Base):
    __tablename__ = 'teleports'

    id: int = Column(Integer, primary_key=True)
    from_x: float = Column(Float)
    from_y: float = Column(Float)
    from_z: float = Column(Float)
    from_interior: int = Column(Integer)
    from_vw: int = Column(Integer)
    radius: float = Column(Float)
    to_x: float = Column(Float)
    to_y: float = Column(Float)
    to_z: float = Column(Float)
    to_angel: float = Column(Float)
    to_interior: int = Column(Integer)
    to_vw: int = Column(Integer)
    description: str = Column(String)
    in_game_id: int = Column(Integer)


class InteriorModel(Base):
    __tablename__ = 'interiors'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    x: float = Column(Float)
    y: float = Column(Float)
    z: float = Column(Float)
    a: float = Column(Float)
    interior: int = Column(Integer)
    in_game_id: int = Column(Integer)


class BusinessType(Base):
    __tablename__ = 'business_types'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    code: str = Column(String)


class BusinessModel(Base):
    __tablename__ = 'business'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    in_game_id: int = Column(Integer)
    business_type_id: int = Column(Integer, ForeignKey("business_types.id"))
    business_type: "BusinessType" = relationship("BusinessType")
    interior_id: int = Column(Integer, ForeignKey("interiors.id"))
    interior: "InteriorModel" = relationship("InteriorModel")
    name: str = Column(String)
    x: float = Column(Float)
    y: float = Column(Float)
    z: float = Column(Float)
    a: float = Column(Float)
    locked: bool = Column(Boolean)
    is_company: bool = Column(Boolean)
    company_chain: int = Column(Integer)


class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True)
    number: str = Column(String)
    password: str = Column(String)
    balance: float = Column(Float)
    owner_id: int = Column(ForeignKey("players.id"))
    owner: "PlayerModel" = relationship("PlayerModel")
    business_id: int = Column(ForeignKey("business.id"))
    business: "BusinessModel" = relationship("BusinessModel")
    fraction_id: int = Column(ForeignKey("fractions.id"))
    fraction: "Fraction" = relationship("Fraction")
    is_default: bool = Column(Boolean)


Base.metadata.create_all(bind=LOADER_ENGINE, checkfirst=True)

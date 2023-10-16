from enum import Enum


class VehicleType(Enum):
    CAR, TRUCK, HANDICAPPED, VAN, MOTORBIKE = 1, 2, 3, 4, 5


class ParkingSpotType(Enum):
    HANDICAPPED, COMPACT, LARGE, MOTORBIKE = 1, 2, 3, 4


class ParkingTicketStatus(Enum):
    ACTIVE, PAID, BLOCKED = 1, 2, 3


class AccountStatus(Enum):
    ADMIN, ACTIVE, BLOCKED, SUBSCRIBED = 1, 2, 3, 4


LARGE_COUNT = 10
COMPACT_COUNT = 10
MOTORBIKE_COUNT = 10
HANDICAPPED_COUNT = 10

CAR_PARKING_RATE = {
    1: 2000,
    2: 1500,
    3: 1000,
}

VAN_PARKING_RATE = {
    1: 2500,
    2: 1800,
    3: 1500,
}

MOTORBIKE_PARKING_RATE = {
    1: 2000,
    2: 1500,
    3: 1000,
}

HANDICAPPED_PARKING_RATE = {
    1: 1500,
    2: 1000,
    3: 500,
}

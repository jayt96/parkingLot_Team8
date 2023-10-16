import time

import enums
from enums import VehicleType, AccountStatus
from datetime import datetime


class ParkingLot:
    def __init__(self, name):
        self.name = name
        self.compact_spot_count = 0
        self.large_spot_count = 0
        self.motorbike_spot_count = 0
        self.handicapped_spot_count = 0
        self.parking_floors = []
        self.max_compact_count = enums.COMPACT_COUNT
        self.max_large_count = enums.LARGE_COUNT
        self.max_motorbike_count = enums.MOTORBIKE_COUNT
        self.max_handicapped_count = enums.HANDICAPPED_COUNT
        self.cnt = 0
        self.floor_count = 0

        self.active_tickets = {}
        self.parking_history = {}

    def update_max_capacity(self):
        self.max_compact_count = enums.COMPACT_COUNT * self.floor_count
        self.max_large_count = enums.LARGE_COUNT * self.floor_count
        self.max_motorbike_count = enums.MOTORBIKE_COUNT * self.floor_count

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_new_parking_ticket(self, vehicle, account_type):
        current_time = time.time()
        current_date = datetime.fromtimestamp(current_time).strftime('%Y%m%d')
        self.cnt += 1

        ticket = int(current_date) * 1000 + self.cnt

        if self.is_full(vehicle.get_type()):
            return 'Parking full!'

        if account_type == AccountStatus.SUBSCRIBED:
            ticket = self.cnt
        else:
            ticket = int(current_date) * 1000 + self.cnt

        vehicle.assign_ticket(ticket)
        self._increment_spot_count(vehicle.get_type())
        self.active_tickets[ticket] = vehicle
        self.parking_history[ticket] = vehicle
        return ticket

    def is_full(self, vehicle_type):
        if vehicle_type == VehicleType.TRUCK or vehicle_type == VehicleType.VAN:
            return self.large_spot_count >= self.max_large_count

        if vehicle_type == VehicleType.MOTORBIKE:
            return self.motorbike_spot_count >= self.max_motorbike_count

        if vehicle_type == VehicleType.CAR:
            return (self.compact_spot_count + self.large_spot_count) >= (
                    self.max_compact_count + self.max_large_count)

        if vehicle_type == VehicleType.HANDICAPPED:
            return self.handicapped_spot_count >= self.max_handicapped_count

    def _increment_spot_count(self, vehicle_type):
        if vehicle_type == VehicleType.TRUCK or vehicle_type == VehicleType.VAN:
            self.large_spot_count += 1
        elif vehicle_type == VehicleType.MOTORBIKE:
            self.motorbike_spot_count += 1
        elif vehicle_type == VehicleType.CAR:
            if self.compact_spot_count < self.max_compact_count:
                self.compact_spot_count += 1
            else:
                self.large_spot_count += 1
        elif vehicle_type == VehicleType.HANDICAPPED:
            self.handicapped_spot_count += 1

    def _decrement_spot_count(self, vehicle_type):
        if vehicle_type == VehicleType.TRUCK or vehicle_type == VehicleType.VAN:
            self.large_spot_count -= 1
        elif vehicle_type == VehicleType.MOTORBIKE:
            self.motorbike_spot_count -= 1
        elif vehicle_type == VehicleType.CAR:
            self.large_spot_count -= 1
        elif vehicle_type == VehicleType.HANDICAPPED:
            self.handicapped_spot_count -= 1

    def leave_parking(self, ticket_number):
        if ticket_number in self.active_tickets:
            vehicle = self.active_tickets[ticket_number]
            self._decrement_spot_count(vehicle.get_type())
            parking_charge = vehicle.parking_charge()
            if int(vehicle.ticket) < 1000:
                parking_charge *= 0.75
            vehicle.update_parking_status(parking_charge)
            self.parking_history[ticket_number] = vehicle
            self.active_tickets.pop(vehicle.ticket, None)
            return vehicle.vehicle_number, parking_charge
        return 'Invalid ticket number.', None

    def vehicle_status(self, ticket_number):
        if ticket_number in self.parking_history:
            vehicle = self.parking_history[ticket_number]
            vehicle_details = {
                "Vehicle Number": vehicle.vehicle_number,
                "Vehicle Type": vehicle.vehicle_type.name,
                "Vehicle parking spot type": vehicle.parking_spot_type.name,
                "Vehicle parking time": vehicle.parking_time.strftime("%d-%m-%Y, %H:%M:%S"),
                "Vehicle parking charges": vehicle.parking_cost,
                "vehicle ticket status": vehicle.ticket_status.name,
            }
            return vehicle_details
        return 'Invalid ticket number.'

    def get_empty_spot_number(self):
        message = ""
        if self.max_compact_count - self.compact_spot_count > 0:
            message += f"Free Compact: {self.max_compact_count - self.compact_spot_count}"
        else:
            message += "Compact is full"
        message += "\n"

        if self.max_large_count - self.large_spot_count > 0:
            message += f"Free Large: {self.max_large_count - self.large_spot_count}"
        else:
            message += "Large is full"
        message += "\n"

        if self.max_motorbike_count - self.motorbike_spot_count > 0:
            message += f"Free Motorbike: {self.max_motorbike_count - self.motorbike_spot_count}"
        else:
            message += "Motorbike is full"
        message += "\n"

        if self.max_handicapped_count - self.handicapped_spot_count > 0:
            message += f"Free Handicapped: {self.max_handicapped_count - self.handicapped_spot_count}"
        else:
            message += "Handicapped is full"
        message += "\n"

        return message

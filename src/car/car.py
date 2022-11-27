from src.car.acceleration import Acceleration


class Car:
    def __init__(self, registration):
        self.registration = registration  # Each car has a unique registration/ID
        self.line = 0
        self.column = 0
        self.position_variables = [{"velocity": 0, "acceleration": Acceleration.CONSTANT},  # Line position
                                   {"velocity": 0, "acceleration": Acceleration.CONSTANT}]  # Column position

    def get_registration(self):
        return self.registration

    def get_line(self):
        return self.line

    def get_column(self):
        return self.column

    def get_position_variables(self):
        return self.position_variables

    def set_line(self, line_pos):
        self.line = line_pos

    def set_column(self, column_pos):
        self.column = column_pos

    def set_velocity(self, acceleration):
        # 0: Line & 1: Column
        if acceleration not in [a.value for a in Acceleration]:
            return
        # v1(j + 1) = v1(j) + a1
        self.position_variables[0]["velocity"] += acceleration
        self.position_variables[1]["velocity"] += acceleration

        self.position_variables[0]["acceleration"] = acceleration
        self.position_variables[1]["acceleration"] = acceleration

    def __eq__(self, car):
        return self.registration == car.registration

    def __hash__(self):
        return hash(self.registration)

    def __str__(self) -> str:
        return f"Car {self.registration}: ({self.line},{self.column}) -> {self.position_variables}"

from src.car.Acceleration import Acceleration


class Car:
    def __init__(self, registration, line_position, column_position):
        self.registration = registration  # Each car has a unique registration/ID
        self.line_position = line_position
        self.column_position = column_position
        self.position_variables = [{"velocity": 0, "acceleration": Acceleration.CONSTANT},
                                   {"velocity": 0, "acceleration": Acceleration.CONSTANT}]

    def get_registration(self):
        return self.registration

    def get_line_position(self):
        return self.line_position

    def get_column_position(self):
        return self.column_position

    def get_position_variables(self):
        return self.position_variables

    def set_line_position(self, line_pos):
        self.line_position = line_pos

    def set_column_position(self, column_pos):
        self.column_position = column_pos

    def set_position_velocity(self, position, velocity):
        # 0: Line & 1: Column
        if position != 0 or position != 1:
            return
        if velocity < 0:
            return
        self.position_variables[position]["velocity"] = velocity

    def set_position_acceleration(self, position, acceleration):
        # 0: Line & 1: Column
        if position != 0 or position != 1:
            return
        if acceleration is None:
            return
        self.position_variables[position]["acceleration"] = acceleration

    def __eq__(self, car):
        return self.registration == car.registration

    def __hash__(self):
        return hash(self.registration)

    def __str__(self) -> str:
        return f"Car: {self.registration}, " \
               f"{self.line_position}, " \
               f"{self.column_position}," \
               f"{self.position_variables}"

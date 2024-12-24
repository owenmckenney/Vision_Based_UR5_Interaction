# PID controller class

class PID:
    def __init__(self, dt=0.1, kp=1.0, ki=0.1, kd=0.0):
        self.dt = dt
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.proportional = 0
        self.integral = 0
        self.derivative = 0
        self.previous_error = 0

    def control(self, error):
        self.proportional = self.kp * error
        self.integral += error * self.dt
        self.derivative = (error - self.previous_error) / self.dt
        self.previous_error = error

        return self.proportional + self.ki * self.integral + self.kd * self.derivative
    
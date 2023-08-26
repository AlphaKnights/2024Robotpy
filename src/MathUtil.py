# I made this class purely because the index searching on the Robotpy docs took too goddamn long

class MathUtil:
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))
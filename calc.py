import math

#  DEFINE COMPLIMENTARY CONSTANTS
COMPLIMENTARY_ALPHA = 0.98
COMPLIMENTARY_DT = 0.02
GYRO_ANGLE_DIVIDE = 131.


class Calc(object):
    def __init__(self):
        pass

    @staticmethod
    def get_y_rotation(x, y, z):
        radians = math.atan2((-1) * z, Calc.dist(y, x))
        return -math.degrees(radians)

    @staticmethod
    def get_z_rotation(x, y, z):
        radians = math.atan2(y, Calc.dist(x, z))
        return math.degrees(radians)

    @staticmethod
    def dist(a, b):
        return math.sqrt((a * a) + (b * b))

    @staticmethod
    def cosine_similarity(a, b):
        return sum([i * j for i, j in zip(a, b)]) / (
                math.sqrt(sum([i * i for i in a])) * math.sqrt(sum([i * i for i in b])))

    @staticmethod
    def euclidean_distance(a, b):
        return math.sqrt(sum([(i - j) * (i - j) for i, j in zip(a, b)]))

    @staticmethod
    def get_accel_vector(acc):
        return math.sqrt(acc['y'] * acc['y'] + acc['z'] * acc['z'])

    @staticmethod
    def get_complementary(acc, gyro, angle):
        gyro_data_z = -1 * gyro['z'] / GYRO_ANGLE_DIVIDE
        # gyro_data_y = gyro['y'] / GYRO_ANGLE_DIVIDE
        deg_x = Calc.get_z_rotation(acc['x'], acc['y'], acc['z'])
        # deg_y = get_y_rotation(acc['x'], acc['y'], acc['z'])
        dgy_z = gyro_data_z
        # dgy_y = gyro_data_y
        angle_x = (COMPLIMENTARY_ALPHA * (angle['x'] + (dgy_z * COMPLIMENTARY_DT))) + ((1 - COMPLIMENTARY_ALPHA) * deg_x)
        # angle_y = (COMPLIMENTARY_ALPHA * (angle_y + (dgy_y * COMPLIMENTARY_DT))) + ((1 - COMPLIMENTARY_ALPHA) * deg_y)
        return {"x": angle_x}
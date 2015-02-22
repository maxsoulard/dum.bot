
class Utils:

    @staticmethod
    def angletodutycycle(angle=None):
        # y = ax+b ou a=5/90 et b=2.5 (pour SG90, 50Hz)
        dutycycle = None
        if angle is not None:
            dutycycle = (5.0*angle)/90 + 2.5
        return dutycycle

    @staticmethod
    def dutycycletoangle(dutycycle=None):
        # x = (y-b)/a ou a=5/90 et b=2.5 (pour SG90, 50Hz)
        angle = None
        if dutycycle is not None:
            angle = (dutycycle - 2.5) * (90/5)
        return angle

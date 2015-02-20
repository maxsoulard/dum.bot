
class Utils:

    @staticmethod
    def angletodutycycle(angle=None):
        dutycycle = None
        if angle is not None:
            dutycycle = (5.0*angle)/90 + 2.5
        return dutycycle

    @staticmethod
    def dutycycletoangle(dutycycle=None):
        angle = None
        if dutycycle is not None:
            angle = (dutycycle - 2.5) * (90/5)
        return angle
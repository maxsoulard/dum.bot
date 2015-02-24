
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

	# Conversions dec - bin
	@staticmethod
    def convertdecbin(param=0):
        if not isinstance(param, int):
            return None
        resultdivision = param
        result = []
        while resultdivision >= 1:
            if param != -1:
                reste = resultdivision % 2
                result.append(str(reste))
                resultdivision /= 2
        result.append(str(resultdivision))
        result.reverse()
        return ''.join(result)

    @staticmethod
    def convertbindec(param=''):
        decimal = 0
        index = len(param)-1
        for c in param:
            if c == '1':
                result = math.pow(2, index)
                decimal += result
            elif c != '0':
                decimal = None
                break
            index -= 1

        return decimal

    @staticmethod
    def manchesterdecode(param=''):
        result = []
        cc = []
        for c in param:
            cc.append(c)
            if len(cc) == 2:
                if cc[0] == '0' and cc[1] == '1':
                    result.append('0')
                elif cc[0] == '1' and cc[1] == '0':
                    result.append('1')
                else:
                    result = None
                    break
                cc = []
        return ''.join(result)

    @staticmethod
    def manchesterencode(param=''):
        result = []
        for c in param:
            if c == '0':
                result.append("01")
            elif c == '1':
                result.append("10")
            else:
                result = None
                break
        return ''.join(result)
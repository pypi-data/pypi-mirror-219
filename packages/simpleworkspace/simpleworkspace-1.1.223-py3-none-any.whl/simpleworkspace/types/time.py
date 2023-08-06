from enum import Enum as _Enum
from .iunit import IUnit as _IUnit

class TimeEnum(_Enum):
    '''relative to seconds'''
    NanoSecond  = 0.000000001
    MicroSecond = 0.000001 
    MilliSecond = 0.001
    Second = 1
    Minute = 60
    Hour = Minute * 60
    Day = 24 * Hour


class TimeUnit(_IUnit[TimeEnum, 'TimeUnit']):
    _TypeEnum = TimeEnum

    def GetParts(self, minPart:TimeEnum=None, maxPart:TimeEnum=None) -> dict[TimeEnum, float]:
        """Splits the current amount of relative time to individual parts

        :param minPart: The smallest part that should be included in the resulting dict. \
            if there are smaller parts available than minPart, they will be added as decimals to minPart 
        :param maxPart:  The highest part that should be included in the resulting dict. \
            If there are bigger parts available than maxPart, they will be added as the maxPart unit instead.
            This implies that when maxPart is specified to say hours, in the case \
            that there is 1 complete day, it will instead be added to hours as 24
        :return: dictionary of all used enums as keys, and their corresponding amount as values

        Example Usage:

        >>> TimeUnit(2.5, TimeEnum.Minute).GetParts()
        {
            TimeEnum.MilliSeconds: 0.0,
            TimeEnum.Seconds: 30.0,
            TimeEnum.Minute: 2.0,
            TimeEnum.Hour: 0.0,
            TimeEnum.Day: 0.0,
        }
        >>> TimeUnit(1, TimeEnum.Day).GetParts(maxPart=TimeEnum.Hour)
        {
            TimeEnum.MilliSeconds: 0.0,
            TimeEnum.Seconds: 0.0,
            TimeEnum.Minute: 0.0,
            TimeEnum.Hour: 24.0,
        }
        >>> TimeUnit(3601.1, TimeEnum.Second).GetParts(minPart=TimeEnum.Second, maxPart=TimeEnum.Minute)
        {
            TimeEnum.Seconds: 1.1,
            TimeEnum.Minute: 60.0,
        }

        """
        parts = {}
        remaining = self.amount * self.unit.value

        # sort by size and reverse it to get biggest parts to smallest
        reversed_enum = sorted(TimeEnum, key=lambda x: x.value, reverse=True)
        for enumUnit in reversed_enum:
            if maxPart and (enumUnit.value > maxPart.value):
                continue
            if enumUnit.value <= remaining:
                part = remaining // enumUnit.value
                parts[enumUnit] = part
                remaining %= enumUnit.value
            else:
                parts[enumUnit] = 0.0
            
            if minPart and (minPart == enumUnit):
                break
        
        #gather the leftovers to the smallest part if any
        if(remaining > 0):
            #use last timeunit in loop since that will be the smallest part
            parts[enumUnit] = parts[enumUnit] + remaining / enumUnit.value
        return parts


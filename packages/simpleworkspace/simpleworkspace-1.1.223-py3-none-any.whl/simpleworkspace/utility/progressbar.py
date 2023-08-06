from time import time
import sys
from ..types import TimeEnum, TimeUnit
import threading

class ProgressBar:
    '''thread safe progressbar'''
    def __init__(self, iterable=None, total=None):
        self.setting_style_fill = '█'
        '''the character to fill the progressbar with'''
        self.setting_style_barLength = 20
        '''total width in characters of the progressbar'''
        self.setting_style_infinityFormat = "Progress: {incremented} {unit} [elapsed={elapsedTime}, speed={speed:.1f}/s]"
        '''the style used for when the progressbar does not have a known total, since alot of statistics can not be calculated in this scenario'''
        self.setting_style_format = "Progress: |{bar}| {percentage:.1f}% [elapsed={elapsedTime}|remaining={remainingTime}|speed={speed:.1f}/s|{unit}={incremented}/{total}]"
        '''the style used for when the progressbar has a known total'''
        self.setting_style_unit = "pcs"
        '''states what one increment is, such as 1 piece or 1 byte etc'''
        self.setting_autoPrint=True
        '''print progressbar on every increment call'''
  
        if(total is None and iterable is not None):
            if hasattr(iterable, "__len__"):
                total = len(iterable)
        
        self.total = total
        self._iterable = iterable
        if(self._iterable is not None):
            self._iterator = iter(iterable)
        self.stats_incremented = 0
        '''the total incremented amount'''
        self._stats_startTime = time()  # Track start time
        self._stats_previousIncrementCount = 0
        self._stats_previousIncrementTime = self._stats_startTime # Track previous time for increment

        self._lock = threading.Lock()
        self._thread_PrintAsync = None
        self._thread_PrintAsync_stopEvent = threading.Event()


    def IsFinished(self):
        if(self.total is None):
            return False #without a total, its not possible to say its finished
        if(self.stats_incremented >= self.total):
            return True
        return False
    
    def Increment(self, increment=1):
        '''Increases the progress bar by the specified increment value'''
        with self._lock:
            self.stats_incremented += increment
            if(self.setting_autoPrint):
                self.Print()
        return

    def _PrintAsync(self, refreshDelay:float):
        #prints once right away, then at end of while loop after delay each time, since the delay can be aborted,
        #we want to make sure we get one last refresh
        self.Print()
        while(not self._thread_PrintAsync_stopEvent.is_set()):
            if(self.IsFinished()):
                break
            self._thread_PrintAsync_stopEvent.wait(refreshDelay)
            self.Print()
        self._thread_PrintAsync_stopEvent.clear()
        return

    def PrintAsync(self, refreshDelay=1):
        """
        Prints the progress bar live in a new thread with the refresh delay specified in settings

        disables autoprint on increment if its on, the live progress thread will take care
        of printing it with better statistics since increments are gathered over potentially a longer duration

        :param refreshDelay: how often to refresh bar stats and visuals, delay is specified in seconds
        """

        self.setting_autoPrint = False 

        self._thread_PrintAsync = threading.Thread(target=self._PrintAsync, args=[refreshDelay])
        self._thread_PrintAsync.start()
        return

    def PrintAsync_Stop(self):
        self._thread_PrintAsync_stopEvent.set()
    
    def PrintAsync_Wait(self):
        self._thread_PrintAsync.join()

    def Print(self):
        """Prints the progress bar to the console"""

        current_time = time()
        elapsedTime = current_time - self._stats_startTime
        elapsedTime_str = self._FormatTime(elapsedTime)
        elapsedTime_SinceLastIncrement = current_time - self._stats_previousIncrementTime
        incrementsSinceLastPrint = self.stats_incremented - self._stats_previousIncrementCount
        incrementsPerSecond = 0 if elapsedTime_SinceLastIncrement == 0 else (incrementsSinceLastPrint) / elapsedTime_SinceLastIncrement
        self._stats_previousIncrementTime = current_time
        self._stats_previousIncrementCount = self.stats_incremented

        sys.stdout.write("\r\x1b[2K") #backtrack the console line with \r, and clear the old text with rest of the sequence
        if(self.total is None):
            sys.stdout.write(self.setting_style_infinityFormat.format(
                incremented=self.stats_incremented,
                elapsedTime=elapsedTime_str,
                speed=incrementsPerSecond,
                unit=self.setting_style_unit
            ))
            return
        


        # Calculate remaining time
        remainingTime = 0 if incrementsPerSecond == 0 else (self.total - self.stats_incremented) / incrementsPerSecond
        remainingTime_str = self._FormatTime(remainingTime)

        #progressbar style
        filled_length = min(int(self.setting_style_barLength * self.stats_incremented / self.total), self.setting_style_barLength) #use min incase bar length is over 100%
        bar = self.setting_style_fill * filled_length + '-' * (self.setting_style_barLength - filled_length)
        percentage = self.stats_incremented * 100 / self.total


        sys.stdout.write(self.setting_style_format.format(
            bar=bar, percentage=percentage, elapsedTime=elapsedTime_str,
            remainingTime=remainingTime_str, speed=incrementsPerSecond, incremented=self.stats_incremented, 
            total=self.total, unit=self.setting_style_unit
        ))
        
        return

    def _FormatTime(self, seconds: float):
        """
        Formats the given time in seconds to the format HH:MM:SS.
        :param seconds: The time in seconds to format.
        """
        timeUnit = TimeUnit(seconds, TimeEnum.Second)
        timeParts = timeUnit.GetParts(minPart=TimeEnum.Second,maxPart=TimeEnum.Hour)
        for i in timeParts.keys():
            timeParts[i] = round(timeParts[i]) #remove all decimals
        return "{0:02d}:{1:02d}:{2:02d}".format( #00:00:00 format
            timeParts[TimeEnum.Hour], timeParts[TimeEnum.Minute], timeParts[TimeEnum.Second]
        )

    def __len__(self):
        return self.total
    
    def __iter__(self):
        return self

    def __next__(self):
        '''Returns the next value from the iterator and increments the progress bar'''

        try:
            value = next(self._iterator)
            self.Increment()
            return value
        except StopIteration:
            raise StopIteration
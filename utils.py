import time

class Log:
    def __init__(self):
        filename = "log" + "-" + time.strftime("%Y%m%d-%H%M") + ".log"
        self.log_file = open(filename, "w")

    def dlog(self, t):
        if self.log_file == None:
            return

        self.log_file.write(t + "\n")
        self.log_file.flush()
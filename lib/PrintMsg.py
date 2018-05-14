from datetime import datetime
class PrintMsg:
    @staticmethod
    def get_color(selectColor):
        color = {
            'HEADER': '\033[95m',
            'OKBLUE': '\033[94m',
            'OKGREEN': '\033[92m',
            'WARNING': '\033[93m',
            'FAIL': '\033[91m',
            'ENDC': '\033[0m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m'
        }

        return color[selectColor]
    
    @staticmethod
    def msg(msg, time = False, sameline = False):
        # Add hora
        addHour = ""
        if time:
            addHour = datetime.now().strftime('%Y-%m-%d %H:%M:%S - ')

        if sameline:
            print("%s%s" % (addHour, msg), end= "", flush=True)
        else:
            print("%s%s" % (addHour, msg))

    @staticmethod
    def error(msg, time = False, sameline = False):
        updateMsg = PrintMsg.get_color('FAIL') + msg + PrintMsg.get_color('ENDC')
        PrintMsg.msg(updateMsg, time = time, sameline = sameline)

    @staticmethod
    def ok(msg, time = False, sameline = False):
        updateMsg = PrintMsg.get_color('OKGREEN') + msg + PrintMsg.get_color('ENDC')
        #print(Fore.BLUE + "Hello World")
        
        
        PrintMsg.msg(updateMsg, time = time, sameline = sameline)
       
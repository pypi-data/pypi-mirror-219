import datetime, random

version = "1.0.5"

class color:
    blue = 0x0076FF
    lightblue = 0x5790A8
    green = 0x00FF00
    yellow = 0xFFFF00
    red = 0xFF0000
    black = 0x000001
    teal = 0x00ffff
    purple = 0xA020F0



class times:
    def utcnowtime():
        time = datetime.datetime.utcnow()
        return time
    def nowtime():
        time = datetime.datetime.now()
        return time
    

print()

class ids:
    def fourdashfour():
        ranid = ""
        def gettheid(string):
            for ta in range(4):
                string += random.choice(["a","b","c","d","e","f","g","h","i","k","l","m","n","o","q","r","s","t","v","x","y","z","1","2","3","4","5","6","7","8","9"])
            return string
        ranid = gettheid(ranid)
        ranid += "-"
        ranid = gettheid(ranid)
        return ranid
    def ranid(amount : int):
        ranid = ""
        def gettheid(string):
            for ta in range(amount):
                string += random.choice(["a","b","c","d","e","f","g","h","i","k","l","m","n","o","q","r","s","t","v","x","y","z","1","2","3","4","5","6","7","8","9"])
            return string
        ranid = gettheid(ranid)
        return ranid   
    

weekends = []

def check_weekend(day):
    print("Today is ", day.strftime("%A"))
    if(day.strftime("%A") == "Sunday" or day.strftime("%A") == "Saturday"):
       print("It is a weekend, no trading today!")
       weekends.append(day.date())
       return 1
    else:
        return 0

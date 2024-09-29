import datetime
mylist = []
today = datetime.date.today()
mylist.append(today)
print(mylist[0]) # print the date object, not the container ;-)

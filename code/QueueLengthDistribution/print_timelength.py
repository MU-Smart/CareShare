import datetime 

s_time = "21:15:00"
s_time = datetime.datetime.strptime(s_time,"%H:%M:%S")
l_d = []
for i in range(0,int(3*60/5)):
	s_time = s_time+datetime.timedelta(minutes=5)
	if(s_time > datetime.datetime.strptime("23:30:00","%H:%M:%S")):
		break
	l_d.append(s_time)



l_s = []
for i in l_d:
	l_s.append(datetime.datetime.strftime(i,"%H:%M:%S"))


print(min(l_s))
print(max(l_s))
print(len(l_s))

d = {}
for i in l_s:
	d[i] = 0

print(d)

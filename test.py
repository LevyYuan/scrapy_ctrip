list = []
for i in range(1,201):
	if  (i/10%10)==7 or i%10==7 or i%7==0:
		list.append(i)
print(list)
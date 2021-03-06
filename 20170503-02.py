from datetime import date, timedelta
import datetime

def f(d1, d2):
	delta = d2 - d1
	return set([d1 + timedelta(days=i) for i in range(delta.days + 1)])

def Date_Overlap(range1, range2):
	#判斷兩日期區間，做set_itsec
	set_itsec = f(*range1) & f(*range2)

	ls_date = []
	if set_itsec:
		print("2區間2:" + str(min(set_itsec)) + "~" + str(max(set_itsec)) + "\n")
		dt1 = min(set_itsec).strftime('%Y%m%d') 
		dt2 = max(set_itsec).strftime('%Y%m%d') 
		ls_date.append([dt1, dt2])

		if min(set_itsec) != min(min(range1),min(range2)):
			print("2區間1:" + str(min(min(range1),min(range2))) + "~" + str(min(set_itsec) + timedelta(days=-1)) + "\n")
			dt1 = min(min(range1),min(range2)).strftime('%Y%m%d') 
			dt2 = (min(set_itsec) + timedelta(days=-1)).strftime('%Y%m%d') 
			ls_date.append([dt1, dt2])


		if max(set_itsec) != max(max(range1),max(range2)):
			print("2區間3:" + str(max(set_itsec) + timedelta(days=1)) + "~" + str(max(max(range1),max(range2))) + "\n")
			dt1 = (max(set_itsec) + timedelta(days=1)).strftime('%Y%m%d') 
			dt2 = max(max(range1),max(range2)).strftime('%Y%m%d') 
			ls_date.append([dt1, dt2])

	else:
		print("1區間:" + str(range1) + "," + str(range2))
		dt1 = min(range1).strftime('%Y%m%d')
		dt2 = max(range1).strftime('%Y%m%d')
		ls_date.append([dt1, dt2])
		dt1 = min(range2).strftime('%Y%m%d')
		dt2 = max(range2).strftime('%Y%m%d')
		ls_date.append([dt1, dt2])
		
	return ls_date



xr_date_st = "20160705"
xr_date_ed = "20160710"
xd_date_st = "20160701"
xd_date_ed = "20160712"

dt1 = datetime.datetime.strptime(xr_date_st, '%Y%m%d').date()
dt2 = datetime.datetime.strptime(xr_date_ed, '%Y%m%d').date()
ls_xr_date = [dt1, dt2]

dt1 = datetime.datetime.strptime(xd_date_st, '%Y%m%d').date()
dt2 = datetime.datetime.strptime(xd_date_ed, '%Y%m%d').date()
ls_xd_date = [dt1, dt2]

#print(ls_xr_date)
#print(ls_xd_date)

ls_dt = Date_Overlap(ls_xr_date, ls_xd_date)
print(ls_dt)
print("End of prog.")
from datetime import date, timedelta
import datetime

def f(d1, d2):
	delta = d2 - d1
	return set([d1 + timedelta(days=i) for i in range(delta.days + 1)])

def Date_Overlap(range1, range2):
	#判斷兩日期區間，做set_itsec
	set_itsec = f(*range1[0:2]) & f(*range2[0:2])
	xr = range1[2]
	xd = range2[2]

	ls_date = []
	if set_itsec:
		dt1 = min(set_itsec).strftime('%Y%m%d') 
		dt2 = max(set_itsec).strftime('%Y%m%d') 
		ls_date.append([dt1, dt2, xr, xd])

		if min(set_itsec) != min(min(range1[0:2]),min(range2[0:2])):
			dt1 = min(min(range1[0:2]),min(range2[0:2])).strftime('%Y%m%d') 
			dt2 = (min(set_itsec) + timedelta(days=-1)).strftime('%Y%m%d') 
			if min(range1[0:2]) < min(range2[0:2]):
				ls_date.append([dt1, dt2, xr, 0])
			else:
				ls_date.append([dt1, dt2, 0, xd])


		if max(set_itsec) != max(max(range1[0:2]),max(range2[0:2])):
			dt1 = (max(set_itsec) + timedelta(days=1)).strftime('%Y%m%d') 
			dt2 = max(max(range1[0:2]),max(range2[0:2])).strftime('%Y%m%d') 

			if max(range1[0:2]) > max(range2[0:2]):
				ls_date.append([dt1, dt2, xr, 0])
			else:
				ls_date.append([dt1, dt2, 0, xd])

	else:
		dt1 = min(range1).strftime('%Y%m%d')
		dt2 = max(range1).strftime('%Y%m%d')
		ls_date.append([dt1, dt2, xr, 0])

		dt1 = min(range2).strftime('%Y%m%d')
		dt2 = max(range2).strftime('%Y%m%d')
		ls_date.append([dt1, dt2, xd, 0])

	return tuple(ls_date)
	


xr_date_st = "20160701"
xr_date_ed = "20160710"
xr = 1.1
xd_date_st = "20160705"
xd_date_ed = "20160712"
xd = 0.5

dt1 = datetime.datetime.strptime(xr_date_st, '%Y%m%d').date()
dt2 = datetime.datetime.strptime(xr_date_ed, '%Y%m%d').date()
ls_xr_date = [dt1, dt2, xr]

dt1 = datetime.datetime.strptime(xd_date_st, '%Y%m%d').date()
dt2 = datetime.datetime.strptime(xd_date_ed, '%Y%m%d').date()
ls_xd_date = [dt1, dt2, xd]

#print(ls_xr_date)
#print(ls_xd_date)

tp_dt = Date_Overlap(ls_xr_date, ls_xd_date)
print(tp_dt)
print("End of prog.")
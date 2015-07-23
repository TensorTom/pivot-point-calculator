import ystockquote
import re
from argparse import ArgumentParser
from datetime import date, timedelta
#10

def last_weekday(adate):
	adate -= timedelta(days=1)
	while adate.weekday() > 4:
		adate -= timedelta(days=1)
	return adate
	
def y_high(self):
	yesterday_high = newlist[2]
	yesterday_high_float = round(float(re.findall("\d+.\d{1,4}", yesterday_high)[0]), 3)
	return yesterday_high_float

def y_low(self):
	yesterday_low = newlist[3]
	yesterday_low_float = round(float(re.findall("\d+.\d{1,4}", yesterday_low)[0]),3)
	return yesterday_low_float

def y_open(self):
	yesterday_open = newlist[5]
	yesterday_open_float = round(float(re.findall("\d+.\d{1,4}", yesterday_open)[0]),3)
	return yesterday_open_float

def y_close(self):
	yesterday_close = newlist[4]
	yesterday_close_float = round(float(re.findall("\d+.\d{1,4}", yesterday_close)[0]),3)
	return yesterday_close_float

def floor_classic(a1, a2, a3, a4):
	pp = ((pivot_high + pivot_low + pivot_close) / 3)
	r1 = (2 * pp) - pivot_low
	r2 = (pp + pivot_high - pivot_low)
	r3 = (pivot_high + 2*(pp - pivot_low))
	s1 = (2*pp) - pivot_high
	s2 = pp - pivot_high + pivot_low
	s3 = pivot_low - 2*(pivot_high - pp)
	#return pp, r1, r2, r3, s1, s2, s3
	fc_values = [pp, r1, r2, r3, s1, s2, s3]
	return fc_values

def woodie_formula(a1, a2, a3, a4):
	pp = ((pivot_high + pivot_low + 2 * pivot_close)/4)
	r1 = (2*pp) - pivot_low
	r2 = (pp + pivot_high - pivot_low)
	s1 = (2 * pp) - pivot_high
	s2 = pp - pivot_high + pivot_low
	wf_values = [pp, r1, r2, s1, s2]
	return wf_values

mylastweekday = last_weekday(date.today())
stringdate = mylastweekday.strftime('%Y-%m-%d')

parser = ArgumentParser(description = 'Get Pivots for ticker from ystockquote')
parser.add_argument("-t", "--ticker", dest="ticker", help="ticker for lookup", metavar="FILE")
args = parser.parse_args()

ticker = args.ticker
historicalinfo = ystockquote.get_historical_prices(ticker, stringdate, stringdate)
string_historical_info = str(historicalinfo)
newlist = string_historical_info.split(',')

pivot_high = y_high(newlist)
pivot_low = y_low(newlist)
pivot_open = y_open(newlist)
pivot_close = y_close(newlist)

#print pivot_high, pivot_low, pivot_open, pivot_close


fc_values = floor_classic(pivot_high, pivot_low, pivot_open, pivot_close)
wf_values = woodie_formula(pivot_high, pivot_low, pivot_open, pivot_close)

k_pp = pivot_close
k_r3 = int(fc_values[3])
k_s3 = int(fc_values[6])
k_r2 = [int(fc_values[2]), int(wf_values[2])]
k_s2 = [int(fc_values[5]), int(wf_values[4])]
k_s1 = [int(fc_values[4]), int(wf_values[3])]
k_r1 = [int(fc_values[1]), int(wf_values[1])]

print "Kirk's Pivots for %s, using closing prices from %s" %(ticker, mylastweekday)
print "R3:", k_r3
print "R2:", k_r2
print "R1:", k_r1
print "Close:", k_pp
print "S1:", k_s1
print "S2:", k_s2
print "S3:", k_s3

print "Floor/Classic Pivots for %s, using closing prices from %s" %(ticker, mylastweekday)
print "R3:", fc_values[3]
print "R2:", fc_values[2]
print "R1:", fc_values[1]
print "Pivot Point:", fc_values[0]
print "S1:", fc_values[4]
print "S2:", fc_values[5]
print "S3:", fc_values[6]

print "Woodie's Formula Pivots for %s, using closing prices from %s" %(ticker, mylastweekday)
print "R2:", wf_values[2]
print "R1:", wf_values[1]
print "Pivot Point:", wf_values[0]
print "S1:", wf_values[3]
print "S2:", wf_values[4]

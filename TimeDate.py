from datetime import datetime, timedelta
dt='01CA36A7F8294CD8'
us=int(dt,16) / 10.
print datetime(1601,1,1) + timedelta(microseconds=us)

#!/usr/bin/python3
# Plot a question's views over time from database
# Usage: ./se.plot.py <log_name> <Url>

import sys
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_views(site, question, days=7):
	"Bin views into weekly increments"
	dates = []
	weekly_views = []

	with open(sys.argv[1], 'r') as f:
		for record, line in enumerate(f.readlines()):
			line = json.loads(line)
			date = line[0]
			if site in line[1] and question in line[1][site]:
				views = int(line[1][site][question])
				if not record:
					start_views = views
					start_date = date
				if date - start_date >= 86400 * (days - 0.5):
					dates.append(datetime.fromtimestamp((date)))
					weekly_views.append(views - start_views)
					start_views = views
					start_date = date

	if len(weekly_views) < 10:
		print((date - start_date) // 86400, 'days ungraphed')
	return dates, weekly_views


def main():
	url = sys.argv[2]
	site = url.split('/')[2].split('.')[0]
	question = url.split('/')[4]

	x, y = get_views(site, question)
	print(*list(zip(x, y)), sep='\n')
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=len(x)))
	plt.locator_params(axis='y', nbins=10)
	plt.plot(x, y)
	#plt.scatter(x, y, label= "stars", color= "green", s=30)
	plt.gcf().autofmt_xdate()

	plt.xlabel('Date')
	plt.ylabel('Views per week')
	plt.title(' '.join((site.title(), "Question", question)))
	plt.show()


if __name__ == "__main__":
	main()

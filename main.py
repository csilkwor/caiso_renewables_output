import sys
import re
import datetime
import requests

# Check command line argment usage
if len(sys.argv) > 3 or len(sys.argv) < 2:
    print("Usage: python main.py startDate(YYYY-MM-DD) [endDate(YY-MM-DD)]\n If no end date is supplied, the current date will be used.")
    exit()

url_pattern = "http://content.caiso.com/green/renewrpt/{date}_DailyRenewablesWatch.txt"

# Parse start/end dates from command line args
start_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
end_date = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date() if len(sys.argv) == 3 else datetime.date.today()

print("Start date: " + str(start_date))
print("End date: " + str(end_date))

renewable_resources_csv = "Date, Hour, GEOTHERMAL, BIOMASS, BIOGAS, SMALL HYDRO, WIND TOTAL, SOLAR PV, SOLAR THERMAL,\n"
total_production_csv = "Date, Hour, RENEWABLES, NUCLEAR, THERMAL, IMPORTS, HYDRO,\n"

# Open files for writing
renewable_resources_file = open("caiso_renewable_resources.csv", "w")
total_production_file = open("caiso_total_production.csv", "w")

# Iterate through the dates
d = start_date
delta = datetime.timedelta(days=1)
while d <= end_date:
    endpoint = url_pattern.format(date=d.strftime('%Y%m%d'))
    doc = requests.get(endpoint)
    if doc.status_code == 200:
        doc_text = doc.text
        doc_text = re.sub("\\t+", ", ", doc_text)
        doc_text = doc_text.splitlines()

        # Iterate through "Hourly Breakdown of Renewable Resources" table
        i = 2
        while i < 26:
            # Append each table row to csv
            renewable_resources_csv += str(d) + doc_text[i] + '\n'
            i = i + 1

        # Iterate through "Hourly Breakdown of Total Production by Resource Type" table
        i = 30
        while i < 54:
            # Append each table row to csv
            total_production_csv += str(d) + doc_text[i] + '\n'
            i = i + 1
    else:
        print("No data available for {date}".format(date=d.strftime('%Y-%m-%d')))

    d += delta

# Write csv output to files and close
renewable_resources_file.write(renewable_resources_csv)
total_production_file.write(total_production_csv)

renewable_resources_file.close()
total_production_file.close()

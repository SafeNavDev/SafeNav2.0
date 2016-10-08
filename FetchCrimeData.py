import requests
import math


class FetchCrimeData:
    def format_month(month):
        int_month = int(month)
        if int_month < 10:
            return '0' + str(int_month)
        else:
            return str(month)

    # NOTE: Requires location list formatted: ['longitude', 'latitude']
    def query_database(year_in, month_in, day_in, category_in, location):
        # This generates the category of crime
        category_param = 'category=' + category_in

        # This generates the date parameter
        month = FetchCrimeData.format_month(month_in)
        date = year_in + '-' + month + '-' + day_in + 'T12:00:00'
        prev_month = FetchCrimeData.format_month(int(month) - 2)
        prev_date = year_in + '-' + prev_month + '-' + day_in + 'T12:00:00'
        date_param = '&$where=incidentdate between ' + "'" + prev_date + "'" + ' and ' + "'" + date + "'"

        # This generates the radius in which we are searching
        location_param = '&$where=within_circle(location, ' + location[0] + ', ' + location[1] + ', 500)'
        print(location_param)

        # Finally, concatenate and pass http get request
        print('https://data.detroitmi.gov/resource/i9ph-uyrp.json?' + category_param
            + date_param + location_param)

data = FetchCrimeData.query_database('2016', '10', '08', 'ARSON', ['42.3417707', '-83.0601714'])
print(data.json())

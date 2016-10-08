import requests


class FetchCrimeData:
    static_base_url = "https://data.detroitmi.gov/resource/i9ph-uyrp.json?"
    static_category_param = ""
    static_date_param = ""

    # A custom initializer for efficiency when computing multiple lines along a path
    # Having certain data members stored is more efficient
    def __init__(self, year_in, month_in, day_in, category_in):
        month_in = FetchCrimeData.format_month(int(month_in))
        date = year_in + '-' + month_in + '-' + day_in + 'T12:00:00'
        prev_month = FetchCrimeData.format_month(int(month_in) - 2)
        prev_date = year_in + '-' + prev_month + '-' + day_in + 'T12:00:00'
        self.static_category_param = 'category=' + category_in
        self.static_date_param = '&$where= incidentdate between ' + "'" + prev_date + "'" + ' and ' + "'" + date + "'"


    def format_month(month):
        int_month = int(month)
        if int_month < 10:
            return '0' + str(int_month)
        else:
            return str(month)

    # NOTE: Requires location list formatted: ['longitude', 'latitude']
    def query_database(year_in, month_in, day_in, category_in, location, radius):
        incidents = []
        # This generates the category of crime
        category_param = 'category=' + category_in

        # This generates the date paadfsasdframeter
        month = FetchCrimeData.format_month(month_in)
        date = year_in + '-' + month + '-' + day_in + 'T12:00:00'
        prev_month = FetchCrimeData.format_month(int(month) - 2)
        prev_date = year_in + '-' + prev_month + '-' + day_in + 'T12:00:00'
        date_param = '&$where= incidentdate between ' + "'" + prev_date + "'" + ' and ' + "'" + date + "'"

        # This generates the radius in which we are searching
        location_param = 'and within_circle(location, ' + location[0] + ', ' + location[1] + ', ' + str(radius) + ')'

        # Finally, concatenate and pass http get request
        url = 'https://data.detroitmi.gov/resource/i9ph-uyrp.json?' + category_param + date_param + location_param
        local_data = requests.get(url).json()
        for x in local_data:
            incidents.append(x['location']['coordinates'])
        return incidents

    # Allows a more efficient query by not initializing local variables every time
    def static_query(self, location, radius):
        incidents = []
        location_param = 'and within_circle(location, ' + location[0] + ', ' + location[1] + ', ' + str(radius) + ')'
        url = self.static_base_url + self.static_category_param + self.static_date_param + location_param
        local_data = requests.get(url).json()
        for x in local_data:
            incidents.append(x['location']['coordinates'])
        return incidents

DataObject = FetchCrimeData('2016', '10', '08', 'ARSON')
data = DataObject.static_query(['42.3417707', '-83.0601714'], 3000)
print(data)

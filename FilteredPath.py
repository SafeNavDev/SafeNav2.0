# print(data.json().keys()) to find all keys in dict
import requests
import math

earth_radius = 3960.0
degrees_to_radians = math.pi / 180.0
radians_to_degrees = 180.0 / math.pi


class FilteredPath:
    def get_data(lat1, long1, lat2, long2):
        # generate a token with your client id and client secret
        # print(token.json()['access_token'])
        token = FilteredPath.gen_token()
        coordinates = long1 + "," + lat1 + "; " + long2 + "," + lat2

        data = requests.post('http://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?stops=' + coordinates, params={
            'f': 'json',
            'token': token.json()['access_token'],
            'studyAreas': '[{"geometry":{"x":-117.1956,"y":34.0572}}]'
        })
        return data.json()['routes']['features'][0]['geometry']['paths'][0]

    def gen_token():
        token = requests.post('https://www.arcgis.com/sharing/rest/oauth2/token/', params={
            'f': 'json',
            'client_id': 'OYBSyP4UMttEkIlp',
            'client_secret': '65057b2bafcf4e27bde6bcabff2dcc3c',
            'grant_type': 'client_credentials',
            'expiration': '1440'
        })
        return token

    def change_in_latitude(miles):
        # "Given a distance north, return the change in latitude."
        return (miles / earth_radius) * radians_to_degrees

    def change_in_longitude(latitude, miles):
        # Given a latitude and a distance west, return the change in longitude
        # Find the radius of a circle around the earth at given latitude.
        r = earth_radius * math.cos(latitude * degrees_to_radians)
        return (miles / r) * radians_to_degrees

    def filter_path_average(path):
        filtered_path = []
        long_diffs = []
        lat_diffs = []
        avg_delta_long = 0
        avg_delta_lat = 0
        sum1 = 0
        sum2 = 0

        for x in range(1, len(path)):
            long_diffs.append(abs(path[x][0] - path[x - 1][0]))
            lat_diffs.append(abs(path[x][1] - path[x - 1][1]))

        for x in long_diffs:
            sum1 += x
        avg_delta_long = sum1 / len(long_diffs)

        for x in lat_diffs:
            sum2 += x
        avg_delta_lat = sum2 / len(lat_diffs)

        for x in range(1, len(path)):
            if long_diffs[x - 1] < avg_delta_long and lat_diffs[x - 1] < avg_delta_lat:
                filtered_path.append(path[x])
        print(len(filtered_path))

    def filter_path_theory(path):
        delta_lat = FilteredPath.change_in_latitude(.025)
        delta_long = FilteredPath.change_in_longitude(42.3314, .025)
        filtered_path = []
        long_diffs = []
        lat_diffs = []

        for x in range(1, len(path)):
            long_diffs.append(abs(path[x][0] - path[x - 1][0]))
            lat_diffs.append(abs(path[x][1] - path[x - 1][1]))

        for x in range(1, len(path)):
            if long_diffs[x - 1] < delta_long and lat_diffs[x - 1] < delta_lat:
                filtered_path.append(path[x])
        print(len(filtered_path))

# First test on small Detroit route dataset
data1 = FilteredPath.get_data('42.3417707', '-83.0601714', '42.3387803', '-83.0572124')
print(len(data1))
data2 = FilteredPath.filter_path_average(data1)
data3 = FilteredPath.filter_path_theory(data1)

# Second test on large Detroit-Washington DC route dataset
data4 = FilteredPath.get_data('42.3417707', '-83.0601714', '9.9280694', '-84.0907246')
print(len(data4))
data5 = FilteredPath.filter_path_average(data4)
data6 = FilteredPath.filter_path_theory(data4)

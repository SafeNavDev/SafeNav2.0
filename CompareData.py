import requests
from FetchCrimeData import FetchCrimeData
from FilteredPath import FilteredPath

segment_length_miles = .15
segment_length_meters = 200

class CompareData:
    def return_conflicts(lat1_in, long1_in, lat2_in, long2_in, year_in, month_in, day_in):
        incidents_on_route = []
        data = FilteredPath.get_data(lat1_in, long1_in, lat2_in, long2_in)
        path = FilteredPath.filter_path_theory(data, segment_length_miles)
        CrossReferencer = FetchCrimeData(year_in, month_in, day_in)
        for x in path:
            print(x)
            CrossReferencer.static_query(incidents_on_route, x, segment_length_meters)
        return incidents_on_route

all_incidents = CompareData.return_conflicts('42.3418', '-83.0602', '42.3591', '-83.0665', '2015', '10', '08')
print(all_incidents)
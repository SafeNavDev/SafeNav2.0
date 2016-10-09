import requests
from FetchCrimeData import FetchCrimeData
from FilteredPath import FilteredPath

segment_length_miles = .1
segment_length_meters = 500

class CompareData:
    def return_conflicts(lat1_in, long1_in, lat2_in, long2_in, year_in, month_in, day_in, category_in):
        incidents_on_route = []
        data = FilteredPath.get_data(lat1_in, long1_in, lat2_in, long2_in)
        path = FilteredPath.filter_path_theory(data, segment_length_miles)
        CrossReferencer = FetchCrimeData(year_in, month_in, day_in, category_in)
        for x in path:
            print(x)
            incidents_on_route.append(CrossReferencer.static_query(x,segment_length_meters))
        print(incidents_on_route)
        return incidents_on_route

all_incidents = CompareData.return_conflicts('42.3417707', '-83.0601714', '42.377', '-83.2089', '2015', '10', '08', 'BURGLARY')
print(all_incidents)
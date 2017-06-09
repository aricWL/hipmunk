import grequests
import json
from flask import Blueprint, jsonify
from flask_restful import Api, Resource

hotels_blueprint = Blueprint(
  'hotels',
  __name__
)

hotels_api = Api(hotels_blueprint)

@hotels_api.resource('/search')
class SearchAPI(Resource):
    def get(self):

        merged = []
        urls = ['expedia', 'orbitz', 'priceline', 'travelocity', 'hilton']
        response_shells = [grequests.get('http://localhost:9000/scrapers/'+ u) for u in urls]
        responses = grequests.map(response_shells)
        results = [json.loads(response.content)['results'] for response in responses]

        while len(results) > 0:
            # Getting current min from each result
            current_mins = [result[-1]['ecstasy'] for result in results]
            # Getting the min of the current mins
            low_index = current_mins.index(min(current_mins))
            # Adding min to merged list
            merged.append(results[low_index][-1])
            # Removing the merged min
            results[low_index].pop()
            # If that results list is now empty, remove it
            if len(results[low_index]) == 0:
                results.pop(low_index)
                
        # The list will be in reverse because we used push()
        merged.reverse()

        return jsonify({'results': merged})

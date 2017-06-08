import requests
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
        results = [json.loads(requests.get('http://localhost:9000/scrapers/expedia').content)['results'],
                    json.loads(requests.get('http://localhost:9000/scrapers/orbitz').content)['results'],
                    json.loads(requests.get('http://localhost:9000/scrapers/priceline').content)['results'],
                    json.loads(requests.get('http://localhost:9000/scrapers/travelocity').content)['results'],
                    json.loads(requests.get('http://localhost:9000/scrapers/hilton').content)['results']]

        results = [result for result in results if len(result) > 0]
        from IPython import embed; embed()
        while len(results) > 0:
            lowest_ecstacies = [result[-1]['ecstasy'] for result in results]
            low_index = lowest_ecstacies.index(min(lowest_ecstacies))
            merged.append(results[low_index][-1])
            results[low_index].pop()
            if len(results[low_index]) == 0:
                results.pop(low_index)

        merged.reverse()

        return jsonify({'results': merged})

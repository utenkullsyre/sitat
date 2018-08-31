from flask import Blueprint
from flask_restful import Api
from resources.Test import Hello
from resources.Sitat import SitatResource
from resources.Humoer import HumoerResource
from resources.Barn import BarnResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/hello')
api.add_resource(SitatResource, '/sitat')
api.add_resource(HumoerResource, '/humoer')
api.add_resource(BarnResource, '/barn')

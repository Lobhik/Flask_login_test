from flask import Blueprint, request,g
from views.test.test_mh_city import MHCityListController

from views.test.test_user_view import CityListController


test_bp = Blueprint('test', __name__)


@test_bp.route("/city", methods=["GET"])
def city_list():
  limit = request.args.get("l", default=10)
  page  = int(request.args.get("p", default=1))
  ct = request.args.get("ct", default=None)
  ac = request.args.get("ac", default=0)
  pt = request.args.get("pt", default=0)


  return CityListController('all_dist', ct, int(ac), int(pt),limit,page)





@test_bp.route("/mh-city", methods=["GET"])
def mh_city_list():
  limit = request.args.get("l", default=10)
  page  = int(request.args.get("p", default=1))
  #ct = request.args.get("ct", default=0)

  return MHCityListController('MH_Districts',limit,page)





from flask import Blueprint, request,g
from views.user.city_list import CityListController

from views.user.user_view import  UserDetailsController

user_bp = Blueprint('user', __name__)



##
@user_bp.route("/city", methods=["GET"])
def city_list():
  limit = request.args.get("l", default=10)
  page  = int(request.args.get("p", default=1))
  ct = request.args.get("ct", default=0)
  ac = request.args.get("ac", default=0)
  pt = request.args.get("pt", default=0)

  # if ct == 0:
  #   return {"data":False, "respMessage":"Data not found", "pageNum":0}

  return CityListController('all_district_list', ct, int(ac), int(pt),limit,page)



##
@user_bp.route("/details", methods=["POST"])
def user_details():
  data = request.get_json()

  if data is None or len(data.keys()) == 0:
    return {"data":False, "respMessage":"Data not found", "pageNum":0}

  return UserDetailsController('user_details', data)



# ##
# @user_bp.route("/user-details", methods=["POST"])
# def user_details():
#   data = request.get_json()

#   if data is None or len(data.keys()) == 0:
#     return {"data":False, "respMessage":"Data not found", "pageNum":0}

#   return UserDetailsController('user_details', data)


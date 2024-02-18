from flask import Blueprint, request
from flask_pydantic import validate
from flask_restx import Resource, Namespace, fields

from app.decorators import token_required
from app.dtos import RegisterNewAuthenticationModel, AuthenticationModel
from app.services import AuthService

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
api = Namespace("Authentication", description="Authentication related users", authorizations=authorizations)

bp = Blueprint("auth", __name__)
auth_service = AuthService()

# Base Response Model
BaseResponseModel = api.model("BaseResponseModel",
                              {
                                  "message": fields.String,
                              })


# Register Model
RegisterModel = api.model("RegisterModel",
                          {
                              "username": fields.String,
                              "password": fields.String
                          })

# Register Success Model
RegisterProfileModel = api.model("RegisterProfileModel", {
    "username": fields.String
})

RegisterSuccessModel = api.model("RegisterSuccessModel",
                                 {
                                     "message": fields.String,
                                     "result": fields.Nested(RegisterProfileModel)
                                 })


@api.route("/register")
class Register(Resource):
    @api.response(201, "User has been created", RegisterSuccessModel)
    @api.response(409, "Username already exists", BaseResponseModel)
    @api.expect(RegisterModel)
    @validate(body=RegisterNewAuthenticationModel)
    def post(self):
        username = request.body_params.username
        password = request.body_params.password
        return auth_service.register(username, password)


# Login Model
LoginModel = api.model("LoginModel",
                       {
                           "username": fields.String,
                           "password": fields.String
                       })

# Login Success Model
LoginSuccessModel = api.model("LoginSuccessModel",
                              {
                                  "message": fields.String,
                                  "result": fields.String
                              })


@api.route("/login")
class Login(Resource):
    @api.response(200, "User has been logged", LoginSuccessModel)
    @api.response(404, "Invalid username or password", BaseResponseModel)
    @api.expect(LoginModel)
    @validate(body=AuthenticationModel)
    def post(self):
        username = request.body_params.username
        password = request.body_params.password
        return auth_service.login(username, password)


# My Profile Model
ProfileModel = api.model("ProfileModel", {
    "username": fields.String
})

MyProfileModel = api.model("MyProfileModel",
                           {
                               "message": fields.String,
                               "result": fields.Nested(ProfileModel)
                           })


@api.route("/profile")
class Profile(Resource):
    @api.response(200, "My user profile", MyProfileModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.doc(security="Bearer Auth")
    @token_required
    def get(self, current_user):
        return {"message": "User profile has been searched",
                "result": {"username": current_user.username}}, 200

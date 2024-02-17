from flask import Blueprint, request
from flask_pydantic import validate
from flask_restx import Resource, Namespace, fields

from app.decorators import token_required
from app.dtos import RegisterNewAuthenticationModel, AuthenticationModel
from app.services import AuthService
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Namespace('Authentication', description='Authentication related users', authorizations=authorizations)

bp = Blueprint('auth', __name__)
auth_service = AuthService()

# Register Model
registerModel = api.model('RegisterModel',
                          {
                              'username': fields.String,
                              'password': fields.String
                          })

# Register Success Model
registerProfileModel = api.model('RegisterProfileModel', {
    'username': fields.String
})

registerSuccessModel = api.model('RegisterSuccessModel',
                          {
                              'message': fields.String,
                              'result': fields.Nested(registerProfileModel)
                          })

# Login Model
loginModel = api.model('LoginModel',
                       {
                           'username': fields.String,
                           'password': fields.String
                       })

# Login Success Model
loginSuccessModel = api.model('LoginSuccessModel',
                          {
                              'message': fields.String,
                              'result': fields.String
                          })

# My Profile Model
profileModel = api.model('ProfileModel', {
    'username': fields.String
})

myProfileModel = api.model('MyProfileModel',
                          {
                              'message': fields.String,
                              'result': fields.Nested(profileModel)
                          })

# Base Response Model
baseResponseModel = api.model('BaseResponseModel',
                          {
                              'message': fields.String,
                          })


@api.route('/register')
class Register(Resource):
    @api.response(201, "User created successfully", registerSuccessModel)
    @api.response(409, "Username already exists", baseResponseModel)
    @api.expect(registerModel)
    @validate(body=RegisterNewAuthenticationModel)
    def post(self):
        username = request.body_params.username
        password = request.body_params.password
        return auth_service.register(username, password)


@api.route('/login')
class Login(Resource):
    @api.response(200, "User has been logged", loginSuccessModel)
    @api.response(404, "Invalid username or password", baseResponseModel)
    @api.expect(loginModel)
    @validate(body=AuthenticationModel)
    def post(self):
        username = request.body_params.username
        password = request.body_params.password
        return auth_service.login(username, password)


@api.route('/profile')
class Profile(Resource):
    @api.response(200, "My user profile", myProfileModel)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, current_user):
        return {"message": "User profile has been searched",
                "result": {"username": current_user.username}}, 200

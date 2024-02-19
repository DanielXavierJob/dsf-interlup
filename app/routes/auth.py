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
    """
        Decorator: @api.route("/register")

        Description:
        Specifies the route "/register" for the Register resource within the API.

        Class: Register(Resource)

        Description:
        This class represents the Register resource in the API. It handles HTTP POST requests for user registration.

        Method: post(self)

        Description:
        Handles HTTP POST requests to the "/register" endpoint. It expects a JSON payload containing the username and
        password for user registration. Validates the request body using the RegisterNewAuthenticationModel schema.
        Calls the register method of the auth_service to register a new user with the provided username and password.
        Returns appropriate responses based on the registration outcome.

        Responses:
        - 201: User has been successfully created. Returns a RegisterSuccessModel instance.
        - 409: Username already exists. Returns a BaseResponseModel instance indicating the conflict.
    """

    @api.response(201, "User has been created", RegisterSuccessModel)
    @api.response(409, "Username already exists", BaseResponseModel)
    @api.expect(RegisterModel)
    @validate(body=RegisterNewAuthenticationModel)
    def post(self):
        """
            Method: post(self)

            Description:
            Handles HTTP POST requests to the "/register" endpoint. It expects a JSON payload containing the username
            and password for user registration. Validates the request body using the RegisterNewAuthenticationModel
            schema. Calls the register method of the auth_service to register a new user with the provided username
            and password. Returns appropriate responses based on the registration outcome.

            Decorators:
            - @api.response(201, "User has been created", RegisterSuccessModel): Indicates that if the registration is
              successful, the response will have HTTP status code 201 and will be accompanied by a RegisterSuccessModel
              instance.
            - @api.response(409, "Username already exists", BaseResponseModel): Indicates that if the registration fails
              due to the username already existing, the response will have HTTP status code 409 and will be accompanied
              by a BaseResponseModel instance.
            - @api.expect(RegisterModel): Specifies the expected JSON schema for the request body, using the
              RegisterModel.
            - @validate(body=RegisterNewAuthenticationModel): Validates the request body against the
              RegisterNewAuthenticationModel schema.

            Returns:
            The result of the register method called from the auth_service.
        """

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
    """
        Decorator: @api.route("/login")

        Description:
        Specifies the route "/login" for the Login resource within the API.

        Class: Login(Resource)

        Description:
        This class represents the Login resource in the API. It handles HTTP POST requests for user login.

        Method: post(self)

        Description:
        Handles HTTP POST requests to the "/login" endpoint. It expects a JSON payload containing the username and
        password for user login. Validates the request body using the AuthenticationModel schema. Calls the login method
        of the auth_service to authenticate the user with the provided username and password. Returns appropriate
        responses based on the authentication outcome.

        Responses:
        - 200: User has been successfully logged in. Returns a LoginSuccessModel instance.
        - 404: Invalid username or password. Returns a BaseResponseModel instance indicating the failure.
    """

    @api.response(200, "User has been logged", LoginSuccessModel)
    @api.response(404, "Invalid username or password", BaseResponseModel)
    @api.expect(LoginModel)
    @validate(body=AuthenticationModel)
    def post(self):
        """
            Method: post(self)

            Description:
            Handles HTTP POST requests to the "/login" endpoint. It expects a JSON payload containing the username and
            password for user login. Validates the request body using the AuthenticationModel schema. Calls the login
            method of the auth_service to authenticate the user with the provided username and password. Returns
            appropriate responses based on the authentication outcome.

            Decorators:
            - @api.response(200, "User has been logged", LoginSuccessModel): Indicates that if the authentication is
              successful, the response will have HTTP status code 200 and will be accompanied by a LoginSuccessModel
              instance.
            - @api.response(404, "Invalid username or password", BaseResponseModel): Indicates that if the
              authentication fails due to invalid credentials, the response will have HTTP status code 404 and will be
              accompanied by a BaseResponseModel instance.
            - @api.expect(LoginModel): Specifies the expected JSON schema for the request body, using the LoginModel.
            - @validate(body=AuthenticationModel): Validates the request body against the AuthenticationModel schema.

            Returns:
            The result of the login method called from the auth_service.
        """

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
        """
            Decorator: @api.route("/profile")

            Description:
            Specifies the route "/profile" for the Profile resource within the API.

            Class: Profile(Resource)

            Description:
            This class represents the Profile resource in the API. It handles HTTP GET requests for retrieving user
            profile information.

            Method: get(self, current_user)

            Description:
            Handles HTTP GET requests to the "/profile" endpoint. It requires a valid authentication token to access
            the user's profile information. Uses the token_required decorator to enforce authentication. Returns
            appropriate responses based on the authentication outcome.

            Parameters:
            - current_user: The current authenticated user obtained from the token.

            Decorators:
            - @api.response(200, "My user profile", MyProfileModel): Indicates that if the authentication is successful,
              the response will have HTTP status code 200 and will be accompanied by a MyProfileModel instance.
            - @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel): Indicates that if the
              authentication fails or no token is provided, the response will have HTTP status code 401 and will be
              accompanied by a BaseResponseModel instance.
            - @api.doc(security="Bearer Auth"): Specifies the security requirements for accessing this endpoint,
              indicating that a Bearer token is required.
            - @token_required: Enforces authentication for accessing the endpoint.

            Returns:
            A dictionary containing a message indicating the success of the profile search along with the user's profile information.
        """

        return {"message": "User profile has been searched",
                "result": {"username": current_user.username}}, 200

from firebase_admin import auth, exceptions

from yd_base_py.yellowdot.firebase.YDFirebase import YDFirebase
from yd_base_py.yellowdot.utils.YDCommon import YDCommon
from yd_base_py.yellowdot.utils.YDLogger import YDLogger
from yd_base_py.yellowdot.models.FBUserResponse import FBUsersResponse


class YDFBUserUtils(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(YDFBUserUtils, cls).__new__(cls)
        return cls._instance

    # Returns instance of the firebase user utils class
    @staticmethod
    def get_instance(self):
        if not YDFBUserUtils._instance:
            YDFBUserUtils._instance = YDFBUserUtils(self.firebase)
        return YDFBUserUtils._instance

    def __init__(self, yd_firebase: YDFirebase):
        self.firebase = yd_firebase
        self.logger = YDLogger("YDFBUserUtils").get_instance()

    # Returns the created user object for the given email, password and display name
    def create_user(self, email: str, password: str, display_name: str, provider: str = None, phone_number: str = None, photo_url: str = None):
        self.logger.info("create_user(email: {0}, password: {1}, display_name: {2}) -->".format(email, password, display_name))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("create_user(Firebase is initialized) <--")
            return None
        try:
            uid = YDCommon.get_instance().generate_uid()
            verified_email = False
            user = self.get_user_by_uid(uid)
            if user:
                uid = YDCommon.get_instance().generate_uid()
            if provider:
                verified_email = True
            user = auth.create_user(uid=uid, email_verified=verified_email, email=email, phone_number=phone_number, password=password,
                                    display_name=display_name, photo_url=photo_url, disabled=False)
            if user:
                self.logger.success("create_user(User created successfully with uid -> {uid}) <--".format(uid=uid))
                return user
            else:
                self.logger.success("create_user(User not created successfully with uid -> {uid}) <--".format(uid=uid))
                return None
        except exceptions.FirebaseError as e:
            self.logger.error("create_user(Error creating user: {0}) <--".format(e))
            return None

    # Returns the user object for the given uid
    def get_user_by_uid(self, uid: str):
        self.logger.info("get_user_by_uid(uid: {0}) -->".format(uid))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("get_user_by_uid(Firebase is initialized) <--")
            return None
        try:
            user = auth.get_user(uid)
            if user:
                self.logger.success("get_user_by_uid(User found with uid -> {uid}) <--".format(uid=uid))
                return user
            else:
                self.logger.success("get_user_by_uid(User not found with uid -> {uid}) <--".format(uid=uid))
                return None
        except exceptions.FirebaseError as e:
            self.logger.error("get_user_by_uid(Error fetching user data: {0}) <--".format(e))
            return None

    def update_user(self, uid: str, email: str, phone_number: str, email_verified: str, password: str,
                    display_name: str, photo_url: str):
        self.logger.info(
            "update_user(uid: {0}, email: {1}, password: {2}, display_name: {3}) -->".format(uid, email, password,
                                                                                             display_name))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("update_user(Firebase is initialized) <--")
            return None
        try:
            user = self.get_user_by_uid(uid)
            if user:
                user = auth.update_user(
                    uid=uid,
                    email=email,
                    phone_number=phone_number,
                    email_verified=email_verified,
                    password=password,
                    display_name=display_name,
                    photo_url=photo_url,
                )
                if user:
                    self.logger.success("update_user(User updated successfully with uid -> {uid}) <--".format(uid=uid))
                    return user
                else:
                    self.logger.error(
                        "update_user(User not updated successfully with uid -> {uid}) <--".format(uid=uid))
                    return None
            else:
                self.logger.warning("update_user(User not found with uid -> {uid}) <--".format(uid=uid))
                return None
        except exceptions.FirebaseError as e:
            self.logger.error("update_user(Error updating user data: {0}) <--".format(e))
            return None

    # Deletes the user for the given uid
    def delete_user(self, uid: str) -> bool:
        self.logger.info("delete_user(uid: {0}) -->".format(uid))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("delete_user(Firebase is initialized) <--")
            return False
        try:
            user = self.get_user_by_uid(uid)
            if user:
                auth.delete_user(uid)
                self.logger.success("delete_user(User deleted successfully with uid -> {uid}) <--".format(uid=uid))
                return True
            else:
                self.logger.warning("delete_user(User not found with uid -> {uid}) <--".format(uid=uid))
                return False
        except exceptions.FirebaseError as e:
            self.logger.error("Error deleting user data: {0}".format(e))
            return False

    # Deletes many users for the given uid_s
    def delete_users(self, uid_s: list) -> bool:
        self.logger.info("delete_users(uid_s: {0}) -->".format(uid_s))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("delete_users(Firebase is initialized) <--")
            return False
        try:
            for uid in uid_s:
                user = self.get_user_by_uid(uid)
                if user:
                    auth.delete_users(uid_s)
                    self.logger.success(
                        "delete_users(User deleted successfully with uid -> {uid}) <--".format(uid=uid))
                else:
                    self.logger.warning("delete_users(User not found with uid -> {uid}) <--".format(uid=uid))
            return True
        except exceptions.FirebaseError as e:
            self.logger.error("Error deleting users data: {0}".format(e))
            return False

    # Returns users list in batches of 1000 from firebase
    def get_users(self, page_token: str = None, max_results: int = 1000):
        self.logger.info("get_users(page_token: {0}, max_results: {1}) -->".format(page_token, max_results))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("get_users(Firebase is initialized) <--")
            return None
        try:
            users = auth.list_users(page_token=page_token, max_results=max_results)
            has_next_page = users.has_next_page
            next_page_token = users.next_page_token
            page_index = page_token
            page_size = max_results
            if users:
                self.logger.success("get_users(Users found) <--")
                return FBUsersResponse(users=users.users, next_page_token=next_page_token, has_next_page=has_next_page, page_index=page_index,
                                       page_size=page_size)
            else:
                self.logger.success("get_users(Users not found) <--")
                return None
        except exceptions.FirebaseError as e:
            self.logger.error("get_users(Error fetching users data: {0}) <--".format(e))
            return None

    # Verifies id token provided by the client
    def verify_id_token(self, id_token: str):
        self.logger.info("verify_id_token(id_token: {0}) -->".format(id_token))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("verify_id_token(Firebase is initialized) <--")
            return None
        try:
            decoded_token = auth.verify_id_token(id_token)
            if decoded_token:
                self.logger.success("verify_id_token(Token verified successfully) <--")
                return decoded_token
            else:
                self.logger.success("verify_id_token(Token not verified) <--")
                return None
        except exceptions.FirebaseError as e:
            self.logger.error("verify_id_token(Error verifying token: {0}) <--".format(e))
            return None

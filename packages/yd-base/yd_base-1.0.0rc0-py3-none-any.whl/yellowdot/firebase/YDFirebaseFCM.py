from firebase_admin import messaging, exceptions

from yd_base_py.yellowdot.firebase.YDFirebase import YDFirebase
from yd_base_py.yellowdot.utils.YDLogger import YDLogger


class YDFirebaseFCM(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(YDFirebaseFCM, cls).__new__(cls)
        return cls._instance

    # Returns instance of the firebase fcm utils class
    @staticmethod
    def get_instance(self):
        if not YDFirebaseFCM._instance:
            YDFirebaseFCM._instance = YDFirebaseFCM(self.firebase)
        return YDFirebaseFCM._instance

    def __init__(self, yd_firebase: YDFirebase):
        self.firebase = yd_firebase
        self.logger = YDLogger("YDFBCloudMessaging").get_instance()

    # Sends a notification to the given device token
    def send_notification_to_device(self, device_token: str, title: str, body: str, data: dict = None, deep_link: str = None, tag: str = None):
        self.logger.info(
            "send_notification(device_token: {0}, title: {1}, body: {2}, data: {3}) -->".format(device_token, title, body, data, tag))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("send_notification(Firebase is initialized) <--")
            return None
        try:
            android_notification = self.get_android_notification(title, body, deep_link, tag)
            apns_notification = self.get_apns_notification(title, body)
            web_push_notification = self.get_web_notification(title, body)
            message = messaging.Message(
                data=data,
                notification=messaging.Notification(title=title, body=body),
                android=self.get_android_config(notification=android_notification),
                apns=self.get_apns_config(payload=apns_notification),
                webpush=self.get_web_push_config(notification=web_push_notification),
                token=device_token
            )
            response = messaging.send(message)
            self.logger.success(
                "send_notification(Notification sent successfully to device token -> {device_token}) <--".format(
                    device_token=device_token))
            return response
        except exceptions.FirebaseError as e:
            self.logger.error("send_notification(Error sending notification: {0}) <--".format(e))
            return None

    # Sends a notification to the list of given device tokens
    def send_notification_to_devices(self, device_tokens: list, title: str, body: str, data: dict = None):
        self.logger.info(
            "send_notification_to_devices(device_tokens: {0}, title: {1}, body: {2}, data: {3}) -->".format(
                device_tokens, title,
                body, data))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("send_notification_to_devices(Firebase is initialized) <--")
            return None
        try:
            android_notification = self.get_android_notification(title, body)
            apns_notification = self.get_apns_notification(title, body)
            web_push_notification = self.get_web_notification(title, body)
            message = messaging.MulticastMessage(
                data=data,
                notification=messaging.Notification(title=title, body=body),
                android=self.get_android_config(notification=android_notification),
                apns=self.get_apns_config(payload=apns_notification),
                webpush=self.get_web_push_config(notification=web_push_notification),
                tokens=device_tokens
            )
            response = messaging.send_each_for_multicast(message)
            self.logger.success(
                "send_notification_to_devices(Notification sent successfully to device tokens -> {device_tokens}) <--"
                .format(device_tokens=device_tokens))
            return response
        except exceptions.FirebaseError as e:
            self.logger.error("send_notification_to_devices(Error sending notification: {0}) <--".format(e))
            return None

    # Sends notification to the given topic
    def send_notification_to_topic(self, topic: str, title: str, body: str, data: dict = None, deep_link: str = None):
        self.logger.info("send_notification(topic: {0}, title: {1}, body: {2}, data: {3}) -->".format(topic, title, body, data))
        if not self.firebase.get_firebase_initialized():
            self.logger.info("send_notification(Firebase is initialized) <--")
            return None
        try:
            android_notification = self.get_android_notification(title, body, deep_link)
            apns_notification = self.get_apns_notification(title, body)
            web_push_notification = self.get_web_notification(title, body)
            message = messaging.Message(
                data=data,
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                android=self.get_android_config(notification=android_notification),
                apns=self.get_apns_config(payload=apns_notification),
                webpush=self.get_web_push_config(notification=web_push_notification),
                topic=topic
            )
            response = messaging.send(message)
            self.logger.success(
                "send_notification(Notification sent successfully to topic -> {topic}) <--".format(topic=topic))
            return response
        except exceptions.FirebaseError as e:
            self.logger.error("send_notification(Error sending notification: {0}) <--".format(e))
            return None

    # Provide android config object
    @staticmethod
    def get_android_config(ttl: int = 3600, priority: str = "high", collapse_key: str = None, notification: messaging.AndroidNotification = None):
        return messaging.AndroidConfig(ttl=ttl, priority=priority, collapse_key=collapse_key, notification=notification)

    # Provide apns config object
    @staticmethod
    def get_apns_config(headers: dict = None, payload: messaging.APNSPayload = None):
        return messaging.APNSConfig(headers=headers, payload=payload)

    # Provide web push config object
    @staticmethod
    def get_web_push_config(headers: dict = None, data: dict = None, notification: messaging.WebpushNotification = None):
        return messaging.WebpushConfig(headers=headers, data=data, notification=notification)

    @staticmethod
    # Provides android notification object
    def get_android_notification(title: str, body: str, icon: str = "default", color: str = "#f45342", tag: str = "test", click_action: str = None):
        return messaging.AndroidNotification(title=title, body=body, icon=icon, color=color, sound="default", click_action=click_action, tag=tag)

    # Provides apns notification object
    @staticmethod
    def get_apns_notification(title: str, body: str, badge: int = 1, sound: str = "default"):
        return messaging.APNSPayload(aps=messaging.Aps(alert=messaging.ApsAlert(title=title, body=body), badge=badge, sound=sound))

    # Provides web notification object
    @staticmethod
    def get_web_notification(title: str, body: str, icon: str = "default"):
        return messaging.WebpushNotification(title=title, body=body, icon=icon, image="https://www.yellowdotenergy.com/footer-assets/Logo.svg")

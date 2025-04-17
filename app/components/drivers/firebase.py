import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError

from app.core.config import Settings
from app.db.enums import InspectionStatusEnum


class FirebaseDriver:
    def __init__(self, context):
        print("Firebase configuration.. ")

        inspection = context.get("inspection")
        self.state = InspectionStatusEnum.get_value_from_id(
            inspection.inspection_status_id
        )

        self.inspection = inspection
        self.context = context
        self.config = Settings()
        print("firebase config.. ")
        self.firebase_credentials = self.config.firebase_credentials
        if not self.firebase_credentials:
            raise ValueError(
                "Missing 'firebase_credentials' in .env file."
            )
        print("firebase firebase_credentials.. ")

        self.firebase_token = self.inspection.notification_info.get(
            'firebase_token'
        )

        print(
            "firebase token ok"
        )
        self.initialize_firebase()
        print("finish firebase initialize")

    def initialize_firebase(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.firebase_credentials)
                firebase_admin.initialize_app(cred)
                print("[firebase] Initialized Firebase app.")
            else:
                print("[firebase] Firebase already initialized.")
        except FileNotFoundError as e:
            print(f"[firebase] Credential file not found: {e}")
        except ValueError as e:
            print(f"[firebase] Initialization error: {e}")
        except FirebaseError as e:
            print(f"[firebase] Firebase SDK error: {e}")
        except Exception as e:
            print(f"[firebase] Unknown error initializing Firebase: {e}")

    def send_notification(self):
        print("sending notification.. ")
        if self.state == InspectionStatusEnum.COMPLETED:
            message_title = "Inspection Completed"
            message_body = "The inspection has been completed successfully."
        elif self.state == InspectionStatusEnum.ERROR:
            message_title = "Inspection Error"
            message_body = "An error occurred during the inspection."
        else:
            raise ValueError(
                f"Unsupported state '{self.state}' for notification."
            )

        print(f"Message: {message_title}")

        message = messaging.Message(
            data={
                "inspection_id": str(self.inspection.id),
                "status": self.state.value,
                "message": message_body
            },
            notification=messaging.Notification(
                title=message_title,
                body=message_body
            ),
            token=self.firebase_token
        )

        response = messaging.send(message)
        print(f"Notification sent with response: {response}")
        return response

    def execute(self):
        if not self.firebase_token:
            print("Firebase token not present")
            return self.context

        print("Executing FirebaseDriver...")
        self.send_notification()
        return self.context

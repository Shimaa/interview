import random
import string

# Enum to define the size of the parcel and locker
class Size:
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


# Class representing the Parcel
class Parcel:
    def __init__(self, parcel_id, size):
        self.parcel_id = parcel_id
        self.size = size

        
# Class representing the Locker
class Locker:
    def __init__(self, locker_id, size):
        self.locker_id = locker_id
        self.size = size
        self.is_available = True
        self.pin_code = None
        self.parcel = None

    def store_parcel(self, parcel):
        if self.is_available and parcel.size == self.size:
            self.parcel = parcel
            self.pin_code = self.generate_pin_code()
            self.is_available = False
            print(f"Parcel {parcel.parcel_id} stored in Locker {self.locker_id}.")
            return self.pin_code
        else:
            print(f"Locker {self.locker_id} is not available or the sizes don't match.")
            return None

    def release_parcel(self, pin_code):
        if self.pin_code == pin_code:
            print(f"Parcel {self.parcel.parcel_id} released from Locker {self.locker_id}.")
            self.is_available = True
            self.parcel = None
            self.pin_code = None
        else:
            print("Invalid pin code! Cannot release parcel.")
    
    def is_locker_available(self):
        return self.is_available

    def generate_pin_code(self):
        return ''.join(random.choices(string.digits, k=6))


# Class representing a User
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def pick_up_parcel(self, locker, pin_code):
        locker.release_parcel(pin_code)


# Class representing the Delivery Agent
class DeliveryAgent:
    def __init__(self, agent_id, name):
        self.agent_id = agent_id
        self.name = name

    def deliver_parcel(self, locker_manager, parcel):
        locker = locker_manager.find_available_locker(parcel)
        if locker:
            pin_code = locker.store_parcel(parcel)
            return locker, pin_code
        else:
            print(f"No available lockers for parcel {parcel.parcel_id}.")
            return None, None


# Class representing the Locker Manager
class LockerManager:
    def __init__(self):
        self.lockers = []

    def add_locker(self, locker):
        self.lockers.append(locker)

    def find_available_locker(self, parcel):
        for locker in self.lockers:
            if locker.is_locker_available() and locker.size == parcel.size:
                return locker
        return None


# Class for managing notifications (Email/SMS)
class NotificationService:
    def __init__(self):
        self.notifications = []

    def send_notification(self, user, locker, pin_code):
        message = f"Hi {user.name}, your parcel is stored in Locker {locker.locker_id}. Your pin code is {pin_code}."
        print(f"Notification sent to {user.email}: {message}")
        self.notifications.append(message)


# Test the system with an example
def test_amazon_locker_service():
    # Create Locker Manager
    locker_manager = LockerManager()

    # Add Lockers
    locker_manager.add_locker(Locker('L1', Size.SMALL))
    locker_manager.add_locker(Locker('L2', Size.MEDIUM))
    locker_manager.add_locker(Locker('L3', Size.LARGE))

    # Create Users
    user1 = User('U1', 'Alice', 'alice@example.com')

    # Create Delivery Agent
    agent = DeliveryAgent('A1', 'Bob')

    # Create a Parcel and try delivering it
    parcel1 = Parcel('P1', Size.SMALL)
    locker, pin_code = agent.deliver_parcel(locker_manager, parcel1)

    if locker:
        # Notify the User
        notification_service = NotificationService()
        notification_service.send_notification(user1, locker, pin_code)

        # User picks up the parcel
        user1.pick_up_parcel(locker, pin_code)


# Run the test
test_amazon_locker_service()

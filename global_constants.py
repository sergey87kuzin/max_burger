import enum


class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    STAFF = 'staff'


class PaymentStatus(str, enum.Enum):
    NOT_PAID = 'not_paid'
    SWITCHED_TO_PAYMENT = 'switched_to_payment'
    PAID = 'paid'


class PaymentType(str, enum.Enum):
    CASH = 'cash'
    CARD_COURIER = 'card'
    ONLINE = 'online'


class DeliveryType(str, enum.Enum):
    IN_REST = 'in rest'
    COURIER = 'courier'

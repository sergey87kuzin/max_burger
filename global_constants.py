import enum


class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    STAFF = 'staff'


class PaymentStatus(str, enum.Enum):
    NOT_PAID = 'not_paid'
    SWITCHED_TO_PAYMENT = 'switched_to_payment'
    PAID = 'paid'

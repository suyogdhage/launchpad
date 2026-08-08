import enum

class UserRole(str, enum.Enum):
    SUPERADMIN = "superadmin"
    HR = "hr"
    MANAGER = "manager"
    NEW_HIRE = "new_hire"

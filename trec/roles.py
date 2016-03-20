from rolepermissions.roles import AbstractUserRole

class Researcher(AbstractUserRole):
    available_permissions = {
        'upload_file': True,
    }

class Admin(AbstractUserRole):
    available_permissions = {
        'upload_file': True,
        'edit_tracks': True,
    }
from rolepermissions.roles import AbstractUserRole

class Researcher(AbstractUserRole):
    available_permissions = {
        'upload_file': True,
        'send_message': True,
    }

class Admin(AbstractUserRole):
    available_permissions = {
        'upload_file': True,
        'send_message': True,
        'edit_tracks': True,
        'bypass_captcha': True,
    }
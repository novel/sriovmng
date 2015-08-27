class SriovError(Exception):
    pass


class SriovDeviceNotFound(SriovError):

    message = "Device not found: %(device)s."

    def __init__(self, **kwargs):
        super(SriovDeviceNotFound, self).__init__(self.message % kwargs)

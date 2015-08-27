class SriovError(Exception):
    message = "SR-IOV exception"

    def __init__(self, **kwargs):
        super(SriovError, self).__init__(self.message % kwargs)
        self.msg = self.message % kwargs


class SriovDeviceNotFound(SriovError):
    message = "Device not found: %(device)s."

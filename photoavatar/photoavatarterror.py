class PhotoAvatarError(Exception):
    IMAGE_ERROR = 1001
    IO_ERROR=1002
    def __init__(self, code,description):
        super()
        self.code = code
        self.description = description
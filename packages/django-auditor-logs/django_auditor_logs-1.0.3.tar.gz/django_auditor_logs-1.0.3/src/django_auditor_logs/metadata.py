class MetadataManager:
    user_metadata = "Sin metadatos"
    request_metadata = "Sin metadatos"

    @classmethod
    def set_user_metadata(self, metadata):
        self.user_metadata = metadata

    @classmethod
    def set_request_metadata(self, metadata):
        self.request_metadata = metadata

    @classmethod
    def get_user_metadata(self):
        return self.user_metadata

    @classmethod
    def get_request_metadata(self):
        return self.request_metadata
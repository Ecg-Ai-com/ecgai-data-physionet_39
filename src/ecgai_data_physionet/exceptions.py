class InValidRecordError(Exception):
    # @log
    def __init__(self, record_id: int = None, data_base_name: str = None):
        message = "The record was not found"
        if record_id is not None:
            message += f" record_id {record_id}"
        if data_base_name is not None:
            message += f" from {data_base_name}"
        super(InValidRecordError, self).__init__(message)


class InvalidSampleRateError(Exception):
    # @log
    def __init__(
        self,
        sample_rate: int,
        sample_rate_valid_numbers: str = "either 100 or 500",
        record_id: int = None,
        data_base_name: str = None,
    ):
        message = f"The sample rate is invalid it needs to be {sample_rate_valid_numbers}, your value was {sample_rate}"
        if record_id is not None:
            message += f" on record_id {record_id}"
        if data_base_name is not None:
            message += f" from {data_base_name}"
        super(InvalidSampleRateError, self).__init__(message)


class FileNotDownloadedError(Exception):
    def __init__(self, filename: str):
        message = f"{filename} was not downloaded"
        super(FileNotDownloadedError, self).__init__(message)

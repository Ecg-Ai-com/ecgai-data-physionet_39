import asyncio
import logging

import pytest

from ecgai_data_physionet.exceptions import InvalidRecordError
from ecgai_data_physionet.file_loader import FileLoader
from ecgai_data_physionet.models.ecg import EcgRecord


def module_logging_level():
    return logging.DEBUG


def logger_name():
    return "physionet"


valid_record_path_name = {
    "test_data/A0001",
    "test_data/A0002",
    "test_data/E06003",
    "test_data/E06004",
}

invalid_record_path_name = {
    "test_data/A000231",
    "test_data/A003402",
    "test_data/E06234003",
    "test_data/E06234004",
}


@pytest.mark.parametrize("record_path", valid_record_path_name)
@pytest.mark.asyncio
async def test_get_records_list_return_valid_ecg_record(record_path, caplog):
    with caplog.at_level(level=module_logging_level(), logger=logger_name()):
        data_set_name = "cpsc_2018"
        sut = FileLoader(data_set_name=data_set_name)
        record_task = asyncio.create_task(sut.get_record(record_path_name=record_path))
        result = await record_task
        assert type(result) is EcgRecord
        # name = os.path.basename(record_name)
        assert result.database_name == data_set_name

        assert result.age is not None
        assert result.sex is not None
        assert len(result.diagnostic_codes) > 0


@pytest.mark.parametrize("record_path", invalid_record_path_name)
@pytest.mark.asyncio
async def test_get_record_with_does_not_exist_record_id_raise_exception(record_path, caplog):
    with caplog.at_level(level=module_logging_level(), logger=logger_name()):
        data_set_name = "cpsc_2018"
        sut = FileLoader(data_set_name=data_set_name)
        with pytest.raises(InvalidRecordError):
            await sut.get_record(record_path_name=record_path)

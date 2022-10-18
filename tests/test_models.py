import json
import logging
import os
import pathlib
from typing import List

import numpy as np

from ecgai_data_physionet.models.diagnostic_code import DiagnosticCode
from ecgai_data_physionet.models.ecg import EcgRecord
from ecgai_data_physionet.models.ecg_lead import EcgLeadRecord
from ecgai_data_physionet.ptbxl import MetaDataRow


def module_logging_level():
    return logging.ERROR


ROOT_DIR = pathlib.Path(__file__).parent.absolute()


def logger_name():
    return "models"


def setup_test_record_data():
    path = os.path.join(ROOT_DIR, "test_data", "00001_hr.json")
    with open(path) as json_file:
        data = json.load(json_file)
    record = EcgRecord.from_json(data)
    assert type(record) is EcgRecord
    return record


def test_create_data_set_record(caplog):
    # try:
    with caplog.at_level(level=module_logging_level(), logger=logger_name()):
        random_signals = np.random.random(50)
        test_signal: List[float] = random_signals.tolist()
        test_lead = EcgLeadRecord.create("II", test_signal)
        test_leads = [test_lead]
        record = EcgRecord.create(
            record_id=1,
            record_name="messageId",
            database_name="database",
            sample_rate=200,
            leads=test_leads,
        )
        assert record.sample_rate == 200
        assert type(record) is EcgRecord


def test_read_from_json(caplog):
    with caplog.at_level(level=module_logging_level(), logger=logger_name()):
        record = setup_test_record_data()
        assert type(record) is EcgRecord


def test_create_description_code(caplog):
    with caplog.at_level(level=module_logging_level(), logger=logger_name()):
        scp_code = "DEF"
        description = "This is my class"
        sut = DiagnosticCode.create(scp_code=scp_code, description=description)
        assert type(sut) is DiagnosticCode
        assert sut.scp_code == scp_code
        assert sut.description == description
        # Is(sut.scp_code).not_empty.matches(scp_code)
        # Is(sut.description).not_empty.matches(description)


def test_meta_data_row_with_invalid_age():
    sut = MetaDataRow(ecg_id=1, patient_id=1, age="asda", sex=0, report="ssd", scp_codes="test:34")
    assert sut.age == 0


def test_meta_data_row_with_valid_age():
    sut = MetaDataRow(ecg_id=1, patient_id=1, age="78", sex=0, report="ssd", scp_codes="test:34")
    assert sut.age == 78

""" Unit test of yaccounts package"""

import pytest
import parametrize_from_file
import yaml

from yaccounts import CsvDataAnalyzer


@pytest.fixture(scope="class")
def aa():
    aa = CsvDataAnalyzer("data.csv")
    aa.run()
    yield aa


class TestBalances:
    @parametrize_from_file.parametrize("balances.yml")
    def test_balances(self, operating_unit, year, balance, aa):
        matches = aa.find(operating_unit, year)

        assert len(matches) == 1, f"Cannot find match for {operating_unit} {year}"
        assert round(matches[0].balance) == round(
            balance
        ), f"Balance for {operating_unit} - {year} does not match"

    def test_student_names(self, aa):
        for operating_unit in aa.get_all_operating_units():
            for student_name in operating_unit.students.keys():
                assert (
                    "benefit" not in student_name.lower()
                ), f"Invalid student name {student_name} in operating unit {operating_unit.operating_unit}."
                assert (
                    "overspent" not in student_name.lower()
                ), f"Invalid student name {student_name} in operating unit {operating_unit.operating_unit}."

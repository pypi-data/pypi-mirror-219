import os.path
import unittest

from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.logging.migration_report import MigrationReport
from src.mb_cruise_migration.migration_properties import MigrationProperties
from testutils import delete_test_logs


class TestLoggers(unittest.TestCase):
    MigrationProperties("config_test.yaml")
    MigrationLog()
    MigrationReport()

    def test_file_creation(self):
        MigrationLog.log.info("THIS IS A TEST")
        MigrationLog.review.info("THIS IS A TEST")
        MigrationReport.report.info("THIS IS A TEST")

        assert os.path.exists("log")
        assert os.path.exists("report")
        assert os.path.exists("review")

        delete_test_logs()

from unittest import TestCase

from ExoiTest.GenerateTestCaseBat.GenerateTestCase import update_message_share_folder, update_running_job_host


class Test2(TestCase):

    def test_update_message_share_folder(self):
        root = "D:\QA\GEDF\GEDataFeed-master"
        message_share_floder = "testFolder"
        update_message_share_folder(root, message_share_floder)

    def test_update_running_job_host(self):
        root = "D:\QA\GEDF\GEDataFeed-master"
        host_name = "testHost"
        update_running_job_host(root, host_name)
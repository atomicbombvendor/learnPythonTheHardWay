from unittest import TestCase

from ExoiTest.AutoTest.AutoTest import *
from ExoiTest.GenerateTestCaseBat.GenerateTestCase import update_message_share_folder


class TestFind_targetZipFile(TestCase):
    def test_find_targetZipFile(self):
        root = "D:\QA\GEDF\GeDataFeed-MOCAL5273\GEDF"
        file_date = "2018-4"
        d_file_date = '2018-05-03'
        file_name = "OwnershipDetails"
        results = find_targetZipFile(root_path=root, file_name=file_name, monthly_fileDate=file_date, daily_delta_fileDate=d_file_date)
        print(results)

    def test_generate_Zip_Content(self):
        root = "D:\QA\GEDF\GeDataFeed-MOCAL5273\GEDF"
        root2 = "D:\QA\GEDF\GeDataFeed-MOCAL5273\GEDF"
        file_date = "2018-4"
        d_file_date = '2018-05-03'
        file_name = "OwnershipDetails"
        results = find_targetZipFile(root_path=root, file_name=file_name, monthly_fileDate=file_date, daily_delta_fileDate=d_file_date)
        generate_compare_Zip_Content(results, root2, root)

    def test_update_message_share_folder(self):
        root = "D:\QA\GEDF\GEDataFeed-master"
        message_share_floder = "testFolder"
        update_message_share_folder(root, message_share_floder)
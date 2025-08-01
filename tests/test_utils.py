from unittest import TestCase

from mediarenamer import utils


class TestUtils(TestCase):

    season_directory_list = [
        "Futurama (1999) Season 8 S08 (1080p DSNP WEB-DL x265 HEVC 10bit EAC3 5.1 t3nzin)",
        "Futurama.S11.1080p.x265-ELiTE[eztv.re]",
        "futurama-1",
        "Riverdale.US.S02.COMPLETE.720p.BluRay.x264-GalaxyTV[TGx]",
        "Riverdale.US.S04.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]",
        "Riverdale.US.S06.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]",
    ]

    show_directory_list = [
        "Band of Brothers (2001)",
        "Chernobyl (2019)",
        "Disenchantment (2018)",
        "Futurama (1999)",
    ]

    file_list = [
        "Chernobyl (2019) - S01E01 - 1.23.45 (1080p BluRay x265 Silence).mkv",
        "Band Of Brothers Part 1 Currahee (1080p x265 Joy).mkv",
        "Band Of Brothers Documentry 2001 (1080p x265 Joy).mkv",
        "Encoded by JoyBell.txt",
        "Riverdale.US.S02E01.720p.BluRay.x264-GalaxyTV.mkv",
        "Futurama (1999) - S08E01 - The Impossible Stream (1080p DSNP WEB-DL x265 t3nzin).mkv",
        "Futurama - S01E01 - Space Pilot 3000 [dd].mkv",
    ]

    def test_get_season_number_from_folder_name(self):
        self.assertEqual(utils.get_season_number_from_folder_name(self.season_directory_list[0]), 8)
        self.assertEqual(utils.get_season_number_from_folder_name(self.season_directory_list[1]), 11)
        self.assertEqual(utils.get_season_number_from_folder_name(self.season_directory_list[2]), None)
        self.assertEqual(utils.get_season_number_from_folder_name(self.season_directory_list[3]), 2)
        self.assertEqual(utils.get_season_number_from_folder_name(self.season_directory_list[4]), 4)
        self.assertEqual(utils.get_season_number_from_folder_name(self.season_directory_list[5]), 6)

    def test_get_episode_number_from_file_name(self):
        self.assertEqual(utils.get_episode_number_from_file_name(self.file_list[0]), 1)
        self.assertEqual(utils.get_episode_number_from_file_name(self.file_list[1]), 1)
        self.assertEqual(utils.get_episode_number_from_file_name(self.file_list[2]), None)
        self.assertEqual(utils.get_episode_number_from_file_name(self.file_list[3]), None)
        self.assertEqual(utils.get_episode_number_from_file_name(self.file_list[4]), 1)
        self.assertEqual(utils.get_episode_number_from_file_name(self.file_list[5]), 1)
        self.assertEqual(utils.get_episode_number_from_file_name(self.file_list[6]), 1)

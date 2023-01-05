import unittest

from twdown import TwdownAPI


class TestTwdownAPI(unittest.TestCase):
    def test_raw_link(self):
        sharelink = "https://twitter.com/karenxcheng/status/1554864997586505729?s=20&t=6lNoKzvyezez3a-id7bcSg"
        assert TwdownAPI(sharelink=sharelink).run()

    def test_short_link(self):
        sharelink = "https://twitter.com/karenxcheng/status/1554864997586505729"
        assert TwdownAPI(sharelink=sharelink).run()

    def test_no_video(self):
        sharelink = "https://twitter.com/mranti/status/1610833523606441986"
        assert TwdownAPI(sharelink=sharelink).run() is None

    def test_order_path(self):
        sharelink = "https://twitter.com/hxiao/status/1610572290558758917"
        assert TwdownAPI(sharelink, dir_to_save="tvs/test_order_path").run()

    def test_download_all_videos(self):
        sharelink = "https://twitter.com/hxiao/status/1610572290558758917"
        assert TwdownAPI(
            sharelink, quality="all", dir_to_save="tvs/test_download_all_videos(hxiao)"
        ).run()

    def test_download_min_video(self):
        sharelink = "https://twitter.com/hxiao/status/1610572290558758917"
        assert TwdownAPI(
            sharelink, quality="min", dir_to_save="tvs/test_download_min_video(hxiao)"
        ).run()

    def test_download_max_video(self):
        sharelink = "https://twitter.com/hxiao/status/1610572290558758917"
        assert TwdownAPI(
            sharelink, quality="max", dir_to_save="tvs/test_download_max_video(hxiao)"
        ).run()

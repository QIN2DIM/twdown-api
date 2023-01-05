# -*- coding: utf-8 -*-
# Time       : 2023/1/5 9:05
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import os
import typing
from dataclasses import dataclass
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import ConnectionError


@dataclass
class TwitterVideo:
    quality: str
    download_link: str


class TwdownAPI:
    def __init__(
        self,
        sharelink: str,
        quality: typing.Literal["max", "min", "all"] = "max",
        dir_to_save: typing.Optional[str] = "",
    ):
        """
        TwdownAPI - https://twdown.net/

        :param sharelink: Sharelink of a tweet
        :param quality: Select the quality of the video
            MAX Download the video with the highest resolution
            MIN Download the video with the lowest resolution
            ALL Download all videos
        :param dir_to_save: Resource storage directory
        """
        self._sharelink = sharelink
        self._dir_to_save = dir_to_save or os.path.join(os.path.dirname(__file__), "tvs")
        self._quality = quality
        self._username = ""
        self._vid = ""

        self._parse_sharelink()
        os.makedirs(self._dir_to_save, exist_ok=True)

    class Quality:
        MAX = "max"
        MIN = "min"
        ALL = "all"

    def _parse_sharelink(self):
        _p = urlparse(self._sharelink)
        self._username = _p.path.split("/")[1]
        self._vid = _p.path.split("/")[-1]

    @staticmethod
    def _post_sharelink(sharelink: str) -> typing.Optional[Response]:
        """
        Post a request to the TWDOWN public API to get the response
        :param sharelink:
        :return:
        """
        api = "https://twdown.net/download.php"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
            "origin": "https://twdown.net",
            "referer": "https://twdown.net/index.php",
        }
        data = {"URL": sharelink}
        resp = requests.post(api, data=data, headers=headers)
        return resp

    @staticmethod
    def _parse_resource(response: Response) -> typing.Optional[typing.List[TwitterVideo]]:
        """
        Parse the TWDOWN response and extract the download link of the resource
        :param response:
        :return:
        """
        if response.status_code != 200:
            return

        twitter_videos: typing.List[TwitterVideo] = []

        soup = BeautifulSoup(response.text, "html.parser")
        if not (tbody := soup.find("tbody")):
            return twitter_videos
        if trs := tbody.find_all("tr"):
            for tr in trs[:-1]:
                if tds := tr.find_all("td"):
                    quality = tds[1].text
                    download_link = tds[-1].find("a")["href"]
                    twitter_videos.append(TwitterVideo(quality, download_link))

        return twitter_videos

    def _download(self, tv: TwitterVideo) -> typing.Optional[str]:
        """
        parse TwitterVideo and download video to the local folder.
        :param tv:
        :return:
        """
        # path_to_save = ./twdown/username_vid_480x640_uuid.mp4
        flag = urlparse(tv.download_link).path.split("vid/")[-1]
        filename = f"{self._username}_{self._vid}_{flag}".replace("/", "_")
        path_to_save = os.path.join(self._dir_to_save, filename)
        with open(path_to_save, "wb") as file:
            file.write(requests.get(tv.download_link).content)
        return path_to_save

    def run(self):
        try:
            response = self._post_sharelink(sharelink=self._sharelink)
        except ConnectionError:
            return []

        if twitter_videos := self._parse_resource(response):
            twitter_videos = sorted(twitter_videos, key=lambda x: x.quality)
            if self._quality == self.Quality.MAX:
                return [self._download(twitter_videos[-1])]
            if self._quality == self.Quality.MIN:
                return [self._download(twitter_videos[0])]
            if self._quality == self.Quality.ALL:
                return [self._download(tv) for tv in twitter_videos]

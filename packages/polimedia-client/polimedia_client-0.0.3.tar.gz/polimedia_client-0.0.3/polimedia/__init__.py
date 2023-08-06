__version__ = "0.0.3"

import pymongo
import pprint
from datetime import datetime
from loguru import logger
from pathlib import Path
from typing import Optional, List


class PolimediaClient:
    def __init__(self, server="127.0.0.1", user=None, pwd=None, collection="polimedia"):
        auth = ""
        if user and pwd:
            auth = f"{user}:{pwd}@"
        self.client = pymongo.MongoClient(f"mongodb://{auth}{server}")
        self.db = self.client[collection]

    def get_mongo_entry_for_video(self, video_id: str) -> Optional[dict]:
        """
        Given the ID of a video, returns the info stored in the PoliMedia Mongo DB about
        that video.

        :param video_id: Media video id (e.g. ada5974a-cf7b-11ec-854a-fbea444eded3)
        :returns: JSON/dict-like object with information about the video
        """

        filt = {
            "_id": video_id,
            "source.type": "polimedia",
            "$or": [{"deletionDate": {"$exists": False}}, {"deletionDate": None}],
        }
        return self.db.videos.find_one(filt)

    def get_server_for_video(self, video_id: str) -> Optional[str]:
        """
        Given the ID of a video, returns the ID of the TransLectures server where the
        video is replicated.

        :param video_id: Media video id (e.g. ada5974a-cf7b-11ec-854a-fbea444eded3)
        :returns: TransLectures server id (e.g. 3fcea090-3864-11e6-9b2d-5b99e0c45117)
        """
        video_json = self.get_mongo_entry_for_video(video_id)
        try:
            if video_json is None:
                raise Exception
            server_id = video_json["pluginData"]["translectures"]["server"]
        except Exception:
            logger.exception(
                "Couldn't retrieve the TransLectures server corresponding "
                f"to video {video_id}"
            )
            server_id = None
        else:
            logger.info(f"Using server {server_id} for video {video_id}")
        return server_id

    def get_path_for_video(self, video_id: str) -> str:
        """
        Given the ID of a video, returns the path in the Media server where the video
        file can be found.

        :param video_id: Media video id (e.g. ada5974a-cf7b-11ec-854a-fbea444eded3)
        :returns: a local path to the video file (e.g.
            /media/paellaserver/politube/videos/.../presenter.mp4)
        """
        video_json = self.db.videos.find_one({"_id": video_id})
        if video_json is None:
            raise Exception(f"Video {video_id} not found in DB")
        video_name = video_json["source"]["videos"][0]["src"]
        repo_json = self.db.repositories.find_one({"_id": video_json["repository"]})
        if repo_json is None:
            raise Exception(f"Repo {video_json['repository']} not found in DB")
        return f"{repo_json['path']}{video_id}/polimedia/{video_name}"

    def get_configfile_for_video(
        self, video_id: str, config_dir: Path
    ) -> Optional[Path]:
        """
        Given the ID of a video, returns the path to the config file with the API keys
        needed for using the specific TransLectures server where the video is located.

        :param video_id: Media video id (e.g. ada5974a-cf7b-11ec-854a-fbea444eded3)
        :returns: a local path to the config file (e.g.
            /home/encoder/.../3fcea090-3864-11e6-9b2d-5b99e0c45117.ini)
        """
        server_id = self.get_server_for_video(video_id)
        if server_id is None:
            logger.warning(f"Couldn't get TransLectures server for {video_id}")
            config_file = None
        else:
            config_file = config_dir.joinpath(f"{server_id}.ini")
        return config_file

    def register_resegmentation_in_mongo(
        self,
        video_id: str,
        upload_id: str,
        subtitle_list: List[str],
        punctuate: bool,
        punctuation_enabled_langs: list
    ):
        """
        Register some information about the operation performed in the PoliMedia Mongo
        DB. This will include the upload_id and the details of the action (langs
        implied, whether or not automatic punctuation waas applied, etc.)

        :param video_id: Media video id (e.g. ada5974a-cf7b-11ec-854a-fbea444eded3)
        :param upload_id: ID given by TransLectures to identify the uploading subtitles
            operation
        :param subtitle_list: list of subtitles uploaded to TransLectures (just the
            2-letter codes)
        :param punctuate: whether automatic punctuation algorithm was applied or not
        """
        ops = [
            {"lang": lang, "punctuate": punctuate and lang in punctuation_enabled_langs}
            for lang in subtitle_list
        ]
        old_entry = self.get_mongo_entry_for_video(video_id)
        logger.info("Registering operation in Mongo")
        logger.debug(f"The old entry was:\n{pprint.pformat(old_entry)}")

        self.db.videos.update_one(
            {"_id": video_id},
            {
                "$addToSet": {
                    "pluginData.textToSpeech.resegmenter": {
                        "date": datetime.now(),
                        "uploadId": upload_id,
                        "operations": ops,
                    }
                }
            },
        )

        new_entry = self.get_mongo_entry_for_video(video_id)
        logger.debug(f"The new entry is:\n{pprint.pformat(new_entry)}")

    def register_speech_synth(
        self,
        video_id: str,
        upload_id: str,
        langs: List[str],
    ):
        """
        Register a speech synthesis command in the Polimedia Mongo DB. This should
        include the video_id (to select the video object in the DB), the upload_id and
        the list of langs for which the audio is going to be generated.

        :param video_id: Media video id (e.g. ada5974a-cf7b-11ec-854a-fbea444eded3)
        :param upload_id: unique ID returned by TL to track the results of the operation
        :param langs: list of languages (in 2-letter codes) for which we want to obtain
            TTS tracks
        """

        old_entry = self.get_mongo_entry_for_video(video_id)
        logger.debug(f"The old entry was:\n{pprint.pformat(old_entry)}")
        self.db.videos.update_one(
            {"_id": video_id},
            {
                "$addToSet": {
                    "pluginData.textToSpeech.speechSynth": {
                        "date": datetime.now(),
                        "uploadId": upload_id,
                        "actions": [{"lang": lang} for lang in langs]
                    }
                }
            }
        )
        new_entry = self.get_mongo_entry_for_video(video_id)
        logger.debug(f"The new entry is:\n{pprint.pformat(new_entry)}")

    def get_masters_path_for_video(self, video_id: str, master_name: str) -> Path:
        video_json = self.get_mongo_entry_for_video(video_id)
        if video_json is None:
            raise Exception(f"Video {video_id} not found in DB")
        master_repo = video_json["source"]["masters"]["repository"]
        masters_repo_json = self.db.repositories.find_one({"_id": master_repo})
        if masters_repo_json is None:
            raise Exception(f"Master repo {master_repo} not found in DB")
        return Path(f"{masters_repo_json['path']}{video_id}/{master_name}")

    def add_master_video_entry(self, video_id: str, name: str):
        self.db.videos.update_one(
            {"_id": video_id},
            {
                "$set": {
                    "source.masters.files": [
                        {"tag": "presenter/transcode", "name": name}
                    ]
                }
            },
        )

    def get_video_file_url(self, video_json):
        videoId = video_json["_id"]
        repo = video_json["repository"]
        repoinfo = self.db.repositories.find_one({"_id": repo})
        if repoinfo is None:
            raise Exception(f"Could not retrieve info for repository {repo}")
        videoFileURL = (
            repoinfo["server"]
            + repoinfo["endpoint"]
            + videoId
            + "/polimedia/"
            + video_json["source"]["videos"][0]["src"]
        )
        return videoFileURL

    # Channels
    def get_mongo_entry_for_channel(self, channel_id: str) -> Optional[dict]:
        """
        Given the ID of a channel, returns the info stored in the PoliMedia Mongo DB
        about that channel.

        :param channel_id: Channel video id (e.g. e98845a0-0298-11ed-abaa-3f7da180bcf7)
        :returns: JSON/dict-like object with information about the video
        """

        filt = {"_id": channel_id}
        return self.db.videos.find_one(filt)

    def get_channel_videos(self, channel_id, recursion_level=0, max_recursion=5):
        channel_videos = []
        recursion_level += 1
        channel_info = self.db.channels.find_one({"_id": channel_id})
        if not channel_info:
            raise Exception(f"No channel with ID {channel_id} could be found")
        for v in channel_info["videos"]:
            channel_videos.append(v)
        if recursion_level <= max_recursion:
            for c in channel_info["children"]:
                channel_videos += self.get_channel_videos(c, recursion_level)
        return list(set(channel_videos))

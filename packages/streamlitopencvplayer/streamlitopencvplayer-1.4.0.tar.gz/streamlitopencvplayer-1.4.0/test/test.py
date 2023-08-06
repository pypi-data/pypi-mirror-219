"""Test script."""

import argparse
import uuid

import streamlit as st

from streamlitopencvplayer.app import display_video



class opencvplayer:
    """Class streamlit opencv player."""

    def __init__(self, video_path, json_path):
        self.video_path = video_path
        self.json_path = json_path

    def main(self):
        """Test function.

        Args:
            video_path : video file path or video url.
            json_path : Json file path or url.
            alerts (Required when data is used) : List of alerts time
            Json file elements :
                guid (Optional) : unique ID
                timestamp : required just when alerts are used
                messageType (Optional) : message type is it an image(0), Log(1) or an Alert(2)
                containerName (Optional)
                data (Optional) : list of bounding box coordinates, score and class

        Returns:
            The video Player.
        """
        if self.video_path is not None:
            return display_video(self.video_path, self.json_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runnnig...")
    parser.add_argument(
        "--video-path",
        "-V",
        help="Enter the video path",
        default=str(uuid.uuid4().hex),
    )
    parser.add_argument("--json-path",
                        "-J",
                        help="Json file path"
                        )

    args = parser.parse_args()
    opencvplayer = opencvplayer(
        args.video_path, args.json_path)
    opencvplayer.main()

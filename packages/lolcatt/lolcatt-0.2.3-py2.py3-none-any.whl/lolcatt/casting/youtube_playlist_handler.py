#!/usr/bin/env python3
from pathlib import Path
from typing import List

from yt_dlp import YoutubeDL


class YoutubePlaylistHandler:
    def __init__(self, cookies_file: str = None):
        if cookies_file is not None:
            cookies_file = Path(str(cookies_file)).expanduser().resolve()
            if not cookies_file.exists():
                raise ValueError(
                    f'Youtube cookies file "{cookies_file}" does not exist. '
                    'Please check your catt config file.'
                )
        self.ydl = YoutubeDL(
            {
                'cookiefile': str(cookies_file),
                'skip_download': True,
                'quiet': True,
                'ignoreerrors': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
            }
        )

    @staticmethod
    def _get_ids_from_ytdl_json(ytdl_json: dict) -> List[str]:
        return [item['id'] for item in ytdl_json['entries']]

    def resolve_playlist(self, s: str) -> List[str]:
        """
        Resolve a playlist into a list of video URLs.
        """
        try:
            ids = self._get_ids_from_ytdl_json(self.ydl.extract_info(s, download=False))
            return [f'https://www.youtube.com/watch?v={id_}' for id_ in ids]
        except TypeError:
            return []

# models.py - Friday, February 25, 2022

import logging, os, time
from dataclasses import dataclass, fields, field
from datetime import datetime, timedelta
from enum import Enum, auto
# from faker import Faker
from random import choice, shuffle, uniform
from typing import List
from yt_dlp import DateRange, parseOpts, YoutubeDL
from config import Config


class CustomLogRecord(logging.LogRecord):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.nameProcess = f"{self.name}[{self.process}]{self.thread}"
		self.nameProcessThread = f"{self.name}[{self.process}]{self.threadName}"


class SearchType(Enum):
	user = auto()
	channel = auto()
	playlist = auto()


@dataclass(order=True)
class VideoDataItem:
	"""
	duration, extractor, video_id, url, info_dict, json_filename, ydl_opts
	"""
	duration:       float
	extractor:      str
	video_id:       str
	url:            str
	info_dict:      dict
	json_filename:  str
	ydl_opts:       dict
	nsfw:           bool = False

	def download(self):
		# Debugging
		if "outtmpl" in self.ydl_opts:
			foo = self.ydl_opts["outtmpl"]
			print(foo)
		start_ts = time.time()
		self.video_filename = YoutubeDL(self.ydl_opts).prepare_filename(self.info_dict)
		result = YoutubeDL(self.ydl_opts).download_with_info_file(self.json_filename)
		stop_ts = time.time()
		self.download_time = stop_ts - start_ts
		part_filename = self.video_filename + '.part'
		if os.path.exists(self.video_filename):
			self.complete = True
			self.filesize = os.path.getsize(self.video_filename)
		elif os.path.exists(part_filename):
			self.complete = False
			self.filesize = os.path.getsize(part_filename)
		return {'filename':      self.video_filename,
		        'download_time': self.download_time,
		        'filesize':      self.filesize
		        }


	def __post_init__(self):
		self.download_time = -1
		self.complete = False
		self.video_filename = None
		self.filesize = -1


	def __str__(self):
		return f"{self.url}"


@dataclass
class VideoData:
	items: List[VideoDataItem] = field(default_factory=list)


def default_ydl_opts():
	parser, opts, args2 = parseOpts()
	return {
		'dateafter': DateRange((datetime.now() - timedelta(days=2)).strftime('%Y%m%d')),
		'download_archive': opts.download_archive,
		'forcefilename': True,
		'format': opts.format,
		'ignoreerrors': True,
		# 'logger': ydl_logger,
		'max_downloads': opts.max_downloads,
		'max_filesize': opts.max_filesize,
		'max_sleep_interval': 7.7777,
		'noprogress': True,
		'no_warnings': True,
		'outtmpl': os.path.expanduser(opts.outtmpl) if opts.outtmpl is not None else opts.outtmpl,
		'playlistend': opts.playlistend,
		'quiet': True,
		'ratelimit': opts.ratelimit,
		'rejecttitle': opts.rejecttitle,
		'restrictfilenames': True,
		'sleep_interval': 3.3333,
		# 'useragent': _my_browser,
		'writeinfojson': False,
	}


if __name__ == '__main__':
	# fake = Faker()
	platforms = ['rumble.com', 'youtube.com', 'youtu.be', 'bitchute.com', 'twitter.com', 'foxnews.com']
	shuffle(platforms)
	video_items = VideoData().items
	"""for i in range(1,11):
		duration = uniform(20,1000)
		extractor = 'extractor_%2d' % i
		platform = choice(platforms)
		username = fake.user_name()
		video_id = fake.pystr_format("############")
		url = f"https://{platform}/{username}/{video_id}"
		info_dict = fake.pydict()
		json_filename = f"{extractor}_{video_id}.info.json"
		ydl_opts = default_ydl_opts()
		video_item = VideoDataItem(duration, extractor, video_id, url, info_dict, json_filename, ydl_opts, )
		video_items.append(video_item)"""
	# print(video_info.ydl_opts)
	# videos = [video_info for x in range(3)]
	# videos.append(video_info)
	for i, v in enumerate(sorted(video_items)):
		print(f"{i + 1:2d} {v.duration:.2f} {v.url}")



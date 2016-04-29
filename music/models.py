# from __future__ import unicode_literals

from django.db import models
# Create your models here.
import os
import mytool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_ROOT = os.path.join(BASE_DIR, 'music')



class MusicChart(models.Model):

	def plot_all_artists(self):
		x_bin_files = [
			"x_day_list_play.bin", 
			"x_day_list_download.bin",
			"x_day_list_collect.bin"]

		y_bin_files = [
			"y_plays_list_play.bin",
			"y_plays_list_download.bin",
			"y_plays_list_collect.bin"]

		image_paths = [
			"/static/images/all_artists_chart_play.png",
			"/static/images/all_artists_chart_download.png",
			"/static/images/all_artists_chart_collect.png"]

		xlabel = [
			"days", "days", "days"
		]

		ylabel = [
			"plays", "downloads", "collects"
		]

		title = [
			"plays of 50 artists", "downloads of 50 artists", "collects of 50 artists"
		]

		for i in range(len(image_paths)):
			if os.path.isfile(MUSIC_ROOT + image_paths[i]) != True:
				# print "Not existed."

				self.plot_all(x_bin_files[i], y_bin_files[i], image_paths[i],
					xlabel[i], ylabel[i], title[i])

		return image_paths


	def plot_all(self, x_file, y_file, save_path, xlabel, ylabel, title):
		x_day_list = mytool.load(MUSIC_ROOT + "/data_bin/" + x_file)
		y_list = mytool.load(MUSIC_ROOT + "/data_bin/" + y_file)

		if os.path.isfile(MUSIC_ROOT + save_path) != True:
			print save_path, "\tNot existed."
			mytool.plot_multi_lines(x_day_list, y_list, MUSIC_ROOT + save_path,
				xlabel, ylabel, title)


	def search_an_artist(self, artists_id):
		image_path = "/static/images/person/" + artists_id + ".png"
		if os.path.isfile(MUSIC_ROOT + image_path):
			return image_path

		artist_newid_map = mytool.load(MUSIC_ROOT + "/data_bin/artist_newid_map.bin")
		if artists_id not in artist_newid_map:
			return "/static/images/404.png"

		day_to_num = mytool.load(MUSIC_ROOT + "/data_bin/day_to_num.bin")
		

		newid_action_map_name = [
			"newid_plays_map.bin", 
			"newid_downloads_map.bin", 
			"newid_collects_map.bin"]

		xlist = []
		ylist = []
		for i in range(len(newid_action_map_name)):
			x, y = self.search(artists_id, day_to_num, artist_newid_map, newid_action_map_name[i])
			xlist.append(x)
			ylist.append(y)

		mytool.plot_multi_lines(xlist, ylist, MUSIC_ROOT + image_path,
			"days", "amount", "actions of the artist: " + artists_id)
		return image_path



	def search(self, artists_id, day_to_num, artist_newid_map, map_name):
		newid_action_map = mytool.load(MUSIC_ROOT + "/data_bin/" + map_name)
		days_to_action = newid_action_map[artist_newid_map[artists_id]]

		x = []
		y = []
		cnt = 0
		for day in days_to_action:
			day_cnt = day_to_num[day[0]]
			while cnt != day_cnt:
				x.append(cnt)
				y.append(0)
				cnt += 1
			cnt += 1

			x.append(day_cnt)
			y.append(day[1])

		return x, y
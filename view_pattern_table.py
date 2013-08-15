"""Script to view the pattern table of an NES ROM

   usage: view_pattern_table.py <filename>

By Jake Vanderplas, 2013 <http://jakevdp.github.com>
License: GPL.
Feel free to use and distribute, but keep this attribution intact.
"""
import zipfile
import numpy as np
from matplotlib import pyplot as plt


class ROMViewer(object):
	"""Visually inspect an NES ROM"""
	def __init__(self, filename, N1=16, N2=16, sep=1):
		extension = filename.split('.')[1]
		bits = 8
		if(extension == 'smc'):
			bits = 16
			N1 = 8
			N2 =8
		elif(extension == 'nes'):
			bits = 8

		if zipfile.is_zipfile(filename):
			zp = zipfile.ZipFile(filename)
			data = np.unpackbits(np.frombuffer(zp.read(zp.filelist[0]),
											   dtype=np.uint8))
		else:
			data = np.unpackbits(np.fromfile(filename, dtype=np.uint8))

		self.bits = bits
		self.data = data.reshape((-1, bits, bits))
		self.N1 = N1
		self.N2 = N2
		self.sep = sep

		self.fig, self.ax = plt.subplots(figsize=(6, 6),
										 subplot_kw=dict(xticks=[], yticks=[]))
		self.fig.subplots_adjust(bottom=0.04, top=0.94, left=0.05, right=0.95)
		self.fig.rom_viewer = self  # needed for object persistence
		self.update_offset(0)
		self.fig.canvas.mpl_connect('key_press_event', self.key_press)

	def update_offset(self, offset):
		"""update offset and re-draw figure"""
		offset = max(offset, 0)
		offset = min(offset, self.data.shape[0] / 2 - self.N1 * self.N2)
		self.current_offset = offset
		self.ax.set_title('offset = %i' % offset)

		# starting at offset, take 128-bit chunks and view as
		# 2-bit 8x8 thumbnails in an 8x8 grid
		im_array = np.zeros((self.sep + self.N1 * (self.bits + self.sep),
							 self.sep + self.N2 * (self.bits + self.sep)))

		for i in range(self.N1):
			for j in range(self.N2):
				thumb = self.data[2 * offset] + 2 * self.data[2 * offset + 1]
				ind_i = self.sep + (self.bits + self.sep) * i
				ind_j = self.sep + (self.bits + self.sep) * j
				im_array[ind_i:ind_i + self.bits, ind_j:ind_j + self.bits] = thumb
				offset += 1

		if not hasattr(self, 'im'):
			self.im = self.ax.imshow(im_array, cmap=plt.cm.binary,
									 interpolation='nearest')
		else:
			self.im.set_data(im_array)
			plt.draw()

	def key_press(self, event):
		"""Use arrow keys to navigate"""
		offset_dict = dict(right=1, left=-1,
						   up=-self.N1 * self.N2,
						   down=self.N1 * self.N2,
						   home=-self.data.shape[0],
						   end=self.data.shape[0])

		if event.key in offset_dict:
			self.update_offset(self.current_offset + offset_dict[event.key])


if __name__ == '__main__':
	import sys
	try:
		filename = sys.argv[1]
	except:
		print __doc__
		sys.exit(0)

	ROMViewer(filename)
	plt.show()

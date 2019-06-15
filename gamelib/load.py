import pygame
from pathlib import Path


def load_images(folder):
	""" Load images from folder as pygame images and saves them to a dict
	:param folder: Path of images to load
	:returns: Returns a dict of images loaded with pygame
	"""
	return_img = {}

	for file in folder.iterdir():
		# img_path = os.path.join(folder, file)
		if file.suffix:
			# print(f"File: {str(file)}")
			# print(f"Type: {type(file)}")
			try:
				return_img[file.name] = pygame.image.load(str(file)).convert_alpha()
			except:
				# print(f'Failed load {file}')
				# return_img[file.name] = file
				pass
		else:
			return_img[file.name] = load_images(file)

	return return_img


# main

def main():
	pygame.display.init()
	eg_folder = Path.cwd().joinpath('test')
	print(load_images(eg_folder))


if __name__ == '__main__':
	main()
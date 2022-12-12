from drivers.heur_target_finder.extract_target_from_url import *
from drivers.heur_target_finder.extract_target_from_image import *


def target_driver(url_id,url):


	print(f"Checking URL {url}")


	url_string_target=get_target_from_url(url_id,url)
	#print(url_string_target)
	image_target=get_target_from_image(url_id,url)
	#print(image_target)
	if(url_string_target==image_target):
		target=image_target
		confidence="4 (Very High)"
	else:
		if(str(image_target)=="None"):
			target=url_string_target
			confidence="2 (Medium)"
		else:
			target=image_target
			confidence="3 (High)"
	if str(target)=="None":
		print(f"Could not find the target that URL {url} is imitating")

	else:

		print(f"URL {url} is imitating {target} with confidence score:{confidence}")

	return target,confidence

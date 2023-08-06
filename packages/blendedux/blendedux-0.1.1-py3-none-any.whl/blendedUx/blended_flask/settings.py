import os
STATIC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
blended_static_dir = STATIC_DIR
# "" #user can modified it as per there choice
CSS_DIRECTORY = os.path.join(STATIC_DIR, "css")
IMAGE_CACHE_DIR = os.path.join(STATIC_DIR, "media")
COMPILE_DIR = os.path.join(CSS_DIRECTORY, "blended")

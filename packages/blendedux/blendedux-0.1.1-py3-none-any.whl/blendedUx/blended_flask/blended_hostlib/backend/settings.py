SRC = "src"
LIB = "lib"
INDEX_JSON = "_index.json"
PROJECT_JSON = "_package.json"
DEFAULT_ALIAS = "parent"
USER_RC = ".userrc"
PACKAGE_LIST_RC = ".packagelistrc"
CANONICAL_TXT = "canonical.txt"
HASH_TXT = ".hash.txt"
ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png']

RESTRICT_IMAGE_TYPE = ['.bmp', '.gif', '.tiff',
                       '.tif', '.ico', '.webp',
                       '.otf', '.eot', '.ttf',
                       '.woff', '.woff2']

# As below type is restricted on HUB. So I am doing this changes.
#ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.bmp', '.gif',
#                       '.png', '.ico', '.webp',
#                       '.otf', '.eot', '.svg', '.ttf',
#                       '.woff', '.woff2']
#RESTRICT_IMAGE_TYPE = ['.tif', '.tiff']

IGNORE_EXTENSIONS = ('.swp', '.db', '~')
IGNORE_PREFIXES = (".", "_")

ALLOWED_FILE_TYPES = ['.html', '.css', '.bd', '.js', '.json', '.svg', '.txt']

CACHE_DICT = {}

BLENDED_ACCOUNT = 'blended'
BLENDED_BASIC = 'basic'

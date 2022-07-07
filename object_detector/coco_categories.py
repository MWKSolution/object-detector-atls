"""Get coco categories from annotations. Save in coco_categories.json for further use."""
import json
from os import path

PATH = path.dirname(__file__)


class CocoCategoriesError(Exception):
    pass


def get_categories():
    """Get coco categories as dict. File: 'annotations/coco_categories.json' must be present.
    If not, run this scrip directly to create one."""
    try:
        with open(PATH + '/annotations/coco_categories.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise CocoCategoriesError('COCO categories json file is missing.') from None
    except json.decoder.JSONDecodeError as e:
        raise CocoCategoriesError('COCO categories json file is corrupted.') from None


if __name__ == '__main__':
    # Get coco categories from annotations. Save in coco_categories.json for further use.
    print("""If this doesn't work:
    1. Download: > http://images.cocodataset.org/annotations/annotations_trainval2017.zip < ,
    2. From zip file copy: > instances_val2017.json < to annotations directory ,
    3. Run this again.""")
    with open(PATH + '/annotations/instances_val2017.json', 'r') as annotations:
        annotations_json = json.load(annotations)

    CATEGORIES = annotations_json['categories']

    with open(PATH + '/annotations/coco_categories.json', 'w') as coco:
        json.dump(CATEGORIES, coco)

    # Show coco categories
    print('COCO categories: ', json.dumps(get_categories(), indent=True))

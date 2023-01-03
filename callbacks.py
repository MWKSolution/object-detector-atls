from dash.dependencies import Input, Output, State
from object_detector import ImageError
from layouts import get_image_src
import base64
import io
from PIL import Image


def get_callbacks(app, detector):

    # load image callback
    @app.callback([Output('upload-data', 'contents'),
                   Output('load-info', 'is_open'),
                   Output('load-info-text', 'children'),
                   Output('image', 'src')],
                  Input('upload-data', 'contents'),
                  State('upload-data', 'filename'))
    def upload_data(content, filename):
        src = None
        if content:
            content_type, content_data = content.split(',')
            if content_type == 'data:image/jpeg;base64':
                # check if image is JPEG, show it and save as input.jpg
                img = base64.b64decode(content_data)
                image = Image.open(io.BytesIO(img))
                image.save('object_detector/images/input.jpg')
                src = f'data:image/jpg;base64,{content_data}'
                return None, False, None, src
            else:
                return None, True, 'This should be JPEG file!', None

    # detect objects callback
    @app.callback([Output('image', 'src'),
                   Output('loading', 'children'),
                   Output('load-info', 'is_open'),
                   Output('load-info-text', 'children')],
                  Input('detect-button', 'n_clicks'))
    def detect_objects(n_clicks):
        src = None
        if n_clicks > 0:
            try:
                # load input.jpg to detector
                detector.load_image('object_detector/images/input.jpg')
            except ImageError as e:
                return None, None, True, 'Load JPEG file first!'
            # detect objects
            result = detector.run_detection()
            # add bounding boxes to image, save it as result.jpg
            detector.get_result_image('object_detector/images/result.jpg')
            # and show it
            src = get_image_src('object_detector/images/result.jpg')
            return src, None, False, None

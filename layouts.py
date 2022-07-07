"""Layouts definitions for Dash app."""
from dash import html, dcc
import dash_bootstrap_components as dbc
import base64

load_indicator = dbc.Spinner(html.Div(id='loading'),
                             spinner_style={'width': '3rem', 'height': '3rem'},
                             fullscreen=False,
                             color='danger')
load_info = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle('Image loader')),
    dbc.ModalBody(dbc.Alert('', id='load-info-text', color='danger'))],
    id='load-info',
    scrollable=False,
    centered=True,
    is_open=False)

detect_button = dbc.Button(
    children=['Detect', load_indicator],
    size='lg',
    n_clicks=0,
    color='primary',
    id='detect-button',
    className='p-4 m-4')

upload = dcc.Upload(['Drag and Drop or select JPEG file'],
                    style={
                        'width'       : '90%',
                        'height'      : '150px',
                        'lineHeight'  : '140px',
                        'borderWidth' : '2px',
                        'borderStyle' : 'dashed',
                        'borderRadius': '10px',
                        'textAlign'   : 'center'},
                    id='upload-data',
                    multiple=False,
                    className='m-3')


def get_image_src(image_path):
    """Get image source from jpg file. Path to file is an argument."""
    encoded = base64.b64encode(open(image_path, 'rb').read())
    src = f'data:image/jpg;base64,{encoded.decode()}'
    return src


image = html.Div([html.Img(src=None, id='image', style={'width': '60vw'})],
                 style={'textAlign': 'center'},
                 className='mt-3')

main_layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div([upload, load_info, detect_button], className="d-grid gap-2"), width=2),
        dbc.Col([image], width=10)])])

nav_bar = dbc.NavbarSimple(
    brand='Object detection JPEG: CARS (cars, trucks, buses)',
    color='primary',
    dark=True)

app_layout = html.Div([nav_bar,
                       main_layout])

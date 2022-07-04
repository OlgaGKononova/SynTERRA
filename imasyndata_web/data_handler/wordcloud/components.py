from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

import dash_html_components as html
import dash_core_components as dcc

import cv2
import base64


def generate_image(text):
    if not text:
        return ""

    wordcloud = WordCloud(max_font_size=200,
                          width=1000, height=500,
                          background_color="#f2f2f2",
                          colormap="inferno",
                          max_words=5000).generate(" ".join(text))

    img = cv2.cvtColor(wordcloud.to_array(), cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.png', img)

    return html.Div([html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(buffer).decode('utf-8')),
                              style={"max-width": "100%",
                                     "height": "auto",
                                     "border-radius": "5%",
                                     "display": "block",
                                     "margin-left": "auto",
                                     "margin-right": "auto",
                                     "margin-top": "30px"
                                     })])
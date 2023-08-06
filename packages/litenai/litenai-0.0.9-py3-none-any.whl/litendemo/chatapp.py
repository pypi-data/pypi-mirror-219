
import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np

import liten as ten

from litendemo import DemoFiles

class ChatApp():
    def start(self):
        """
        Start chat app
        """
        pn.extension(design='material')
        session = ten.Session.get_or_create('liten')
        demofiles = DemoFiles(session.spark)
        demofiles.init()
        chatbot = ten.ChatBot(session)
        chat_panel = chatbot.start()
        chat_panel.servable()

ChatApp().start()

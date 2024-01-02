# author: WxlPtt

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
# copy the link.
from kivy.core.clipboard import Clipboard
from filestack import Client

import time
import webbrowser

Builder.load_file('kivy_files/frontend.kv')


class CameraScreen(Screen):

    # Other method to open and close camera:
    # One button.
    # In kivy file, Button: on_press: root.start() if root.ids.camera.play == False else root.close()
    def open_camera(self):
        """Open camera. It is used in kivy file. files/frontend.kv
        :return:
        """
        # The default of camera is closed.
        self.ids.camera.play = True
        self.ids.open_close_camera.text = "Close Camera"
        # set back to default set.
        # self.ids.camera.texture = self.ids.camera._camera.texture
        self.ids.camera.opacity = 1

    def close_camera(self):
        """Close camera. It is used in kivy file. files/frontend.kv
        :return:
        """
        # Close camera
        self.ids.camera.play = False
        self.ids.open_close_camera.text = "Open Camera"
        self.ids.camera.texture = None
        self.ids.camera.opacity = 0

    def capture_camera(self):
        """
        Capture a photo.
        Generate a png file in Capture_images directory.
        Move to Image_Screen
        :return:
        """
        # Get current time as the file name.
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.file_name = 'Capture_images/' + current_time + ".png"
        # self.ids.camera.export_as_image()
        self.ids.camera.export_to_png(self.file_name)
        self.manager.current = 'image_screen'
        # Move to Image_Screen
        self.manager.current_screen.ids.camera_captured.source = self.file_name


class ImageScreen(Screen):

    def capture_again(self):
        """
        Back to Camera_Screen, and capture it again.
        :return:
        """
        self.manager.current = 'camera_screen'

    def create_link(self):
        """
        1. Get the file path.
        2. Share it to filestack, which is a package that import filestack
        3. Use an apikey to get an access of the filestack.
        4. Upload the file, and insert a url to the Image_Screen's label.
        :return:
        """

        # 1. Get the file path.
        file_path = App.get_running_app().root.ids.camera_screen.file_name

        # 2. Share it to filestack, which is a package that import filestack
        # 3. Use an apikey to get an access of the filestack.
        client = Client(apikey="AjIyQQo9kQfWEOlRRMUoIz")

        # 4. Upload the file, and insert a url to the Image_Screen's label.
        self.file_link = client.upload(filepath=file_path).url
        # file_link not a string. so file_link.url will output the address.
        self.manager.current_screen.ids.file_link.text = self.file_link

    def copy_link(self):
        """
        Copy link to the clipboard available for pasting.
        :return:
        """
        try:
            Clipboard.copy(self.file_link)
        except:
            self.manager.current_screen.ids.file_link.text = 'Please create a photo link first.'

    def open_link(self):
        """
        Open link with default browser.
        :return:
        """
        try:
            webbrowser.open(self.file_link)
        except:
            self.manager.current_screen.ids.file_link.text = 'Please create a photo link first.'


class RootWidget(ScreenManager):
    """
    a part of kivy package, set root widget
    """
    pass


class MainApp(App):
    """
    Inherit App, a part of kivy package.
    """

    def build(self):
        return RootWidget()

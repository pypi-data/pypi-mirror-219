import os
import shutil
from mkdocs.plugins import BasePlugin


class MaterialVALighthousePlugin(BasePlugin):

    def __init__(self):
        self.enabled = True

    def on_pre_build(self, config):
        self.copy_over_css()
        self.copy_over_logo()

        return config

    @staticmethod
    def copy_over_logo():
        os.makedirs("docs/assets/images", exist_ok=True)
        logo_src_path = os.path.join(os.path.dirname(__file__), "va_lighthouse_logo.png")
        logo_dst_path = "docs/assets/images/va_lighthouse_logo.png"
        shutil.copyfile(logo_src_path, logo_dst_path)

    @staticmethod
    def copy_over_css():
        os.makedirs("docs/assets/stylesheets", exist_ok=True)
        extra_css_path = "docs/assets/stylesheets/va_lighthouse.css"
        custom_css_path = os.path.join(os.path.dirname(__file__), "va_lighthouse.css")
        shutil.copyfile(custom_css_path, extra_css_path)

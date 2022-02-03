import gi
import pycurl
import certifi
import json
from io import BytesIO

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Request:
    def get(self, url) -> dict:
        buffer = BytesIO()

        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.CAINFO, certifi.where())
        c.perform()

        time = c.getinfo(c.TOTAL_TIME)
        status_code = c.getinfo(c.HTTP_CODE)
        c.close()

        data = buffer.getvalue().decode("iso-8859-1")
        try:
            data = json.dumps(json.loads(data), indent=4)
        except Exception as e:
            raise e

        return {
            'url': url,
            'method': 'GET',
            'time': time,
            'status_code': status_code,
            'response': str(data)
        }


class MyWindow(object):
    __gtype_name__ = "window1"

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("layout-glade.glade")
        self.builder.connect_signals(self)

    def run(self, *args):
        self.builder.get_object("window1").show()
        Gtk.main()

    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_entry_press_enter(self, widget, event):
        # if event.keyval == 13:
        if event.keyval in [13, 65293]:
            btn_send = self.builder.get_object("btn_send_url")
            btn_send.set_label("Sending...")
            rs = Request().get(widget.get_text())
            btn_send.set_label("Send")

            h = self.builder.get_object("history_data")
            h.append(None, [
                rs["url"],
                rs["time"],
                rs["method"],
                rs["status_code"]
            ])

            id_response = self.builder.get_object("id_text_results")
            textbuffer = id_response.get_buffer()
            textbuffer.set_text(rs["response"])

            # This work for add text to the last line
            # textbuffer = id_response.get_buffer()
            # start_iter = textbuffer.get_start_iter()
            # textbuffer.insert(start_iter, rs["response"])


MyWindow().run()

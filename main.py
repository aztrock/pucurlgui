import gi
import pycurl

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Request:
    def get(self, url) -> dict:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.perform()

        # print(c)  # DATA
        # print (c.getinfo(c.HTTP_CODE), c.getinfo(c.EFFECTIVE_URL))
        # print ("time taken:", c.getinfo(c.TOTAL_TIME))

        time = c.getinfo(c.TOTAL_TIME)
        status_code = c.getinfo(c.HTTP_CODE)
        c.close()
        return {
            'url': url,
            'method': 'GET',
            'time': time,
            'status_code': status_code
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



MyWindow().run()

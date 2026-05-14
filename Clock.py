from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from datetime import datetime, timezone, timedelta

Window.clearcolor = (0.06, 0.08, 0.12, 1)

# Madagascar UTC+3
MADA = timezone(timedelta(hours=3))

SESSIONS = {
    "Sydney": (22, 7),
    "Tokyo": (0, 9),
    "London": (8, 17),
    "New York": (13, 22),
}

class TradingClockApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.time_label = Label(text="", font_size='48sp', bold=True, color=(1,1,1,1))
        self.date_label = Label(text="", font_size='20sp', color=(0.7,0.8,1))
        self.root.add_widget(self.time_label)
        self.root.add_widget(self.date_label)

        self.session_labels = {}
        for name in SESSIONS:
            lbl = Label(text="", font_size='22sp', halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            self.session_labels[name] = lbl
            self.root.add_widget(lbl)

        Clock.schedule_interval(self.update, 1)
        self.update(0)
        return self.root

    def update(self, dt):
        now_mada = datetime.now(MADA)
        self.time_label.text = now_mada.strftime("%H:%M:%S")
        self.date_label.text = now_mada.strftime("Antananarivo • %A %d %B %Y")

        now_utc = datetime.now(timezone.utc)
        utc_hour = now_utc.hour + now_utc.minute/60

        for name, (open_h, close_h) in SESSIONS.items():
            if open_h < close_h:
                open_now = open_h <= utc_hour < close_h
            else:
                open_now = utc_hour >= open_h or utc_hour < close_h

            status = "OPEN" if open_now else "CLOSED"
            color = "[color=00ff88]" if open_now else "[color=ff5555]"
            self.session_labels[name].markup = True
            self.session_labels[name].text = f"{color}{name:9} {status}[/color] ({open_h:02d}:00 - {close_h:02d}:00 UTC)"

if __name__ == "__main__":
    TradingClockApp().run()

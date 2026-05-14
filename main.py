
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from datetime import datetime, timezone, timedelta

EAT = timezone(timedelta(hours=3))
UTC = timezone.utc
SESSIONS = {"Sydney":(21,6),"Tokyo":(0,9),"London":(7,16),"New York":(13,22)}

def ouverte(d,f,h): 
    return (d<=h<f) if d<f else (h>=d or h<f)

class TradingClock(BoxLayout):
    def __init__(self,**kw):
        super().__init__(orientation='vertical', padding=30, spacing=20, **kw)
        self.lbl_tana = Label(text="TANA --:--:--", font_size='64sp', bold=True, color=(0,1,0,1))
        self.lbl_utc = Label(text="UTC --:--:--", font_size='36sp')
        self.lbl_sess = Label(text="Sessions", font_size='28sp')
        self.add_widget(self.lbl_tana)
        self.add_widget(self.lbl_utc)
        self.add_widget(self.lbl_sess)
        Clock.schedule_interval(self.update,1)

    def update(self,dt):
        now_utc = datetime.now(UTC)
        now_eat = now_utc.astimezone(EAT)
        h = now_utc.hour + now_utc.minute/60
        ouv = [n for n,(d,f) in SESSIONS.items() if ouverte(d,f,h)]
        self.lbl_tana.text = f"TANA {now_eat.strftime('%H:%M:%S')}"
        self.lbl_utc.text = f"UTC {now_utc.strftime('%H:%M:%S')}"
        self.lbl_sess.text = " | ".join(ouv) if ouv else "fermé"

class TradingClockApp(App):
    def build(self): 
        return TradingClock()

if __name__ == '__main__':
    TradingClockApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from mutagen.mp3 import MP3
import os
import time

class MP3Player(BoxLayout):
    def __init__(self, **kwargs):
        super(MP3Player, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.songs = []
        self.current_song = None
        self.is_paused = False

        self.recycle_view = RecycleView()
        self.recycle_view.data = [{'text': ''}]  # Initialize with empty data
        self.add_widget(self.recycle_view)

        self.status_bar = Label(text="", size_hint_y=None, height=40)
        self.add_widget(self.status_bar)

        controframe = BoxLayout(size_hint_y=None, height=50)
        self.add_widget(controframe)

        self.play_btn = Button(text='Play', on_press=self.play)
        self.pause_btn = Button(text='Pause', on_press=lambda x: self.pause(self.is_paused))
        self.forward_btn = Button(text='Next', on_press=self.forward)
        self.reverse_btn = Button(text='Previous', on_press=self.reverse)

        controframe.add_widget(self.reverse_btn)
        controframe.add_widget(self.play_btn)
        controframe.add_widget(self.pause_btn)
        controframe.add_widget(self.forward_btn)

        self.add_song_menu = Button(text='Add Songs', on_press=self.add_song)
        self.add_widget(self.add_song_menu)

        Clock.schedule_interval(self.check_music_status, 0.1)

    def play_time(self):
        current_time = SoundLoader.get(self.current_song).get_pos()
        current_time_converter = time.strftime("%H:%M:%S", time.gmtime(current_time))
        song_length = MP3(self.current_song).info.length
        song_length_converted = time.strftime("%H:%M:%S", time.gmtime(song_length))
        self.status_bar.text = f"time elapsed {current_time_converter}/{song_length_converted}"

    def add_song(self, instance):
        chooser = FileChooserIconView()
        chooser.bind(on_submit=self.load_song)
        self.add_widget(chooser)

    def load_song(self, instance, selection, touch):
        if selection:
            song = selection[0]
            song_name = os.path.basename(song).replace(".mp3", "")
            self.songs.append(song_name)
            self.recycle_view.data = [{'text': song_name} for song_name in self.songs]
            self.remove_widget(instance)

    def play(self, instance):
        if self.recycle_view.data:
            selected_index = self.recycle_view.adapter.get_data().index(self.recycle_view.data[self.recycle_view.index])
            self.current_song = self.songs[selected_index]
            self.current_song = f"D:/software projects/mp3 player/songs/{self.current_song}.mp3"
            SoundLoader.load(self.current_song).play()
            self.is_paused = False
            Clock.schedule_interval(lambda dt: self.play_time(), 1)

    def forward(self, instance):
        next_one = self.recycle_view.index + 1
        if next_one < len(self.songs):
            self.recycle_view.index = next_one
            self.play(instance)

    def reverse(self, instance):
        next_one = self.recycle_view.index - 1
        if next_one >= 0:
            self.recycle_view.index = next_one
            self.play(instance)

    def pause(self, is_paused):
        self.is_paused = not is_paused
        if self.is_paused:
            SoundLoader.get(self.current_song).stop()
        else:
            SoundLoader.get(self.current_song).play()

    def check_music_status(self, dt):
        if not self.is_paused and self.current_song and SoundLoader.get(self.current_song).state == 'stop':
            self.on_song_end()

    def on_song_end(self):
        next_one = self.recycle_view.index + 1
        if next_one < len(self.songs):
            self.recycle_view.index = next_one
            self.play(None)
        else:
            self.recycle_view.index = 0

class MyApp(App):
    def build(self):
        return MP3Player()

if __name__ == '__main__':
    MyApp().run()

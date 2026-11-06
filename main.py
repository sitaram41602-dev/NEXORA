
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
import os

Window.clearcolor = (0.06, 0.01, 0.12, 1)
PURPLE = (0.5, 0.1, 0.9, 1)

class NexoraApp(App):

    def build(self):
        self.sm = ScreenManager()
        self.sound = None

        self.home()
        self.calculator()
        self.notes()
        self.profile()
        self.settings()
        self.music()

        return self.sm

    def button(self, text, action):
        b = Button(
            text=text,
            font_size=18,
            background_normal="",
            background_color=PURPLE,
            size_hint_y=None,
            height=55
        )
        b.bind(on_release=action)
        return b

    def back(self, layout):
        layout.add_widget(
            self.button(
                "BACK HOME",
                lambda x: setattr(
                    self.sm, "current", "home"
                )
            )
        )

    def home(self):
        s = Screen(name="home")
        layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=12
        )

        title = Label(
            text="[b]N E X O R A[/b]",
            markup=True,
            font_size=38,
            color=(0.7, 0.2, 1, 1)
        )

        anim = (
            Animation(color=(1, 0.3, 1, 1), duration=1.2)
            + Animation(color=(0.4, 0.1, 1, 1), duration=1.2)
        )
        anim.repeat = True
        anim.start(title)

        layout.add_widget(title)
        layout.add_widget(Label(
            text="WELCOME TO YOUR WORLD",
            font_size=17
        ))

        for name in [
            "Calculator", "Notes", "Music Player",
            "Profile", "Settings"
        ]:
            screen_name = name.lower().replace(" ", "_")
            layout.add_widget(
                self.button(
                    name,
                    lambda x, n=screen_name:
                    setattr(self.sm, "current", n)
                )
            )

        s.add_widget(layout)
        self.sm.add_widget(s)

    def calculator(self):
        s = Screen(name="calculator")
        layout = BoxLayout(
            orientation="vertical", padding=20, spacing=10
        )

        layout.add_widget(Label(text="CALCULATOR", font_size=28))

        a = TextInput(hint_text="First number", multiline=False)
        b = TextInput(hint_text="Second number", multiline=False)
        result = Label(text="Result:", font_size=24)

        layout.add_widget(a)
        layout.add_widget(b)

        def calculate(op):
            try:
                x, y = float(a.text), float(b.text)

                if op == "+":
                    ans = x + y
                elif op == "-":
                    ans = x - y
                elif op == "*":
                    ans = x * y
                else:
                    if y == 0:
                        result.text = "Cannot divide by zero"
                        return
                    ans = x / y

                result.text = "Result: " + str(ans)

            except ValueError:
                result.text = "Enter valid numbers"

        for op in ["+", "-", "*", "/"]:
            layout.add_widget(
                self.button(op, lambda x, o=op: calculate(o))
            )

        layout.add_widget(result)
        self.back(layout)
        s.add_widget(layout)
        self.sm.add_widget(s)

    def notes(self):
        s = Screen(name="notes")
        layout = BoxLayout(
            orientation="vertical", padding=20, spacing=12
        )

        layout.add_widget(Label(text="MY NOTES", font_size=28))
        note = TextInput(
            hint_text="Write your notes...",
            multiline=True
        )

        path = os.path.join(self.user_data_dir, "notes.txt")

        try:
            with open(path, "r", encoding="utf-8") as f:
                note.text = f.read()
        except FileNotFoundError:
            pass

        status = Label(text="")

        def save(instance):
            with open(path, "w", encoding="utf-8") as f:
                f.write(note.text)
            status.text = "NOTES SAVED!"

        layout.add_widget(note)
        layout.add_widget(self.button("SAVE NOTES", save))
        layout.add_widget(status)
        self.back(layout)

        s.add_widget(layout)
        self.sm.add_widget(s)

    def music(self):
        s = Screen(name="music_player")
        layout = BoxLayout(
            orientation="vertical", padding=12, spacing=8
        )

        layout.add_widget(Label(
            text="NEXORA MUSIC PLAYER",
            font_size=24,
            size_hint_y=None,
            height=45
        ))

        chooser = FileChooserListView(
            path="/storage/emulated/0/Music",
            filters=["*.mp3", "*.wav", "*.ogg"]
        )

        layout.add_widget(chooser)

        status = Label(
            text="Select a music file",
            size_hint_y=None,
            height=35
        )

        def load_music(instance):
            if not chooser.selection:
                status.text = "First select a song!"
                return

            if self.sound:
                self.sound.stop()

            self.sound = SoundLoader.load(
                chooser.selection[0]
            )

            if self.sound:
                status.text = "Music Loaded!"
            else:
                status.text = "File could not be loaded"

        def play_music(instance):
            if self.sound:
                self.sound.play()
                status.text = "Music Playing!"
            else:
                status.text = "Load a song first"

        def stop_music(instance):
            if self.sound:
                self.sound.stop()
                status.text = "Music Stopped"

        layout.add_widget(self.button("LOAD MUSIC", load_music))
        layout.add_widget(self.button("PLAY MUSIC", play_music))
        layout.add_widget(self.button("STOP MUSIC", stop_music))
        layout.add_widget(status)

        self.back(layout)
        s.add_widget(layout)
        self.sm.add_widget(s)

    def profile(self):
        s = Screen(name="profile")
        layout = BoxLayout(
            orientation="vertical", padding=25, spacing=20
        )

        layout.add_widget(Label(text="MY PROFILE", font_size=30))
        layout.add_widget(Label(
            text="APP: NEXORA\nCREATOR: AYUSH\nVERSION: 3.0",
            font_size=23
        ))

        self.back(layout)
        s.add_widget(layout)
        self.sm.add_widget(s)

    def settings(self):
        s = Screen(name="settings")
        layout = BoxLayout(
            orientation="vertical", padding=25, spacing=20
        )

        layout.add_widget(Label(text="SETTINGS", font_size=30))
        layout.add_widget(Label(
            text="NEXORA\nPURPLE NEON THEME\nVERSION 3.0",
            font_size=22
        ))

        self.back(layout)
        s.add_widget(layout)
        self.sm.add_widget(s)


if __name__ == "__main__":
    NexoraApp().run()

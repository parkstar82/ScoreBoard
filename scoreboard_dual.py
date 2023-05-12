from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import time
import screeninfo
from timer import Timer


class ScoreBoard:
    def __init__(self, parent, screen_width, screen_height, timer):
        self.parent = parent
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.timer = timer

        self.round = 1
        self.red_score = 0
        self.blue_score = 0
        self.str_font = "굴림"  # Windows Basic 한글 Font
        self.str_number_font = "Arial"  # 숫자 폰트
        
        # Const
        self.title_font_size = 80
        self.score_label_font_size = 350
        self.warning_font_size = 40
        self.name_font_size = 60
        self.timer_1_10_button_font_size = 13
        self.plus_minus_button_font_size = 60
        self.timer_button_font_size = 45
        self.reset_timer_button_font_size = 15
        self.timer_label_width_size = 540
        self.timer_label_height_size = 175
        self.timer_label_font_size = 100

        self.title_font = (self.str_font, self.adjust_widget_size(self.title_font_size), "bold")
        self.score_label_font = (self.str_number_font, self.adjust_widget_size(self.score_label_font_size))
        self.warning_font = (self.str_font, self.adjust_widget_size(self.warning_font_size))
        self.name_font = (self.str_font, self.adjust_widget_size(self.name_font_size))
        self.timer_1_10_button_font = (self.str_number_font, self.adjust_widget_size(self.timer_1_10_button_font_size))
        self.plus_minus_button_font = (self.str_number_font, self.adjust_widget_size(self.plus_minus_button_font_size))
        self.timer_button_font = (self.str_number_font, self.adjust_widget_size(self.timer_button_font_size))
        self.reset_timer_button_font = (self.str_number_font, self.adjust_widget_size(self.reset_timer_button_font_size))
        self.timer_label_width = self.adjust_widget_size(self.timer_label_width_size)
        self.timer_label_height = self.adjust_widget_size(self.timer_label_height_size)
        self.timer_label_font = (self.str_number_font, self.adjust_widget_size(self.timer_label_font_size))

        pygame.mixer.init()
        pygame.mixer.music.load(self.resource_path("end_sound.mp3"))

        # Title text input
        self.title_entry = tk.Entry(
            self.parent,
            font=self.title_font,
            fg="white",
            bg="black",
            justify="center",
            insertbackground='yellow'
        )
        self.title_entry.place(
            relx=0.5, rely=0.06, anchor="center", relwidth=1.0, relheight=0.13
        )
        # Set initial text
        initial_text = "합기도대회"
        self.title_entry.insert(0, initial_text)

        # Red score panel
        self.red_panel = tk.Frame(self.parent, bg="red")
        self.red_panel.place(relx=0, rely=0.12, relwidth=0.5, relheight=0.7)

        self.red_label = tk.Label(
            self.red_panel,
            text="{}".format(self.red_score),
            fg="white",
            bg="red",
            font=self.score_label_font,
        )
        self.red_label.place(relx=0.5, rely=0.4, anchor='center')

        # Warning buttons
        self.red_warning_button = tk.Button(
            self.parent,
            text="경고",
            command=self.red_warning,
            font=self.warning_font,
        )
        self.red_warning_button.place(relx=0.05, rely=0.9, anchor="center")

        # Warning circles
        self.load_images()

        self.red_warning_box = tk.Frame(self.red_panel, bg="black")
        self.red_warning_box.place(
            relx=0.5, rely=0.8, relwidth=0.4, relheight=0.12, anchor="center"
        )

        self.red_yellow_circle = tk.Label(self.red_warning_box, bg="black")
        self.red_yellow_circle.place(relx=0.15, rely=0.5, anchor="center")

        self.red_red_circle1 = tk.Label(self.red_warning_box, bg="black")
        self.red_red_circle1.place(relx=0.5, rely=0.5, anchor="center")

        self.red_red_circle2 = tk.Label(self.red_warning_box, bg="black")
        self.red_red_circle2.place(relx=0.85, rely=0.5, anchor="center")
        
        self.red_yellow_circle.config(image=self.yellow_circle_photo)
        self.red_red_circle1.config(image=self.red_circle_photo)
        self.red_red_circle2.config(image=self.red_circle_photo)

        # Warning state
        self.red_warning_state = 0

        # Name text input
        self.red_name_entry = tk.Entry(
            self.red_panel,
            font=self.name_font,
            fg="white",
            bg="black",
            justify="center",
            width=self.adjust_widget_size(50),
            insertbackground='yellow'
        )
        self.red_name_entry.pack(anchor="center", side="bottom", pady=0, padx=0)
        self.red_name_entry.place(
            relx=0.5, rely=0.94, anchor="center", relwidth=1.0, relheight=0.12
        )
        # Set initial text
        initial_red_name_text = "홍길동"
        self.red_name_entry.insert(0, initial_red_name_text)

        # Blue score panel
        self.blue_panel = tk.Frame(self.parent, bg="blue")
        self.blue_panel.place(relx=0.5, rely=0.12, relwidth=0.5, relheight=0.7)

        self.blue_label = tk.Label(
            self.blue_panel,
            text="{}".format(self.blue_score),
            fg="white",
            bg="blue",
            font=self.score_label_font,
        )
        self.blue_label.place(relx=0.5, rely=0.4, anchor='center')

        # Warning buttons
        self.blue_warning_button = tk.Button(
            self.parent,
            text="경고",
            command=self.blue_warning,
            font=self.warning_font,
        )
        self.blue_warning_button.place(relx=0.95, rely=0.9, anchor="center")

        # Warning circles
        self.blue_warning_box = tk.Frame(self.blue_panel, bg="black")
        self.blue_warning_box.place(
            relx=0.5, rely=0.8, relwidth=0.4, relheight=0.12, anchor="center"
        )

        self.blue_yellow_circle = tk.Label(self.blue_warning_box, bg="black")
        self.blue_yellow_circle.place(relx=0.15, rely=0.5, anchor="center")

        self.blue_red_circle1 = tk.Label(self.blue_warning_box, bg="black")
        self.blue_red_circle1.place(relx=0.5, rely=0.5, anchor="center")

        self.blue_red_circle2 = tk.Label(self.blue_warning_box, bg="black")
        self.blue_red_circle2.place(relx=0.85, rely=0.5, anchor="center")
        
        self.blue_yellow_circle.config(image=self.yellow_circle_photo)
        self.blue_red_circle1.config(image=self.red_circle_photo)
        self.blue_red_circle2.config(image=self.red_circle_photo)

        # Warning state
        self.blue_warning_state = 0

        # Name text input
        self.blue_name_entry = tk.Entry(
            self.blue_panel,
            font=self.name_font,
            fg="white",
            bg="black",
            justify="center",
            width=self.adjust_widget_size(50),
            insertbackground='yellow'
        )
        self.blue_name_entry.place(
            relx=0.5, rely=0.94, anchor="center", relwidth=1.0, relheight=0.12
        )
        # Set initial text
        initial_blue_name_text = "청길동"
        self.blue_name_entry.insert(0, initial_blue_name_text)

        self.init_timer_label()

        self.increase_timer_button = tk.Button(
            self.parent,
            text="-1",
            command=lambda: self.decrease_timer(100),
            font=self.timer_1_10_button_font,
        )
        self.increase_timer_button.place(relx=0.362, rely=0.842, anchor="center")

        self.decrease_timer_button = tk.Button(
            self.parent,
            text="+1",
            command=lambda: self.increase_timer(100),
            font=self.timer_1_10_button_font,
        )
        self.decrease_timer_button.place(relx=0.615, rely=0.842, anchor="center")

        self.increase_timer10_button = tk.Button(
            self.parent,
            text="-10",
            command=lambda: self.decrease_timer(1000),
            font=self.timer_1_10_button_font,
        )
        self.increase_timer10_button.place(relx=0.385, rely=0.842, anchor="center")

        self.decrease_timer10_button = tk.Button(
            self.parent,
            text="+10",
            command=lambda: self.increase_timer(1000),
            font=self.timer_1_10_button_font,
        )
        self.decrease_timer10_button.place(relx=0.642, rely=0.842, anchor="center")

        # Buttons
        self.red_button = tk.Button(
            self.parent,
            text="+1",
            command=self.red_increase,
            font=self.plus_minus_button_font,
            fg="red",
        )
        self.red_button.place(relx=0.18, rely=0.9, anchor="center")

        self.red_button_minus = tk.Button(
            self.parent,
            text="-1",
            command=self.red_decrease,
            font=self.plus_minus_button_font,
            fg="red",
        )
        self.red_button_minus.place(relx=0.29, rely=0.9, anchor="center")

        self.blue_button = tk.Button(
            self.parent,
            text="+1",
            command=self.blue_increase,
            font=self.plus_minus_button_font,
            fg="blue",
        )
        self.blue_button.place(relx=0.72, rely=0.9, anchor="center")

        self.blue_button_minus = tk.Button(
            self.parent,
            text="-1",
            command=self.blue_decrease,
            font=self.plus_minus_button_font,
            fg="blue",
        )
        self.blue_button_minus.place(relx=0.827, rely=0.9, anchor="center")

        # Start timer button
        self.start_timer_button = tk.Button(
            self.parent,
            text="Start Timer",
            # command=self.start_timer,
            font=self.timer_button_font,
        )
        self.start_timer_button.place(relx=0.5, rely=0.88, anchor="center")

        # Reset timer button
        self.reset_timer_button = tk.Button(
            self.parent,
            text="Reset",
            command=self.reset_timer,
            font=self.reset_timer_button_font,
        )
        self.reset_timer_button.place(relx=0.5, rely=0.96, anchor="center")
        
        # resize windows event bind
        self.parent.bind('<Configure>', self.on_resize)
        
    def on_resize(self, event):
        # Update the screen width and height
        print('on_resize')
        self.screen_width = self.parent.winfo_width()
        self.screen_height = self.parent.winfo_height()

        # update adjus widget size
        self.title_font = (self.str_font, self.adjust_widget_size(self.title_font_size), "bold")
        self.score_label_font = (self.str_number_font, self.adjust_widget_size(self.score_label_font_size))
        self.warning_font = (self.str_font, self.adjust_widget_size(self.warning_font_size))
        self.name_font = (self.str_font, self.adjust_widget_size(self.name_font_size))
        self.timer_1_10_button_font = (self.str_number_font, self.adjust_widget_size(self.timer_1_10_button_font_size))
        self.plus_minus_button_font = (self.str_number_font, self.adjust_widget_size(self.plus_minus_button_font_size))
        self.timer_button_font = (self.str_number_font, self.adjust_widget_size(self.timer_button_font_size))
        self.reset_timer_button_font = (self.str_number_font, self.adjust_widget_size(self.reset_timer_button_font_size))
        self.timer_label_width = self.adjust_widget_size(self.timer_label_width_size)
        self.timer_label_height = self.adjust_widget_size(self.timer_label_height_size)
        self.timer_label_font = (self.str_number_font, self.adjust_widget_size(self.timer_label_font_size))
        
        self.title_entry.config(font=self.title_font)
        self.red_label.config(font=self.score_label_font)
        self.blue_label.config(font=self.score_label_font)
        self.red_warning_button.config(font=self.warning_font)
        self.blue_warning_button.config(font=self.warning_font)
        self.red_name_entry.config(font=self.name_font)
        self.blue_name_entry.config(font=self.name_font)
        self.increase_timer_button.config(font=self.timer_1_10_button_font)
        self.decrease_timer_button.config(font=self.timer_1_10_button_font)
        self.increase_timer10_button.config(font=self.timer_1_10_button_font)
        self.decrease_timer10_button.config(font=self.timer_1_10_button_font)
        self.red_button.config(font=self.plus_minus_button_font)
        self.red_button_minus.config(font=self.plus_minus_button_font)
        self.blue_button.config(font=self.plus_minus_button_font)
        self.blue_button_minus.config(font=self.plus_minus_button_font)
        self.start_timer_button.config(font=self.timer_button_font)
        self.reset_timer_button.config(font=self.reset_timer_button_font)
        
        self.timer_canvas.config(
            width=self.timer_label_width,
            height=self.timer_label_height
        )
        self.timer_label.config(font=self.timer_label_font)
        self.timer_label.place(
            x=(self.timer_label_width // 2), y=(self.timer_label_height // 2), anchor="center"
        )
        
    def init_timer_label(self):
        # Timer
        self.time_remaining = tk.StringVar(self.parent)
        self.time_remaining.set(timer.get_time_remaining())

        self.timer_canvas = tk.Canvas(
            self.parent,
            width=self.timer_label_width,
            height=self.timer_label_height,
            bg="white",
            bd=2,
            relief="solid",
            highlightthickness=2,
            highlightbackground="yellow",
            highlightcolor="yellow",
        )
        self.timer_canvas.place(relx=0.5, rely=0.73, anchor="center")

        self.timer_label = tk.Label(
            self.timer_canvas,
            textvariable=self.time_remaining,
            font=self.timer_label_font,
            bg="white",
        )
        self.timer_label.place(
            x=(self.timer_label_width // 2), y=(self.timer_label_height // 2), anchor="center"
        )

    def load_images(self):
        # Warning circles
        self.yellow_circle_image = Image.open(self.resource_path("yellow_circle.png"))
        adjust_image_size = self.adjust_widget_size(80)
        self.yellow_circle_image = self.yellow_circle_image.resize(
            (adjust_image_size, adjust_image_size), Image.LANCZOS
        )
        self.yellow_circle_photo = ImageTk.PhotoImage(
            self.yellow_circle_image, master=self.parent
        )

        self.red_circle_image = Image.open(self.resource_path("red_circle.png"))
        self.red_circle_image = self.red_circle_image.resize(
            (adjust_image_size, adjust_image_size), Image.LANCZOS
        )
        self.red_circle_photo = ImageTk.PhotoImage(
            self.red_circle_image, master=self.parent
        )

    def red_increase(self):
        self.red_score += 1
        self.red_label.config(text="{}".format(self.red_score))

    def blue_increase(self):
        self.blue_score += 1
        self.blue_label.config(text="{}".format(self.blue_score))

    def red_decrease(self):
        self.red_score -= 1
        self.red_label.config(text="{}".format(self.red_score))

    def blue_decrease(self):
        self.blue_score -= 1
        self.blue_label.config(text="{}".format(self.blue_score))

    def update_timer(self):
        self.time_remaining.set(self.timer.get_time_remaining())
        self.timer_label.update_idletasks()  # Update only the timer label widget

    def show_start_timer_button(self, isStart):
        if isStart:
            self.start_timer_button.config(text="Stop Timer")
            # Hide Button
            self.increase_timer_button.place_forget()
            self.decrease_timer_button.place_forget()
            self.increase_timer10_button.place_forget()
            self.decrease_timer10_button.place_forget()
        else:
            self.start_timer_button.config(text="Start Timer")
            # Show Button
            self.increase_timer_button.place(
                relx=0.362, rely=0.842, anchor="center"
            )
            self.decrease_timer_button.place(
                relx=0.615, rely=0.842, anchor="center"
            )
            self.increase_timer10_button.place(
                relx=0.385, rely=0.842, anchor="center"
            )
            self.decrease_timer10_button.place(
                relx=0.642, rely=0.842, anchor="center"
            )
    
    def play_sound(self):
        # Play an MP3 file when the timer ends
        pygame.mixer.music.play()

    def reset_timer(self):
        self.timer.reset()
        # self.timer_seconds = self.init_time
        # self.start_timer_seconds = self.init_time
        self.update_timer()

        # Reset scores
        self.round = 1
        self.red_score = 0
        self.blue_score = 0
        self.red_label.config(text="{}".format(self.red_score))
        self.blue_label.config(text="{}".format(self.blue_score))
        self.red_warning_state = -1
        self.blue_warning_state = -1

        self.timer.is_start = True  # 경고 상태 초기화
        self.red_warning()
        self.blue_warning()

        # Reset Timer Button
        self.timer.timer_running = False
        self.timer.is_start = False
        self.start_timer_button.config(text="Start Timer")

        # Show Button
        self.increase_timer_button.place(relx=0.362, rely=0.842, anchor="center")
        self.decrease_timer_button.place(relx=0.615, rely=0.842, anchor="center")
        self.increase_timer10_button.place(relx=0.385, rely=0.842, anchor="center")
        self.decrease_timer10_button.place(relx=0.642, rely=0.842, anchor="center")

    def increase_timer(self, time):
        # self.timer.increase_timer(time)
        self.update_timer()

    def decrease_timer(self, time):
        # if (self.timer.timer_seconds - time) > 0:
        #     self.timer.decrease_timer(time)
        self.update_timer()

    def save_warning_widgets(self):
        self.red_yellow_circle_place_info = self.red_yellow_circle.place_info()
        self.red_red_circle1_place_info = self.red_red_circle1.place_info()
        self.red_red_circle2_place_info = self.red_red_circle2.place_info()
        self.blue_yellow_circle_place_info = self.blue_yellow_circle.place_info()
        self.blue_red_circle1_place_info = self.blue_red_circle1.place_info()
        self.blue_red_circle2_place_info = self.blue_red_circle2.place_info()

    def red_warning(self):
        if self.timer.is_start:
            self.red_warning_state += 1
            
            if self.red_warning_state == 1:
                self.red_yellow_circle.config(image=self.yellow_circle_photo)
                self.red_yellow_circle.place(**self.red_yellow_circle_place_info)
                self.red_red_circle1.place_forget()
                self.red_red_circle2.place_forget()
            elif self.red_warning_state == 2:
                self.red_yellow_circle.place_forget()
                self.red_red_circle1.config(image=self.red_circle_photo)
                self.red_red_circle1.place(**self.red_red_circle1_place_info)
                self.red_red_circle2.place_forget()
            elif self.red_warning_state == 3:
                self.red_yellow_circle.place(**self.red_yellow_circle_place_info)
                self.red_red_circle1.place(**self.red_red_circle1_place_info)
                self.red_red_circle2.place_forget()
            elif self.red_warning_state == 4:
                self.red_yellow_circle.place_forget()
                self.red_red_circle1.place(**self.red_red_circle1_place_info)
                self.red_red_circle2.config(image=self.red_circle_photo)
                self.red_red_circle2.place(**self.red_red_circle2_place_info)
            else:
                self.red_warning_state = 0
                self.red_yellow_circle.place_forget()
                self.red_red_circle1.place_forget()
                self.red_red_circle2.place_forget()

    def blue_warning(self):
        if self.timer.is_start:
            self.blue_warning_state += 1

            if self.blue_warning_state == 1:
                self.blue_yellow_circle.config(image=self.yellow_circle_photo)
                self.blue_yellow_circle.place(**self.blue_yellow_circle_place_info)
                self.blue_red_circle1.place_forget()
                self.blue_red_circle2.place_forget()
            elif self.blue_warning_state == 2:
                self.blue_yellow_circle.place_forget()
                self.blue_red_circle1.config(image=self.red_circle_photo)
                self.blue_red_circle1.place(**self.blue_red_circle1_place_info)
                self.blue_red_circle2.place_forget()
            elif self.blue_warning_state == 3:
                self.blue_yellow_circle.place(**self.blue_yellow_circle_place_info)
                self.blue_red_circle1.place(**self.blue_red_circle1_place_info)
                self.blue_red_circle2.place_forget()
            elif self.blue_warning_state == 4:
                self.blue_yellow_circle.place_forget()
                self.blue_red_circle1.place(**self.blue_red_circle1_place_info)
                self.blue_red_circle2.config(image=self.red_circle_photo)
                self.blue_red_circle2.place(**self.blue_red_circle2_place_info)
            else:
                self.blue_warning_state = 0
                self.blue_yellow_circle.place_forget()
                self.blue_red_circle1.place_forget()
                self.blue_red_circle2.place_forget()

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def adjust_widget_size(self, base_size, base_resolution=(1920, 1080)):
        width_scale = self.screen_width / base_resolution[0]
        height_scale = self.screen_height / base_resolution[1]

        # Use the smaller scaling factor to ensure the widget fits on the screen
        scale_factor = min(width_scale, height_scale)

        # Calculate the adjusted size based on the scaling factor
        adjusted_size = int(base_size * scale_factor)

        return adjusted_size

    def toggle_fullscreen(self, isActivate=True):
        if isActivate:
            # deactivate full screen
            self.parent.state("normal")
            self.parent.geometry(self.geometry)
            self.parent.overrideredirect(False)
        else:
            # activate full screen
            # Store geometry for reset
            self.geometry = self.parent.geometry()
            # Hides borders and make truly fullscreen
            self.parent.overrideredirect(True)
            # Maximize window (Windows only). Optionally set screen geometry if you have it
            self.parent.state("zoomed")

    def blink_winner(self, count, is_blue_win):
        if count <= 0:
            self.red_label.config(fg="white")
            self.blue_label.config(fg="white")
            self.parent.update_idletasks()
            return

        if is_blue_win:
            self.blue_label.config(
                fg="yellow" if self.blue_label.cget("fg") == "white" else "white"
            )
        else:
            self.red_label.config(
                fg="yellow" if self.red_label.cget("fg") == "white" else "white"
            )

        self.parent.update_idletasks()
        self.parent.after(500, self.blink_winner, count - 1, is_blue_win)


class ControlPanel(tk.Toplevel):
    def __init__(self, master, scoreboard, monitor, timer):
        super().__init__(master)
        self.scoreboard = scoreboard
        self.monitor = monitor
        self.timer = timer
        
        self.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        self.overrideredirect(False)

        self.screen_width = self.monitor.width
        self.screen_height = self.monitor.height

        self.widgets = ScoreBoard(self, self.screen_width, self.screen_height, self.timer)

        self.title("컨트롤 패널")

        self.widgets.red_button.config(command=self.update_red_score)
        self.widgets.red_button_minus.config(command=self.update_red_decrease)
        self.widgets.red_warning_button.config(command=self.update_red_warning)
        self.widgets.blue_button.config(command=self.update_blue_score)
        self.widgets.blue_button_minus.config(command=self.update_blue_decrease)
        self.widgets.blue_warning_button.config(command=self.update_blue_warning)
        self.widgets.increase_timer_button.config(
            command=lambda: self.update_decrease_timer(100)
        )
        self.widgets.decrease_timer_button.config(
            command=lambda: self.update_increase_timer(100)
        )
        self.widgets.increase_timer10_button.config(
            command=lambda: self.update_decrease_timer(1000)
        )
        self.widgets.decrease_timer10_button.config(
            command=lambda: self.update_increase_timer(1000)
        )
        self.widgets.start_timer_button.config(command=self.update_start_timer)
        self.widgets.reset_timer_button.config(command=self.update_reset_timer)
        # Bind the keys
        self.bind("<KeyPress>", self.update_on_key_pressed)

        # Bind the close event to the on_close method
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.widgets.title_entry.bind("<KeyRelease>", self.copy_title_entry)
        self.widgets.red_name_entry.bind("<KeyRelease>", self.copy_red_name_entry)
        self.widgets.blue_name_entry.bind("<KeyRelease>", self.copy_blue_name_entry)

    def init_geometry(self):
        self.geometry(
            f"{self.screen_width}x{self.screen_height}+{self.monitor.x}+{self.monitor.y}"
        )
        
    def copy_title_entry(self, evnet):
        self.scoreboard.widgets.title_entry.delete(0, tk.END)
        self.scoreboard.widgets.title_entry.insert(0, self.widgets.title_entry.get())
        
    def copy_red_name_entry(self, event):
        self.scoreboard.widgets.red_name_entry.delete(0, tk.END)
        self.scoreboard.widgets.red_name_entry.insert(0, self.widgets.red_name_entry.get())
        
    def copy_blue_name_entry(self, event):
        self.scoreboard.widgets.blue_name_entry.delete(0, tk.END)
        self.scoreboard.widgets.blue_name_entry.insert(0, self.widgets.blue_name_entry.get())
        
    def on_close(self):
        # Close both the control panel and the view panel
        self.destroy()
        self.scoreboard.destroy()

        # Terminate the mainloop
        self.master.quit()

    def update_red_score(self):
        self.scoreboard.widgets.red_increase()
        self.widgets.red_increase()

    def update_red_decrease(self):
        self.scoreboard.widgets.red_decrease()
        self.widgets.red_decrease()

    def update_red_warning(self):
        self.widgets.red_warning()
        self.scoreboard.widgets.red_warning()

    def update_blue_score(self):
        self.scoreboard.widgets.blue_increase()
        self.widgets.blue_increase()

    def update_blue_decrease(self):
        self.scoreboard.widgets.blue_decrease()
        self.widgets.blue_decrease()

    def update_blue_warning(self):
        self.scoreboard.widgets.blue_warning()
        self.widgets.blue_warning()

    def update_decrease_timer(self, value):
        self.timer.decrease_timer(value)
        self.scoreboard.widgets.decrease_timer(value)
        self.widgets.decrease_timer(value)

    def update_increase_timer(self, value):
        self.timer.increase_timer(value)
        self.scoreboard.widgets.increase_timer(value)
        self.widgets.increase_timer(value)

    def update_on_key_pressed(self, event):
        if (
            self.focus_get() != self.widgets.title_entry
            and self.focus_get() != self.widgets.red_name_entry
            and self.focus_get() != self.widgets.blue_name_entry
        ):
            key_code = event.keycode
            if key_code == 49:  # 1
                self.widgets.blue_increase()
                self.scoreboard.widgets.blue_increase()
            elif key_code == 50:  # 2
                self.widgets.blue_decrease()
                self.scoreboard.widgets.blue_decrease()
            elif key_code == 189:  # -
                self.widgets.red_increase()
                self.scoreboard.widgets.red_increase()
            elif key_code == 187:  # =
                self.widgets.red_decrease()
                self.scoreboard.widgets.red_decrease()
            elif key_code == 52:  # 4
                self.widgets.blink_winner(6, True)  # Blue Win
                self.scoreboard.widgets.blink_winner(6, True)  # Blue Win
            elif key_code == 57:  # 9
                self.widgets.blink_winner(6, False)  # Red Win
                self.scoreboard.widgets.blink_winner(6, False)  # Red Win
            elif key_code == 32:  # Spacebar
                self.start_timer()
            elif key_code == 13:  # Enter
                self.scoreboard.widgets.toggle_fullscreen(self.scoreboard.overrideredirect())
                self.widgets.toggle_fullscreen(self.overrideredirect())
            elif key_code == 27:  # Escape
                self.scoreboard.widgets.toggle_fullscreen(True)
                self.widgets.toggle_fullscreen(True)
        elif event.keycode == 13:  # Enter
            self.focus()

    def update_start_timer(self):
        # self.scoreboard.widgets.start_timer()
        self.start_timer()

    def update_reset_timer(self):
        self.widgets.reset_timer()
        self.scoreboard.reset_timer()

    def swap_positions(self):
        red_widgets = [
            self.widgets.red_panel,
            self.widgets.red_warning_button,
            self.widgets.red_warning_box,
            self.widgets.red_yellow_circle,
            self.widgets.red_red_circle1,
            self.widgets.red_red_circle2,
            self.widgets.red_button,
            self.widgets.red_button_minus,
        ]

        blue_widgets = [
            self.widgets.blue_panel,
            self.widgets.blue_warning_button,
            self.widgets.blue_warning_box,
            self.widgets.blue_yellow_circle,
            self.widgets.blue_red_circle1,
            self.widgets.blue_red_circle2,
            self.widgets.blue_button,
            self.widgets.blue_button_minus,
        ]

        # Save the original relx values
        red_original_relx_values = [
            widget.place_info()["relx"] for widget in red_widgets
        ]
        blue_original_relx_values = [
            widget.place_info()["relx"] for widget in blue_widgets
        ]

        # Swap relx values for red and blue widgets
        for i in range(len(red_widgets)):
            red_widget = red_widgets[i]
            blue_widget = blue_widgets[i]

            red_widget.place_configure(relx=blue_original_relx_values[i])
            blue_widget.place_configure(relx=red_original_relx_values[i])
            
        self.widgets.save_warning_widgets()

    def start_timer(self):
        if self.timer.start_timer_seconds > 0:
            if not self.timer.timer_running:
                self.timer.start(True)
                self.timer.is_start = True
                self.widgets.show_start_timer_button(True) # Show 'Stop Timer' and Hide widgets
                self.countdown()
            else:
                self.timer.start(False)
                self.widgets.show_start_timer_button(False) # Show 'Start Timer' and Show widgets
        else:
            # 2라운드 시작
            self.timer.timer_running = False
            self.timer.is_start = False
            self.timer.start_timer_seconds = 3000
            self.timer.timer_seconds = 3000
            self.widgets.update_timer()
            self.widgets.show_start_timer_button(False) # Show 'Start Timer' and Show widgets
            
    def countdown(self):
        if self.timer.timer_running:
            self.timer.update_timer_seconds()

            if self.timer.timer_seconds > 0:
                self.widgets.update_timer()
                self.scoreboard.widgets.update_timer()
                self.after(10, self.countdown)
            elif self.timer.timer_seconds <= 0:  # 시간 종료로 경기가 끝났을 때
                # 다음 라운드 준비
                self.widgets.round += 1
                self.widgets.start_timer_button.config(text="{} Round".format(self.widgets.round))
                # Reset Timer Button
                self.timer.timer_running = False
                self.timer.is_start = False
                self.timer.start_timer_seconds = 0
                self.timer.timer_seconds = 0
                
                self.widgets.update_timer()
                self.scoreboard.widgets.update_timer()

                # Play an MP3 file when the timer ends
                self.widgets.play_sound()
                self.scoreboard.widgets.play_sound()

                # Blink the winner's score
                # self.blink_winner(6)  # Blink 3 times (6 because it's a half cycle of blinking)
            
class ViewPanel(tk.Toplevel):
    def __init__(self, master, monitor, timer):
        super().__init__(master)

        self.title("스코어보드")
        self.monitor = monitor
        self.timer = timer
        self.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        self.overrideredirect(False)

        self.screen_width = self.monitor.width
        self.screen_height = self.monitor.height
        self.widgets = ScoreBoard(self, self.screen_width, self.screen_height, timer)
        
        # view panel에서 숨김
        self.widgets.red_warning_button.place_forget()
        self.widgets.red_button.place_forget()
        self.widgets.red_button_minus.place_forget()
        self.widgets.blue_warning_button.place_forget()
        self.widgets.blue_button.place_forget()
        self.widgets.blue_button_minus.place_forget()
        self.widgets.red_warning_button.place_forget()
        
        self.widgets.start_timer_button.place_forget()
        self.widgets.reset_timer_button.place_forget()
        self.widgets.increase_timer_button.place_forget()
        self.widgets.increase_timer10_button.place_forget()
        self.widgets.decrease_timer_button.place_forget()
        self.widgets.decrease_timer10_button.place_forget()
        
        # 위젯 크기 조정
        self.widgets.red_panel.place(relheight=0.881)
        self.widgets.blue_panel.place(relheight=0.881)
        
        self.widgets.name_font_size = 80
        self.widgets.name_font = (self.widgets.str_font, self.widgets.adjust_widget_size(self.widgets.name_font_size))
        self.widgets.red_name_entry.config(font=self.widgets.name_font)
        self.widgets.blue_name_entry.config(font=self.widgets.name_font)
        self.widgets.red_label.config(pady=60, padx=20)
        self.widgets.blue_label.config(pady=60, padx=20)
        
        self.widgets.save_warning_widgets()

    def init_geometry(self):
        self.geometry(
            f"{self.screen_width}x{self.screen_height}+{self.monitor.x}+{self.monitor.y}"
        )
        
    def start_timer(self):
        if self.timer.start_timer_seconds > 0:
            self.focus()

            if not self.timer.timer_running:
                self.widgets.countdown()
        else:
            self.widgets.update_timer()
            
    def reset_timer(self):
        self.widgets.update_timer()

        # Reset scores
        self.widgets.round = 1
        self.widgets.red_score = 0
        self.widgets.blue_score = 0
        self.widgets.red_label.config(text="{}".format(self.widgets.red_score))
        self.widgets.blue_label.config(text="{}".format(self.widgets.blue_score))
        self.widgets.red_warning_state = -1
        self.widgets.blue_warning_state = -1

        self.timer.is_start = True  # 경고 상태 초기화
        self.widgets.red_warning()
        self.widgets.blue_warning()

        # Reset Timer Button
        self.timer.timer_running = False
        self.timer.is_start = False

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    monitor = []
    for m in screeninfo.get_monitors():
        monitor.append(m)
            
    if len(monitor) == 1:
        monitor.append(monitor[0])
        
    timer = Timer()

    score_board = ViewPanel(root, monitor[1], timer)
    control_panel = ControlPanel(root, score_board, monitor[0], timer)
    control_panel.swap_positions()

    root.mainloop()

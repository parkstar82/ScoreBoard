from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import screeninfo
from timer import Timer

import win32gui
import win32ui
import win32con


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
        self.weight_font_size = 43
        self.timer_1_10_button_font_size = 13
        self.plus_minus_button_font_size = 60
        self.timer_button_font_size = 45
        self.reset_timer_button_font_size = 15
        self.timer_label_width_size = 540
        self.timer_label_height_size = 175
        self.timer_label_font_size = 100

        self.title_font = (
            self.str_font,
            self.adjust_widget_size(self.title_font_size),
            "bold",
        )
        self.score_label_font = (
            self.str_number_font,
            self.adjust_widget_size(self.score_label_font_size),
        )
        self.warning_font = (
            self.str_font,
            self.adjust_widget_size(self.warning_font_size),
        )
        self.name_font = (self.str_font, self.adjust_widget_size(self.name_font_size))
        self.weight_font = (
            self.str_font,
            self.adjust_widget_size(self.weight_font_size),
        )
        self.timer_1_10_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_1_10_button_font_size),
        )
        self.plus_minus_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.plus_minus_button_font_size),
        )
        self.timer_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_button_font_size),
        )
        self.reset_timer_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.reset_timer_button_font_size),
        )
        self.timer_label_width = self.adjust_widget_size(self.timer_label_width_size)
        self.timer_label_height = self.adjust_widget_size(self.timer_label_height_size)
        self.timer_label_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_label_font_size),
        )

        pygame.mixer.init()
        pygame.mixer.music.load(self.resource_path("end_sound.mp3"))

        # Title text input
        self.title_entry = tk.Entry(
            self.parent,
            font=self.title_font,
            fg="white",
            bg="black",
            justify="center",
            insertbackground="yellow",
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
        self.red_label.place(relx=0.5, rely=0.4, anchor="center")

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
            insertbackground="yellow",
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
        self.blue_label.place(relx=0.5, rely=0.4, anchor="center")

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
            insertbackground="yellow",
        )
        self.blue_name_entry.place(
            relx=0.5, rely=0.94, anchor="center", relwidth=1.0, relheight=0.12
        )
        # Set initial text
        initial_blue_name_text = "청길동"
        self.blue_name_entry.insert(0, initial_blue_name_text)

        self.init_timer_label()
        self.init_weight_entry()

        self.decrease_timer_button = tk.Button(
            self.parent,
            text="-1",
            command=lambda: self.decrease_timer(100),
            font=self.timer_1_10_button_font,
        )
        self.decrease_timer_button.place(relx=0.362, rely=0.842, anchor="center")

        self.increase_timer_button = tk.Button(
            self.parent,
            text="+1",
            command=lambda: self.increase_timer(100),
            font=self.timer_1_10_button_font,
        )
        self.increase_timer_button.place(relx=0.615, rely=0.842, anchor="center")

        self.decrease_timer10_button = tk.Button(
            self.parent,
            text="-10",
            command=lambda: self.decrease_timer(1000),
            font=self.timer_1_10_button_font,
        )
        self.decrease_timer10_button.place(relx=0.385, rely=0.842, anchor="center")

        self.increase_timer10_button = tk.Button(
            self.parent,
            text="+10",
            command=lambda: self.increase_timer(1000),
            font=self.timer_1_10_button_font,
        )
        self.increase_timer10_button.place(relx=0.642, rely=0.842, anchor="center")

        # Capture button
        self.capture_button = tk.Button(
            self.parent,
            text="Capture",
            font=self.reset_timer_button_font,
        )
        self.capture_button.place(relx=0.630, rely=0.882, anchor="center")

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
        self.parent.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Update the screen width and height
        self.screen_width = self.parent.winfo_width()
        self.screen_height = self.parent.winfo_height()

        # update adjus widget size
        self.title_font = (
            self.str_font,
            self.adjust_widget_size(self.title_font_size),
            "bold",
        )
        self.score_label_font = (
            self.str_number_font,
            self.adjust_widget_size(self.score_label_font_size),
        )
        self.warning_font = (
            self.str_font,
            self.adjust_widget_size(self.warning_font_size),
        )
        self.name_font = (self.str_font, self.adjust_widget_size(self.name_font_size))
        self.weight_font = (
            self.str_font,
            self.adjust_widget_size(self.weight_font_size),
        )
        self.timer_1_10_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_1_10_button_font_size),
        )
        self.plus_minus_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.plus_minus_button_font_size),
        )
        self.timer_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_button_font_size),
        )
        self.reset_timer_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.reset_timer_button_font_size),
        )
        self.timer_label_width = self.adjust_widget_size(self.timer_label_width_size)
        self.timer_label_height = self.adjust_widget_size(self.timer_label_height_size)
        self.timer_label_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_label_font_size),
        )

        self.title_entry.config(font=self.title_font)
        self.red_label.config(font=self.score_label_font)
        self.blue_label.config(font=self.score_label_font)
        self.red_warning_button.config(font=self.warning_font)
        self.blue_warning_button.config(font=self.warning_font)
        self.red_name_entry.config(font=self.name_font)
        self.blue_name_entry.config(font=self.name_font)
        self.weight_entry.config(font=self.weight_font)
        self.increase_timer_button.config(font=self.timer_1_10_button_font)
        self.decrease_timer_button.config(font=self.timer_1_10_button_font)
        self.increase_timer10_button.config(font=self.timer_1_10_button_font)
        self.decrease_timer10_button.config(font=self.timer_1_10_button_font)
        self.capture_button.config(font=self.reset_timer_button_font)
        self.red_button.config(font=self.plus_minus_button_font)
        self.red_button_minus.config(font=self.plus_minus_button_font)
        self.blue_button.config(font=self.plus_minus_button_font)
        self.blue_button_minus.config(font=self.plus_minus_button_font)
        self.start_timer_button.config(font=self.timer_button_font)
        self.reset_timer_button.config(font=self.reset_timer_button_font)

        self.timer_canvas.config(
            width=self.timer_label_width, height=self.timer_label_height
        )
        self.timer_label.config(font=self.timer_label_font)
        self.timer_label.place(
            x=(self.timer_label_width // 2),
            y=(self.timer_label_height // 2),
            anchor="center",
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
        # view panel timer 위치
        # self.timer_canvas.place(relx=0.5, rely=0.73, anchor="center")
        self.timer_canvas.place(relx=0.5, rely=0.532, anchor="center")

        self.timer_label = tk.Label(
            self.timer_canvas,
            textvariable=self.time_remaining,
            font=self.timer_label_font,
            bg="white",
        )
        self.timer_label.place(
            x=(self.timer_label_width // 2),
            y=(self.timer_label_height // 2),
            anchor="center",
        )

    # def adjust_font_size(self):
    #     """weight_entry 폰트의 사이즈를 text overflow 하지 않게 조정한다.
    #     1. 입력된 글자가 많으면 폰트 사이즈를 크게한다.
    #     2. 입력된 글자가 적으면 폰트 사이즈를 작게한다
    #     """
    #     # Get the current font size
    #     current_font = tkfont.Font(family=self.weight_font[0], size=self.weight_font[1])

    #     # Get the width of the weight_entry widget
    #     widget_width = self.weight_entry.winfo_width()

    #     # Get the current text in the weight_entry widget
    #     current_text = self.text_var.get()

    #     # Calculate the width of the text
    #     text_width = self.weight_entry.tk.call(
    #         "font", "measure", current_font, current_text
    #     )

    #     # While the text is wider than the widget, decrease the font size
    #     if text_width > widget_width:
    #         while text_width > widget_width and self.weight_font[1] > 10:
    #             self.weight_font = (self.weight_font[0], self.weight_font[1] - 1)
    #             current_font.config(
    #                 family=self.weight_font[0], size=self.weight_font[1]
    #             )
    #             text_width = self.weight_entry.tk.call(
    #                 "font", "measure", current_font, current_text
    #             )
    #     elif text_width < widget_width:
    #         while text_width < widget_width and self.weight_font[1] < 43:
    #             self.weight_font = (self.weight_font[0], self.weight_font[1] + 1)
    #             current_font.config(
    #                 family=self.weight_font[0], size=self.weight_font[1]
    #             )
    #             text_width = self.weight_entry.tk.call(
    #                 "font", "measure", current_font, current_text
    #             )

    #         # 항상 widget_width 보다 작게 조정한다.
    #         if self.weight_font[1] != 43:
    #             self.weight_font = (self.weight_font[0], self.weight_font[1] - 1)

    #     # Apply the updated font to the weight_entry widget
    #     self.weight_font_size = self.weight_font[1]
    #     self.weight_entry.config(font=self.weight_font)

    def init_weight_entry(self):
        self.text_var = tk.StringVar()

        self.weight_entry = tk.Entry(
            self.parent,
            font=self.weight_font,
            fg="white",
            bg="black",
            justify="center",
            insertbackground="yellow",
            textvariable=self.text_var,
        )

        self.weight_entry.place(
            relx=0.5, rely=0.678, anchor="center", relwidth=0.284, relheight=0.12
        )

        # Set initial text
        initial_weight_text = "부별체급"
        self.weight_entry.insert(0, initial_weight_text)
        # self.text_var.trace("w", lambda name, index, mode, sv=self.text_var: self.adjust_font_size())

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
        
        #logo image
        self.logo_image = Image.open(self.resource_path("logo.jpg"))
        logo_adjust_image_size = self.adjust_widget_size(480)
        self.logo_image = self.logo_image.resize(
            (logo_adjust_image_size, logo_adjust_image_size), Image.LANCZOS
        )
        self.resize_logo_image = ImageTk.PhotoImage(
            self.logo_image, master=self.parent
        )
        
        log_adjust_image_size = self.adjust_widget_size(15)
        self.log_yellow_circle_image = self.yellow_circle_image.resize(
            (log_adjust_image_size, log_adjust_image_size), Image.LANCZOS
        )
        self.log_yellow_circle_photo = ImageTk.PhotoImage(
            self.log_yellow_circle_image, master=self.parent
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
            self.capture_button.place_forget()
        else:
            self.start_timer_button.config(text="Start Timer")
            # Show Buttons
            self.show_timer_config_buttons()

    def show_timer_config_buttons(self):
        self.decrease_timer_button.place(relx=0.362, rely=0.842, anchor="center")
        self.increase_timer_button.place(relx=0.615, rely=0.842, anchor="center")
        self.decrease_timer10_button.place(relx=0.385, rely=0.842, anchor="center")
        self.increase_timer10_button.place(relx=0.642, rely=0.842, anchor="center")
        self.capture_button.place(relx=0.630, rely=0.882, anchor="center")

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

        # Show Buttons
        self.show_timer_config_buttons()

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
        # if self.timer.is_start:
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
        # if self.timer.is_start:
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

        self.widgets = ScoreBoard(
            self, self.screen_width, self.screen_height, self.timer
        )

        self.title("컨트롤 패널")

        self.widgets.red_button.config(command=self.update_red_score)
        self.widgets.red_button_minus.config(command=self.update_red_decrease)
        self.widgets.red_warning_button.config(command=self.update_red_warning)
        self.widgets.blue_button.config(command=self.update_blue_score)
        self.widgets.blue_button_minus.config(command=self.update_blue_decrease)
        self.widgets.blue_warning_button.config(command=self.update_blue_warning)
        self.widgets.increase_timer_button.config(
            command=lambda: self.update_increase_timer(100)
        )
        self.widgets.decrease_timer_button.config(
            command=lambda: self.update_decrease_timer(100)
        )
        self.widgets.increase_timer10_button.config(
            command=lambda: self.update_increase_timer(1000)
        )
        self.widgets.decrease_timer10_button.config(
            command=lambda: self.update_decrease_timer(1000)
        )
        self.widgets.start_timer_button.config(command=self.update_start_timer)
        self.widgets.reset_timer_button.config(command=self.update_reset_timer)
        self.widgets.capture_button.config(command=self.save_screenshot)
        # Bind the keys
        self.bind("<KeyPress>", self.update_on_key_pressed)

        # Bind the close event to the on_close method
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.widgets.title_entry.bind("<KeyRelease>", self.copy_title_entry)
        self.widgets.red_name_entry.bind("<KeyRelease>", self.copy_red_name_entry)
        self.widgets.blue_name_entry.bind("<KeyRelease>", self.copy_blue_name_entry)
        # self.widgets.weight_entry.bind("<KeyRelease>", self.copy_weight_entry)
        
        self.init_menu()
        self.init_log()
        self.add_round_row()
        
    def init_log(self):
        '''
        점수 로그 화면 표시
          - 시간-행위 쌍으로 표시(01:22 +1)
        '''
        
        #red
        self.red_log_panel = tk.Frame(self.widgets.red_panel, bg='black')
        self.red_log_panel.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.88)
        
        self.red_log_view = ttk.Treeview(self.red_log_panel, columns=("time",), show='tree', style="Red.Treeview")
        
        self.red_log_view.column('#0', width=30, anchor=tk.CENTER)
        self.red_log_view.column("time", width=80, anchor=tk.CENTER)
        
        # Red Treeview 태그 설정
        self.red_log_view.tag_configure('odd_row', background='#FFD1D1')
        self.red_log_view.tag_configure('even_row', background='#FFE8E8')
        self.red_log_view.tag_configure('round_row', background='#8B0000', foreground='white')
        
        self.red_log_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # blue
        self.blue_log_panel = tk.Frame(self.widgets.blue_panel)
        self.blue_log_panel.place(relx=0, rely=0, relwidth=0.15, relheight=0.88)
        
        self.blue_log_view = ttk.Treeview(self.blue_log_panel, columns=("time",), show='tree', style="Blue.Treeview")
        
        self.blue_log_view.column('#0', width=30, anchor=tk.CENTER)
        self.blue_log_view.column("time", width=80, anchor=tk.CENTER)
        
        # Blue Treeview 태그 설정
        self.blue_log_view.tag_configure('odd_row', background='#D1D1FF')
        self.blue_log_view.tag_configure('even_row', background='#E8E8FF')
        self.blue_log_view.tag_configure('round_row', background='#00008B', foreground='white')
        
        self.blue_log_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        style = ttk.Style(root)
        style.theme_use("clam")
        log_font = (
            self.widgets.str_number_font,
            self.widgets.adjust_widget_size(15),
        )
        log_rowheight = self.widgets.adjust_widget_size(30)
        style.configure("Red.Treeview", background="#F5E6D3", foreground="black", fieldbackground="red", font=log_font, rowheight=log_rowheight)
        style.configure("Blue.Treeview", background="#F5E6D3", foreground="black", fieldbackground="blue", font=log_font, rowheight=log_rowheight)
        
    # 아이템을 추가할 때 태그를 적용하는 메서드
    def add_log_item(self, treeview, time, image=None, text=None):
        item_count = len(treeview.get_children())
        tag = 'odd_row' if item_count % 2 == 0 else 'even_row'
        
        if image:
            treeview.insert("", tk.END, values=(time,), image=image, tags=(tag,))
        elif text is not None:
            treeview.insert("", tk.END, values=(time,), text=text, tags=(tag,))
            
    def _add_empty_item(self, treeview):
        item_count = len(treeview.get_children())
        tag = 'odd_row' if item_count % 2 == 0 else 'even_row'
        treeview.insert("", tk.END, values=("",), tags=(tag,))
            
    def balance_log_views(self):
        '''양쪽 log view 높이 맞추기'''
        red_count = len(self.red_log_view.get_children())
        blue_count = len(self.blue_log_view.get_children())
        
        target_count = max(red_count, blue_count)
        
        while len(self.red_log_view.get_children()) < target_count:
            self._add_empty_item(self.red_log_view)
        
        while len(self.blue_log_view.get_children()) < target_count:
            self._add_empty_item(self.blue_log_view)
            
    def add_round_row(self):
        self.balance_log_views()
        
        self.red_log_view.insert("", tk.END, values=('Round',), text=self.widgets.round, tags=('round_row',))
        self.blue_log_view.insert("", tk.END, values=('Round',), text=self.widgets.round, tags=('round_row',))
    
    def init_menu(self):
        '''
        상단 메뉴
        '''
        menubar = tk.Menu(self)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="프로그램 정보", command=self.help_dialog)
        
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.config(menu=menubar)
        self.menubar = menubar
        
        self.help_dialog = None
        
    def help_dialog(self):
        '''
        탭 윈도우
        탭1 제작 및 배포 - 전북합기도 이미지
        탭2 단축키 - 단축키 리스트
        '''
        
        # Check if a help_dialog instance already exists
        if self.help_dialog is not None and self.help_dialog.winfo_exists():
            # If it does, focus on the existing window
            self.help_dialog.focus_force()
            return
        
        self.help_dialog = tk.Toplevel(self)
        self.help_dialog.title("프로그램 정보")
        self.help_dialog.geometry("480x270")  # Set a reasonable initial size
        # Center the dialog on the screen
        self.center_window(self.help_dialog)
            
        notebook = ttk.Notebook(self.help_dialog)

        # 탭 1: 이미지
        tab1 = tk.Frame(notebook)
        image_label = tk.Label(tab1, image=self.widgets.resize_logo_image)
        image_label.pack()

        notebook.add(tab1, text="제작자")

        # 탭 2: 단축키목록
        self.shortcut_data = [
            ("1", "파란색 점수 증가"),
            ("2", "파란색 점수 감소"),
            ("-", "빨간색 점수 증가"),
            ("=", "빨간색 점수 감소"),
            ("4", "파란색 승리 표시 (깜박임)"),
            ("9", "빨간색 승리 표시 (깜박임)"),
            ("스페이스바", "타이머 시작"),
            ("엔터", "전체 화면 모드 전환"),
            ("Esc", "전체 화면 모드 종료"),
        ]
        
        tab2 = tk.Frame(notebook)
        # Create the Treeview with headings
        treeview = ttk.Treeview(tab2, columns=("단축키", "설명"), show="headings")

        # Define column headings
        treeview.heading("단축키", text="단축키")
        treeview.heading("설명", text="설명")

        # Insert shortcut data into Treeview
        for shortcut, description in self.shortcut_data:
            treeview.insert("", tk.END, values=(shortcut, description))

        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        yscrollbar = tk.Scrollbar(tab2)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        treeview.config(yscrollcommand=yscrollbar.set)
        yscrollbar.config(command=treeview.yview)

        notebook.add(tab2, text="단축키")

        notebook.pack(fill=tk.BOTH, expand=True)
                
    def center_window(self, window):
        '''
        help dialog 화면 가운데 위치
        '''
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Get window width and height
        window_width = window.winfo_screenmmwidth()
        window_height = window.winfo_screenmmheight()

        # Calculate center coordinates
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window position
        window.geometry(f"+{x}+{y}")
        

    def init_geometry(self):
        self.geometry(
            f"{self.screen_width}x{self.screen_height}+{self.monitor.x}+{self.monitor.y}"
        )

    def copy_title_entry(self, evnet):
        self.scoreboard.widgets.title_entry.delete(0, tk.END)
        self.scoreboard.widgets.title_entry.insert(0, self.widgets.title_entry.get())

    def copy_red_name_entry(self, event):
        self.scoreboard.widgets.red_name_entry.delete(0, tk.END)
        self.scoreboard.widgets.red_name_entry.insert(
            0, self.widgets.red_name_entry.get()
        )

    def copy_blue_name_entry(self, event):
        self.scoreboard.widgets.blue_name_entry.delete(0, tk.END)
        self.scoreboard.widgets.blue_name_entry.insert(
            0, self.widgets.blue_name_entry.get()
        )

    def copy_weight_entry(self, event):
        self.scoreboard.widgets.weight_entry.delete(0, tk.END)
        self.scoreboard.widgets.weight_entry.insert(0, self.widgets.weight_entry.get())

    def on_close(self):
        # Close both the control panel and the view panel
        self.destroy()
        self.scoreboard.destroy()

        # Terminate the mainloop
        self.master.quit()

    def update_red_score(self):
        self.scoreboard.widgets.red_increase()
        self.widgets.red_increase()
        self.add_log_item(self.red_log_view, self.timer.get_time_remaining(),text="+1")

    def update_red_decrease(self):
        self.scoreboard.widgets.red_decrease()
        self.widgets.red_decrease()
        self.add_log_item(self.red_log_view, self.timer.get_time_remaining(),text="-1")

    def update_red_warning(self):
        self.widgets.red_warning()
        self.scoreboard.widgets.red_warning()
        self.add_log_item(self.red_log_view, self.timer.get_time_remaining(), image=self.widgets.log_yellow_circle_photo)

    def update_blue_score(self):
        self.scoreboard.widgets.blue_increase()
        self.widgets.blue_increase()
        self.add_log_item(self.blue_log_view, self.timer.get_time_remaining(), text="+1")

    def update_blue_decrease(self):
        self.scoreboard.widgets.blue_decrease()
        self.widgets.blue_decrease()
        self.add_log_item(self.blue_log_view, self.timer.get_time_remaining(), text="-1")

    def update_blue_warning(self):
        self.scoreboard.widgets.blue_warning()
        self.widgets.blue_warning()
        self.add_log_item(self.blue_log_view, self.timer.get_time_remaining(), image=self.widgets.log_yellow_circle_photo)

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
            and self.focus_get() != self.widgets.weight_entry
        ):
            key_code = event.keycode
            if key_code == 49:  # 1
                self.update_blue_score()
                # self.widgets.blue_increase()
                # self.scoreboard.widgets.blue_increase()
            elif key_code == 50:  # 2
                self.update_blue_decrease()
                # self.widgets.blue_decrease()
                # self.scoreboard.widgets.blue_decrease()
            elif key_code == 189:  # -
                # self.widgets.red_increase()
                # self.scoreboard.widgets.red_increase()
                self.update_red_score()
            elif key_code == 187:  # =
                # self.widgets.red_decrease()
                # self.scoreboard.widgets.red_decrease()
                self.update_red_decrease()
            elif key_code == 52:  # 4
                self.widgets.blink_winner(6, True)  # Blue Win
                self.scoreboard.widgets.blink_winner(6, True)  # Blue Win
            elif key_code == 57:  # 9
                self.widgets.blink_winner(6, False)  # Red Win
                self.scoreboard.widgets.blink_winner(6, False)  # Red Win
            elif key_code == 32:  # Spacebar
                self.start_timer()
            elif key_code == 13:  # Enter
                self.scoreboard.widgets.toggle_fullscreen(
                    self.scoreboard.overrideredirect()
                )
                self.widgets.toggle_fullscreen(self.overrideredirect())
                
                if self.overrideredirect():
                    self.config(menu="")
                else:
                    self.config(menu=self.menubar)
                
            elif key_code == 27:  # Escape
                self.scoreboard.widgets.toggle_fullscreen(True)
                self.widgets.toggle_fullscreen(True)
                self.config(menu=self.menubar)
                
        elif event.keycode == 13:  # Enter
            self.focus()

    def update_start_timer(self):
        # self.scoreboard.widgets.start_timer()
        self.start_timer()

    def update_reset_timer(self):
        '''
        reset_timer 재정의
        '''
        self.widgets.reset_timer()
        self.scoreboard.reset_timer()
        # delete logs
        self.red_log_view.delete(*self.red_log_view.get_children())
        self.blue_log_view.delete(*self.blue_log_view.get_children())
        # 1R add
        self.add_round_row()

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
                self.widgets.show_start_timer_button(
                    True
                )  # Show 'Stop Timer' and Hide widgets
                self.countdown()
            else:
                self.timer.start(False)
                self.widgets.show_start_timer_button(
                    False
                )  # Show 'Start Timer' and Show widgets
        else:
            # 2라운드 시작
            self.timer.timer_running = False
            self.timer.is_start = False
            self.timer.start_timer_seconds = 3000
            self.timer.timer_seconds = 3000
            self.widgets.update_timer()
            self.scoreboard.widgets.update_timer()
            self.widgets.show_start_timer_button(
                False
            )  # Show 'Start Timer' and Show widgets

    def countdown(self):
        if self.timer.timer_running:
            self.timer.update_timer_seconds()

            if self.timer.timer_seconds > 0:
                self.widgets.update_timer()
                self.scoreboard.widgets.update_timer()
                self.after(10, self.countdown)
            elif self.timer.timer_seconds <= 0:  # 시간 종료로 경기가 끝났을 때
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

                # save_screenshot
                self.save_screenshot()

                # Update round number
                self.widgets.round += 1
                self.widgets.start_timer_button.config(
                    text="{} Round".format(self.widgets.round)
                )
                
                # Add round log
                self.add_round_row()
                

                # Blink the winner's score
                # self.blink_winner(6)  # Blink 3 times (6 because it's a half cycle of blinking)

    def save_screenshot(self):
        """현재 폴더에 스크린샷을 저장한다.
        1. 파일 이름 : title_entry.get() + '_' + weight_entry.get() + '_' + round_entry.get() +
                       '_' + red_name_entry.get() + '_' + red_label.get() + '_' + blue_name_entry.get() + '_' + blue_label.get() + '.png'
        2. 경로 : 현재 폴더
        """

        # Create the file name
        file_name = (
            self.widgets.title_entry.get()
            + "_"
            + self.widgets.weight_entry.get()
            + "_"
            + str(self.widgets.round)
            + "R_"
            + self.widgets.red_name_entry.get()
            + "_"
            + str(self.widgets.red_score)
            + "점_"
            + self.widgets.blue_name_entry.get()
            + "_"
            + str(self.widgets.blue_score)
            + "점.png"
        )

        # Get the handle of the window
        hwnd = self.winfo_id()

        # Get the size of the window
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        # Get the window device context
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # Create a bitmap and select it into the device context
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bitmap)

        # BitBlt the window to the bitmap
        save_dc.BitBlt((0, 0), (w, h), mfc_dc, (0, 0), win32con.SRCCOPY)

        # Save the bitmap to a file
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)
        im = Image.frombuffer(
            "RGB",
            (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
            bmpstr,
            "raw",
            "BGRX",
            0,
            1,
        )

        im.save(file_name)

        # Clean up
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)


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

        self.widgets.weight_entry.place_forget()
        self.widgets.capture_button.place_forget()

        # timer 위젯 위치 조정
        self.widgets.timer_canvas.place(relx=0.5, rely=0.73, anchor="center")

        # 위젯 크기 조정
        self.widgets.red_panel.place(relheight=0.881)
        self.widgets.blue_panel.place(relheight=0.881)

        self.widgets.name_font_size = 80
        self.widgets.name_font = (
            self.widgets.str_font,
            self.widgets.adjust_widget_size(self.widgets.name_font_size),
        )
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

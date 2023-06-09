from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import time

class ScoreBoard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("스코어보드")
        self.geometry("1920x1080")
        self.attributes("-fullscreen", True)  # Add this line to enable fullscreen mode

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.round = 1
        self.red_score = 0
        self.blue_score = 0
        self.timer_seconds = 9000  # 현재 남은 시간

        self.init_time = self.timer_seconds  # 사용자 설정 시작 시간
        self.start_timer_seconds = self.timer_seconds  # 현재 남은 시작 시간
        self.is_start = False  # 시합 시작
        self.str_font = "굴림" # Windows Basic 한글 Font
        self.str_number_font = "Arial" # 숫자 폰트

        # Bind the keys
        self.bind("<KeyPress>", self.on_key_pressed)

        pygame.mixer.init()
        pygame.mixer.music.load(self.resource_path("end_sound.mp3"))

        # Timer
        self.timer_running = False

        # Title text input
        self.title_entry = tk.Entry(
            self,
            font=(self.str_font, self.adjust_widget_size(80), "bold"),
            fg="white",
            bg="black",
            justify="center",
        )
        self.title_entry.place(
            relx=0.5, rely=0.06, anchor="center", relwidth=1.0, relheight=0.13
        )
        # Set initial text
        initial_text = "합기도대회"
        self.title_entry.insert(0, initial_text)

        # Red score panel
        self.red_panel = tk.Frame(self, bg="red")
        self.red_panel.place(relx=0, rely=0.12, relwidth=0.5, relheight=0.7)

        self.red_label = tk.Label(
            self.red_panel,
            text="{}".format(self.red_score),
            fg="white",
            bg="red",
            font=(self.str_number_font, self.adjust_widget_size(350)),
        )
        self.red_label.pack(anchor="center",pady=20, padx=20)

        # Warning buttons
        self.red_warning_button = tk.Button(
            self,
            text="경고",
            command=self.red_warning,
            font=(self.str_font, self.adjust_widget_size(40)),
        )
        self.red_warning_button.place(relx=0.05, rely=0.9, anchor="center")

        # Warning circles
        self.yellow_circle_image = Image.open(self.resource_path("yellow_circle.png"))
        adjust_image_size = self.adjust_widget_size(80)
        self.yellow_circle_image = self.yellow_circle_image.resize(
            (adjust_image_size, adjust_image_size), Image.LANCZOS
        )
        self.yellow_circle_photo = ImageTk.PhotoImage(self.yellow_circle_image)

        self.red_circle_image = Image.open(self.resource_path("red_circle.png"))
        self.red_circle_image = self.red_circle_image.resize(
            (adjust_image_size, adjust_image_size), Image.LANCZOS
        )
        self.red_circle_photo = ImageTk.PhotoImage(self.red_circle_image)

        self.red_warning_box = tk.Frame(self.red_panel, bg="black")
        self.red_warning_box.place(
            relx=0.48, rely=0.8, relwidth=0.4, relheight=0.12, anchor="center"
        )

        self.red_yellow_circle = tk.Label(self.red_panel, bg="black")
        self.red_yellow_circle.place(relx=0.35, rely=0.8, anchor="center")

        self.red_red_circle1 = tk.Label(self.red_panel, bg="black")
        self.red_red_circle1.place(relx=0.47, rely=0.8, anchor="center")

        self.red_red_circle2 = tk.Label(self.red_panel, bg="black")
        self.red_red_circle2.place(relx=0.59, rely=0.8, anchor="center")

        # Warning state
        self.red_warning_state = 0

        # Name text input
        self.red_name_entry = tk.Entry(
            self.red_panel,
            font=(self.str_font, self.adjust_widget_size(60)),
            fg="white",
            bg="black",
            justify="center",
            width=self.adjust_widget_size(50),
        )
        self.red_name_entry.pack(anchor="center", side="bottom", pady=0, padx=0)
        # Set initial text
        initial_red_name_text = "홍길동"
        self.red_name_entry.insert(0, initial_red_name_text)

        # Blue score panel
        self.blue_panel = tk.Frame(self, bg="blue")
        self.blue_panel.place(relx=0.5, rely=0.12, relwidth=0.5, relheight=0.7)

        self.blue_label = tk.Label(
            self.blue_panel,
            text="{}".format(self.blue_score),
            fg="white",
            bg="blue",
            font=(self.str_number_font, self.adjust_widget_size(350)),
        )
        self.blue_label.pack(anchor="center", pady=20, padx=20)

        # Warning buttons
        self.blue_warning_button = tk.Button(
            self,
            text="경고",
            command=self.blue_warning,
            font=(self.str_font, self.adjust_widget_size(40)),
        )
        self.blue_warning_button.place(relx=0.95, rely=0.9, anchor="center")

        # Warning circles
        self.blue_warning_box = tk.Frame(self.blue_panel, bg="black")
        self.blue_warning_box.place(
            relx=0.52, rely=0.8, relwidth=0.4, relheight=0.12, anchor="center"
        )

        self.blue_yellow_circle = tk.Label(self.blue_panel, bg="black")
        self.blue_yellow_circle.place(relx=0.39, rely=0.8, anchor="center")

        self.blue_red_circle1 = tk.Label(self.blue_panel, bg="black")
        self.blue_red_circle1.place(relx=0.51, rely=0.8, anchor="center")

        self.blue_red_circle2 = tk.Label(self.blue_panel, bg="black")
        self.blue_red_circle2.place(relx=0.64, rely=0.8, anchor="center")

        # Warning state
        self.blue_warning_state = 0

        # Name text input
        self.blue_name_entry = tk.Entry(
            self.blue_panel,
            font=(self.str_font, self.adjust_widget_size(60)),
            fg="white",
            bg="black",
            justify="center",
            width=self.adjust_widget_size(50),
        )
        self.blue_name_entry.pack(anchor="center", side="bottom", pady=0, padx=0)
        # Set initial text
        initial_blue_name_text = "청길동"
        self.blue_name_entry.insert(0, initial_blue_name_text)

        # Timer
        self.time_remaining = tk.StringVar()
        minutes = self.timer_seconds // 6000
        seconds = (self.timer_seconds % 6000) // 100
        ms = self.timer_seconds % 100
        self.time_remaining.set("{:02d}:{:02d}.{:02d}".format(minutes, seconds, ms))

        label_width = self.adjust_widget_size(540)
        label_height = self.adjust_widget_size(175)

        self.timer_canvas = tk.Canvas(
            self,
            width=label_width,
            height=label_height,
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
            font=(self.str_number_font, self.adjust_widget_size(100)),
            bg="white",
        )
        self.timer_label.place(
            x=(label_width // 2), y=(label_height // 2), anchor="center"
        )

        self.increase_timer_button = tk.Button(
            self,
            text="-1",
            command=lambda: self.decrease_timer(100),
            font=(self.str_number_font, self.adjust_widget_size(13)),
        )
        self.increase_timer_button.place(relx=0.362, rely=0.842, anchor="center")

        self.decrease_timer_button = tk.Button(
            self,
            text="+1",
            command=lambda: self.increase_timer(100),
            font=(self.str_number_font, self.adjust_widget_size(13)),
        )
        self.decrease_timer_button.place(relx=0.615, rely=0.842, anchor="center")

        self.increase_timer10_button = tk.Button(
            self,
            text="-10",
            command=lambda: self.decrease_timer(1000),
            font=(self.str_number_font, self.adjust_widget_size(13)),
        )
        self.increase_timer10_button.place(relx=0.385, rely=0.842, anchor="center")

        self.decrease_timer10_button = tk.Button(
            self,
            text="+10",
            command=lambda: self.increase_timer(1000),
            font=(self.str_number_font, self.adjust_widget_size(13)),
        )
        self.decrease_timer10_button.place(relx=0.642, rely=0.842, anchor="center")

        # Buttons
        self.red_button = tk.Button(
            self,
            text="+1",
            command=self.red_increase,
            font=(self.str_number_font, self.adjust_widget_size(60)),
            fg="red",
        )
        self.red_button.place(relx=0.18, rely=0.9, anchor="center")

        self.red_button_minus = tk.Button(
            self,
            text="-1",
            command=self.red_decrease,
            font=(self.str_number_font, self.adjust_widget_size(60)),
            fg="red",
        )
        self.red_button_minus.place(relx=0.29, rely=0.9, anchor="center")

        self.blue_button = tk.Button(
            self,
            text="+1",
            command=self.blue_increase,
            font=(self.str_number_font, self.adjust_widget_size(60)),
            fg="blue",
        )
        self.blue_button.place(relx=0.72, rely=0.9, anchor="center")

        self.blue_button_minus = tk.Button(
            self,
            text="-1",
            command=self.blue_decrease,
            font=(self.str_number_font, self.adjust_widget_size(60)),
            fg="blue",
        )
        self.blue_button_minus.place(relx=0.827, rely=0.9, anchor="center")

        # Start timer button
        self.start_timer_button = tk.Button(
            self,
            text="Start Timer",
            command=self.start_timer,
            font=(self.str_number_font, self.adjust_widget_size(45)),
        )
        self.start_timer_button.place(relx=0.5, rely=0.88, anchor="center")

        # Reset timer button
        self.reset_timer_button = tk.Button(
            self,
            text="Reset",
            command=self.reset_timer,
            font=(self.str_number_font, self.adjust_widget_size(15)),
        )
        self.reset_timer_button.place(relx=0.5, rely=0.96, anchor="center")

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
        minutes = self.timer_seconds // 6000
        seconds = (self.timer_seconds % 6000) // 100
        ms = self.timer_seconds % 100

        if minutes > 0:
            self.time_remaining.set("{:02d}:{:02d}.{:02d}".format(minutes, seconds, ms))
        else:
            self.time_remaining.set("{:02d}.{:02d}".format(seconds, ms))

        self.timer_label.update_idletasks()  # Update only the timer label widget

    def start_timer(self):
        if self.start_timer_seconds > 0:
            self.focus()

            if not self.timer_running:
                self.timer_running = True
                self.is_start = True
                self.start_timer_button.config(text="Stop Timer")
                self.start_time = time.time()  # Save the current time

                self.countdown()

                # Hide Button
                self.increase_timer_button.place_forget()
                self.decrease_timer_button.place_forget()
                self.increase_timer10_button.place_forget()
                self.decrease_timer10_button.place_forget()
            else:
                self.timer_running = False
                self.start_timer_button.config(text="Start Timer")
                self.start_timer_seconds = self.timer_seconds
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
        else:
            self.timer_running = False
            self.start_timer_button.config(text="Start Timer")
            self.start_timer_seconds = 3000
            self.timer_seconds = 3000
            self.update_timer()
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

    def countdown(self):
        if self.timer_running:
            elapsed_time = int(
                (time.time() - self.start_time) * 100
            )  # Calculate the elapsed time in milliseconds
            self.timer_seconds = (
                self.start_timer_seconds - elapsed_time
            )  # Update the timer seconds

            if self.timer_seconds > 0:
                self.update_timer()
                self.after(10, self.countdown)
            elif self.timer_seconds <= 0: # 시간 종료로 경기가 끝났을 때
                # 다음 라운드 준비
                self.round += 1
                self.start_timer_button.config(text="{} Round".format(self.round))
                # Reset Timer Button
                self.timer_running = False
                self.is_start = False
                self.start_timer_seconds = 0
                self.timer_seconds = 0
                self.update_timer()

                # Play an MP3 file when the timer ends
                pygame.mixer.music.play()
                
                # Blink the winner's score
                # self.blink_winner(6)  # Blink 3 times (6 because it's a half cycle of blinking)

    def reset_timer(self):
        self.timer_seconds = self.init_time
        self.start_timer_seconds = self.init_time
        self.update_timer()

        # Reset scores
        self.round = 1
        self.red_score = 0
        self.blue_score = 0
        self.red_label.config(text="{}".format(self.red_score))
        self.blue_label.config(text="{}".format(self.blue_score))
        self.red_warning_state = -1
        self.blue_warning_state = -1
        
        self.is_start = True # 경고 상태 초기화
        self.red_warning()
        self.blue_warning()

        # Reset Timer Button
        self.timer_running = False
        self.is_start = False
        self.start_timer_button.config(text="Start Timer")

        # Show Button
        self.increase_timer_button.place(relx=0.362, rely=0.842, anchor="center")
        self.decrease_timer_button.place(relx=0.615, rely=0.842, anchor="center")
        self.increase_timer10_button.place(relx=0.385, rely=0.842, anchor="center")
        self.decrease_timer10_button.place(relx=0.642, rely=0.842, anchor="center")

    def increase_timer(self, time):
        self.timer_seconds += time
        self.start_timer_seconds = self.timer_seconds
        if not self.is_start:
            self.init_time = self.timer_seconds
        self.update_timer()

    def decrease_timer(self, time):
        if (self.timer_seconds - time) > 0:
            self.timer_seconds -= time
            self.start_timer_seconds = self.timer_seconds
            if not self.is_start:
                self.init_time = self.timer_seconds
            self.update_timer()

    def red_warning(self):
        if self.is_start:
            self.red_warning_state += 1

            if self.red_warning_state == 1:
                self.red_yellow_circle.config(image=self.yellow_circle_photo)
                self.red_red_circle1.config(image="")
                self.red_red_circle2.config(image="")
            elif self.red_warning_state == 2:
                self.red_yellow_circle.config(image="")
                self.red_red_circle1.config(image=self.red_circle_photo)
                self.red_red_circle2.config(image="")
            elif self.red_warning_state == 3:
                self.red_yellow_circle.config(image=self.yellow_circle_photo)
                self.red_red_circle1.config(image=self.red_circle_photo)
                self.red_red_circle2.config(image="")
            elif self.red_warning_state == 4:
                self.red_yellow_circle.config(image="")
                self.red_red_circle1.config(image=self.red_circle_photo)
                self.red_red_circle2.config(image=self.red_circle_photo)
            else:
                self.red_warning_state = 0
                self.red_yellow_circle.config(image="")
                self.red_red_circle1.config(image="")
                self.red_red_circle2.config(image="")

    def blue_warning(self):
        if self.is_start:
            self.blue_warning_state += 1

            if self.blue_warning_state == 1:
                self.blue_yellow_circle.config(image=self.yellow_circle_photo)
                self.blue_red_circle1.config(image="")
                self.blue_red_circle2.config(image="")
            elif self.blue_warning_state == 2:
                self.blue_yellow_circle.config(image="")
                self.blue_red_circle1.config(image=self.red_circle_photo)
                self.blue_red_circle2.config(image="")
            elif self.blue_warning_state == 3:
                self.blue_yellow_circle.config(image=self.yellow_circle_photo)
                self.blue_red_circle1.config(image=self.red_circle_photo)
                self.blue_red_circle2.config(image="")
            elif self.blue_warning_state == 4:
                self.blue_yellow_circle.config(image="")
                self.blue_red_circle1.config(image=self.red_circle_photo)
                self.blue_red_circle2.config(image=self.red_circle_photo)
            else:
                self.blue_warning_state = 0
                self.blue_yellow_circle.config(image="")
                self.blue_red_circle1.config(image="")
                self.blue_red_circle2.config(image="")

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

    # Key event handlers
    def on_key_pressed(self, event):
        if (
            self.focus_get() != self.title_entry
            and self.focus_get() != self.red_name_entry
            and self.focus_get() != self.blue_name_entry
        ):
            key_code = event.keycode
            if key_code == 49:  # 1
                self.red_increase()
            elif key_code == 50:  # 2
                self.red_decrease()
            elif key_code == 189:  # -
                self.blue_increase()
            elif key_code == 187:  # =
                self.blue_decrease()
            elif key_code == 52:  # 4
                self.blink_winner(6, False) # Red Win
            elif key_code == 57:  # 9
                self.blink_winner(6, True) # Blue Win
            elif key_code == 32:  # Spacebar
                self.start_timer()
            elif key_code == 13:  # Enter
                self.attributes("-fullscreen", not self.attributes('-fullscreen'))
            elif key_code == 27:  # Escape
                self.attributes("-fullscreen", False)
        elif event.keycode == 13:  # Enter
            self.focus()
    
    def blink_winner(self, count, is_blue_win):
        if count <= 0:
            self.red_label.config(fg="white")
            self.blue_label.config(fg="white")
            self.update_idletasks()
            return

        if is_blue_win:
            self.blue_label.config(fg="yellow" if self.blue_label.cget("fg") == "white" else "white")
        else:
            self.red_label.config(fg="yellow" if self.red_label.cget("fg") == "white" else "white")

        self.update_idletasks()
        self.after(500, self.blink_winner, count - 1, is_blue_win)

if __name__ == "__main__":
    app = ScoreBoard()
    app.mainloop()

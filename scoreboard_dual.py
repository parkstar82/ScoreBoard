from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk, UnidentifiedImageError
import screeninfo
from timer import Timer

import win32gui
import win32ui
import win32con


class ScoreBoard:
    def __init__(self, parent, screen_width, screen_height, timer, timer_rest):
        self.parent = parent
        self.parent.configure(bg="gray100")
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.timer = timer
        self.timer_rest = timer_rest

        self.round = 1
        self.red_score = 0
        self.blue_score = 0
        self.str_font = "굴림"  # Windows Basic 한글 Font
        # self.str_font = "Arial"  # Windows Basic 한글 Font
        self.str_number_font = "Arial"  # 숫자 폰트

        # Const
        self.title_font_size = 80
        self.score_label_font_size = 350
        self.warning_font_size = 60
        self.name_font_size = 60
        self.weight_font_size = 43
        self.timer_1_10_button_font_size = 13
        self.plus_minus_button_font_size = 60
        self.timer_button_font_size = 45
        self.btn_timer_reset_font_size = 15
        self.timer_label_width_size = 540
        self.timer_label_height_size = 175
        self.timer_label_font_size = 100
        self.control_btn_frame_width = 160
        self.control_btn_frame_height = 120
        self.start_timer_btn_width = 320
        self.start_timer_btn_height = 100
        self.util_icon_btn_size = 30
        self.util_icon_btn_frame_size = 50
        self.is_rest = False
        self.timer_canvas_rely = 0.532
        self.timer_canvas_rest_rely = 0.332

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
            "bold",
        )
        self.name_font = (
            self.str_font,
            self.adjust_widget_size(self.name_font_size),
        )
        self.weight_font = (
            self.str_font,
            self.adjust_widget_size(self.weight_font_size),
        )
        self.timer_1_10_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_1_10_button_font_size),
            "bold",
        )
        self.plus_minus_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.plus_minus_button_font_size),
            "bold",
        )
        self.timer_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_button_font_size),
            "bold",
        )
        self.btn_timer_reset_font = (
            self.str_number_font,
            self.adjust_widget_size(self.btn_timer_reset_font_size),
            "bold",
        )
        self.timer_label_width = self.adjust_widget_size(self.timer_label_width_size)
        self.timer_label_height = self.adjust_widget_size(self.timer_label_height_size)
        self.timer_label_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_label_font_size),
        )
        self.control_btn_frame_width = self.adjust_widget_size(
            self.control_btn_frame_width
        )
        self.control_btn_frame_height = self.adjust_widget_size(
            self.control_btn_frame_height
        )
        self.start_timer_btn_width = self.adjust_widget_size(self.start_timer_btn_width)
        self.start_timer_btn_height = self.adjust_widget_size(
            self.start_timer_btn_height
        )
        self.util_icon_btn_size = self.adjust_widget_size(self.util_icon_btn_size)

        # Load end sound
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.resource_path("end_sound.mp3"))
        except ImportError:
            print(
                "Warning: Pygame not installed. Sound disabled. Install using: pip install pygame",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Warning: Could not initialize sound. Error: {e}", file=sys.stderr)

        # Warning circles
        self.load_images()
        self.load_utility_images()
        self.create_widgets()

        # Hide 휴식 타이머
        self.toggle_rest_mode()

        # resize windows event bind
        self.parent.bind("<Configure>", self.on_resize)

    def create_widgets(self):
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

        self.red_score_label = tk.Label(
            self.red_panel,
            text="{}".format(self.red_score),
            fg="white",
            bg="red",
            font=self.score_label_font,
        )
        self.red_score_label.place(relx=0.5, rely=0.4, anchor="center")

        self.red_warning_box = tk.Frame(self.red_panel, bg="black")
        self.red_warning_box.place(
            relx=0.5, rely=0.8, relwidth=0.4, relheight=0.12, anchor="center"
        )

        self.red_yellow_circle = tk.Label(self.red_warning_box, bg="black")
        self.red_red_circle = tk.Label(self.red_warning_box, bg="black")
        self.red_yellow_circle.config(image=self.yellow_circle_photo)
        self.red_red_circle.config(image=self.red_circle_photo)
        self.red_yellow_circle.place(relx=0.15, rely=0.5, anchor="center")
        self.red_red_circle.place(relx=0.15, rely=0.5, anchor="center")

        self.red_red_circle1 = tk.Label(self.red_warning_box, bg="black")
        self.red_yellow_circle1 = tk.Label(self.red_warning_box, bg="black")
        self.red_yellow_circle1.config(image=self.yellow_circle_photo)
        self.red_red_circle1.config(image=self.red_circle_photo)
        self.red_yellow_circle1.place(relx=0.5, rely=0.5, anchor="center")
        self.red_red_circle1.place(relx=0.5, rely=0.5, anchor="center")

        self.red_red_circle2 = tk.Label(self.red_warning_box, bg="black")
        self.red_yellow_circle2 = tk.Label(self.red_warning_box, bg="black")
        self.red_yellow_circle2.config(image=self.yellow_circle_photo)
        self.red_red_circle2.config(image=self.red_circle_photo)
        self.red_yellow_circle2.place(relx=0.85, rely=0.5, anchor="center")
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

        self.blue_score_label = tk.Label(
            self.blue_panel,
            text="{}".format(self.blue_score),
            fg="white",
            bg="blue",
            font=self.score_label_font,
        )
        self.blue_score_label.place(relx=0.5, rely=0.4, anchor="center")

        # Warning circles
        self.blue_warning_box = tk.Frame(self.blue_panel, bg="black")
        self.blue_warning_box.place(
            relx=0.5, rely=0.8, relwidth=0.4, relheight=0.12, anchor="center"
        )

        self.blue_yellow_circle = tk.Label(self.blue_warning_box, bg="black")
        self.blue_red_circle = tk.Label(self.blue_warning_box, bg="black")
        self.blue_yellow_circle.config(image=self.yellow_circle_photo)
        self.blue_red_circle.config(image=self.red_circle_photo)
        self.blue_yellow_circle.place(relx=0.15, rely=0.5, anchor="center")
        self.blue_red_circle.place(relx=0.15, rely=0.5, anchor="center")

        self.blue_yellow_circle1 = tk.Label(self.blue_warning_box, bg="black")
        self.blue_red_circle1 = tk.Label(self.blue_warning_box, bg="black")
        self.blue_yellow_circle1.config(image=self.yellow_circle_photo)
        self.blue_red_circle1.config(image=self.red_circle_photo)
        self.blue_yellow_circle1.place(relx=0.5, rely=0.5, anchor="center")
        self.blue_red_circle1.place(relx=0.5, rely=0.5, anchor="center")

        self.blue_yellow_circle2 = tk.Label(self.blue_warning_box, bg="black")
        self.blue_red_circle2 = tk.Label(self.blue_warning_box, bg="black")
        self.blue_yellow_circle2.config(image=self.yellow_circle_photo)
        self.blue_red_circle2.config(image=self.red_circle_photo)
        self.blue_yellow_circle2.place(relx=0.85, rely=0.5, anchor="center")
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

        # 경기 타이머
        self.init_timer_label()

        # 휴식 타이머
        self.init_timer_rest_label()

        # 체급
        self.init_weight_entry()

        self.control_frame = tk.Frame(
            self.parent, bg="lightgray", pady=5, padx=10
        )  # Dark background
        self.control_frame.place(
            relx=0.5, rely=0.915, anchor="center", relwidth=1.0, relheight=0.19
        )

        # --- Configure grid with 5 columns inside control_frame ---
        # Column 0: Blue controls (fixed width)
        # Column 1: Empty expanding space
        # Column 2: Timer controls (fixed width)
        # Column 3: Empty expanding space
        # Column 4: Red controls (fixed width)
        self.control_frame.grid_columnconfigure(0, weight=0)
        self.control_frame.grid_columnconfigure(1, weight=1)  # Expanding space
        self.control_frame.grid_columnconfigure(2, weight=0)
        self.control_frame.grid_columnconfigure(3, weight=1)  # Expanding space
        self.control_frame.grid_columnconfigure(4, weight=0)
        self.control_frame.grid_rowconfigure(0, weight=1)

        # Blue controls
        self.blue_control_frame = tk.Frame(self.control_frame, bg="lightgray")
        self.blue_control_frame.grid(
            row=0, column=0, sticky="ns"
        )  # Use grid, sticky stretches horizontally
        # Inner frame to hold the blue buttons, centered within blue_control_frame
        self.blue_buttons_inner_frame = tk.Frame(
            self.blue_control_frame, bg="lightgray"
        )
        # Pack the inner frame so it stays centered
        self.blue_buttons_inner_frame.pack(
            anchor="e", expand=True
        )  # expand=True helps centering

        # Helper function to create buttons within fixed-size frames
        def create_framed_button(parent, command, text, btn_font, bg_color, fg_color):
            frame = tk.Frame(
                parent,
                width=self.control_btn_frame_width,
                height=self.control_btn_frame_height,
                bg=parent.cget("bg"),
            )
            frame.pack_propagate(False)  # Prevent frame from shrinking to button size
            frame.pack(side=tk.LEFT, padx=4, pady=5)  # Pack the frame

            button = tk.Button(
                frame,
                text=text,
                command=command,
                font=btn_font,
                bg=bg_color,
                fg=fg_color,
                bd=1,  # Optional: border
                relief=tk.RAISED,  # Optional: border style
                # width/height options removed from button - frame controls size
            )
            # Pack button to fill the frame
            button.pack(fill=tk.BOTH, expand=True)
            return frame, button  # Return both if needed

        # Create Blue buttons using the helper
        _, self.blue_warning_button = create_framed_button(
            self.blue_buttons_inner_frame,
            self.blue_warning,
            "경고",
            self.warning_font,
            "#ffff00",
            "black",
        )
        _, self.btn_blue_plus = create_framed_button(
            self.blue_buttons_inner_frame,
            self.blue_increase,
            "+1",
            self.plus_minus_button_font,
            "blue",
            "white",
        )
        _, self.btn_blue_minus = create_framed_button(
            self.blue_buttons_inner_frame,
            self.blue_decrease,
            "-1",
            self.plus_minus_button_font,
            "#8080ff",
            "white",
        )

        # Timer controls
        self.timer_control_frame = tk.Frame(self.control_frame, bg="lightgray")
        # Place timer controls in the center column (1) of the grid
        self.timer_control_frame.grid(row=0, column=2, padx=10)
        self.timer_adj_minus_frame = tk.Frame(self.timer_control_frame, bg="lightgray")
        self.btn_timer_minus_1 = tk.Button(
            self.timer_adj_minus_frame,
            text="-1",
            command=lambda: self.update_timer(),
            font=self.timer_1_10_button_font,
            bg="gray50",
            fg="white",
            width=4,
        )
        self.btn_timer_minus_10 = tk.Button(
            self.timer_adj_minus_frame,
            text="-10",
            command=lambda: self.update_timer(),
            font=self.timer_1_10_button_font,
            bg="gray50",
            fg="white",
            width=4,
        )
        self.btn_timer_minus_10.pack(pady=1)
        self.btn_timer_minus_1.pack(pady=1)

        # utility buttons
        # |-------------------|
        # |  btn_start_timer  |
        # |-------------------|
        # | rest|capture|reset|
        # |-------------------|
        # Capture button
        self.timer_util_frame = tk.Frame(self.timer_control_frame, bg="lightgray")
        # Configure grid inside utility frame
        self.timer_util_frame.grid_columnconfigure(
            (0, 1, 2), weight=1, uniform="util_buttons"
        )  # uniform makes columns equal width
        self.timer_util_frame.grid_rowconfigure(0, weight=0)  # Start button row
        self.timer_util_frame.grid_rowconfigure(1, weight=0)  # Icon buttons row
        self.timer_util_frame.grid_rowconfigure(
            1, minsize=self.util_icon_btn_frame_size + 2
        )

        # Helper function specifically for utility buttons in frames
        def create_util_button_in_frame(
            parent_grid,
            row,
            col,
            command,
            image_photo,
            bg_color,
            frame_width,
            frame_height,
            colspan=1,
        ):
            # Frame to control the size, placed in the grid
            frame = tk.Frame(
                parent_grid,
                width=frame_width,
                height=frame_height,
                bg="gray20",
            )
            frame.pack_propagate(False)
            frame.grid(
                row=row, column=col, columnspan=colspan, sticky="nsew", padx=1, pady=1
            )

            # Button inside the frame
            button = tk.Button(
                frame,
                image=image_photo,
                command=command,
                bg="gray35",
                bd=0,
                relief=tk.FLAT,
                activebackground="gray20",
            )
            # Assign fallback text/color if image failed to load
            if image_photo is None:
                # Simple fallback text
                fallback_text = "?"
                if command == self.rest_timer:
                    fallback_text = "P"
                elif command == self.reset_timer:
                    fallback_text = "R"
                # elif command == self.capture_action: fallback_text = "C" # If capture had command
                button.config(
                    text=fallback_text,
                    font=self.timer_1_10_button_font,
                    fg="white",
                    relief=tk.RAISED,
                    bd=1,
                )

            button.pack(fill=tk.BOTH, expand=True)
            return frame, button

        # Create Start timer button (still text) - using its own frame for size control
        start_frame = tk.Frame(
            self.timer_util_frame,
            width=self.start_timer_btn_width,
            height=self.start_timer_btn_height,
            bg=self.timer_util_frame.cget("bg"),
        )
        start_frame.pack_propagate(False)
        start_frame.grid(
            row=0, column=0, columnspan=3, sticky="nsew", padx=1, pady=(0, 2)
        )
        self.btn_start_timer = tk.Button(
            start_frame,
            text="시작",
            font=self.timer_button_font,
            bg="#16a34a",
            fg="white",
            bd=1,
            relief=tk.RAISED,
        )
        self.btn_start_timer.pack(fill=tk.BOTH, expand=True)

        self.btn_start_timer_rest = tk.Button(
            start_frame,
            text="휴식",
            font=self.timer_button_font,
            bg="#16a34a",
            fg="white",
            bd=1,
            relief=tk.RAISED,
        )
        self.btn_start_timer_rest.pack(fill=tk.BOTH, expand=True)

        # Create Icon utility buttons using the helper
        self.btn_timer_rest_frame, self.btn_timer_rest = create_util_button_in_frame(
            self.timer_util_frame,
            1,
            0,
            None,
            self.pause_icon_photo,
            "#9333ea",
            self.util_icon_btn_frame_size,
            self.util_icon_btn_frame_size,
        )
        self.btn_capture_frame, self.btn_capture = create_util_button_in_frame(
            self.timer_util_frame,
            1,
            1,
            None,
            self.camera_icon_photo,
            "#9333ea",
            self.util_icon_btn_frame_size,
            self.util_icon_btn_frame_size,
        )
        self.btn_timer_reset_frame, self.btn_timer_reset = create_util_button_in_frame(
            self.timer_util_frame,
            1,
            2,
            self.reset_timer,
            self.reset_icon_photo,
            "#9333ea",
            self.util_icon_btn_frame_size,
            self.util_icon_btn_frame_size,
        )

        # Timer adjust plus frame
        self.timer_adj_plus_frame = tk.Frame(self.timer_control_frame, bg="lightgray")
        self.btn_timer_plus_1 = tk.Button(
            self.timer_adj_plus_frame,
            text="+1",
            command=lambda: self.update_timer(),
            font=self.timer_1_10_button_font,
            bg="gray50",
            fg="white",
            width=4,
        )
        self.btn_timer_plus_10 = tk.Button(
            self.timer_adj_plus_frame,
            text="+10",
            command=lambda: self.update_timer(),
            font=self.timer_1_10_button_font,
            bg="gray50",
            fg="white",
            width=4,
        )
        # Pack order reversed for visual layout (+1 on top)
        self.btn_timer_plus_10.pack(pady=1)
        self.btn_timer_plus_1.pack(pady=1)

        # Pack the timer control sub-frames (using pack is fine here)
        self.timer_adj_minus_frame.pack(side=tk.LEFT, padx=5, fill="y", anchor="w")
        self.timer_util_frame.pack(
            side=tk.LEFT, padx=5, fill="both", expand=True
        )  # Allow util frame to expand
        self.timer_adj_plus_frame.pack(side=tk.LEFT, padx=5, fill="y", anchor="e")

        # Red controls
        self.red_control_frame = tk.Frame(self.control_frame, bg="lightgray")
        self.red_control_frame.grid(
            row=0, column=4, sticky="ns"
        )  # Sticky fills the cell

        # Inner frame to hold the red buttons, centered within red_control_frame
        self.red_buttons_inner_frame = tk.Frame(self.red_control_frame, bg="lightgray")
        # Pack the inner frame so it stays centered
        self.red_buttons_inner_frame.pack(anchor="w", expand=True)

        # Create Red buttons inside the red_buttons_inner_frame
        _, self.btn_red_plus = create_framed_button(
            self.red_buttons_inner_frame,
            self.red_increase,
            "+1",
            self.plus_minus_button_font,
            "red",
            "white",
        )
        _, self.btn_red_minus = create_framed_button(
            self.red_buttons_inner_frame,
            self.red_decrease,
            "-1",
            self.plus_minus_button_font,
            "#F08080",
            "white",
        )
        _, self.red_warning_button = create_framed_button(
            self.red_buttons_inner_frame,
            self.red_warning,
            "경고",
            self.warning_font,
            "#ffff00",
            "black",
        )

    def on_resize(self, event):
        """
        Handle window resize events and adjust widget sizes accordingly.
        """
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
            "bold",
        )
        self.name_font = (
            self.str_font,
            self.adjust_widget_size(self.name_font_size),
        )
        self.weight_font = (
            self.str_font,
            self.adjust_widget_size(self.weight_font_size),
        )
        self.timer_1_10_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_1_10_button_font_size),
            "bold",
        )
        self.plus_minus_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.plus_minus_button_font_size),
            "bold",
        )
        self.timer_button_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_button_font_size),
            "bold",
        )
        self.btn_timer_reset_font = (
            self.str_number_font,
            self.adjust_widget_size(self.btn_timer_reset_font_size),
            "bold",
        )
        self.timer_label_width = self.adjust_widget_size(self.timer_label_width_size)
        self.timer_label_height = self.adjust_widget_size(self.timer_label_height_size)
        self.timer_label_font = (
            self.str_number_font,
            self.adjust_widget_size(self.timer_label_font_size),
        )
        self.control_btn_frame_width = self.adjust_widget_size(
            self.control_btn_frame_width
        )
        self.control_btn_frame_height = self.adjust_widget_size(
            self.control_btn_frame_height
        )
        self.start_timer_btn_width = self.adjust_widget_size(self.start_timer_btn_width)
        self.start_timer_btn_height = self.adjust_widget_size(
            self.start_timer_btn_height
        )
        self.util_icon_btn_size = self.adjust_widget_size(self.util_icon_btn_size)

        self.title_entry.config(font=self.title_font)
        self.red_score_label.config(font=self.score_label_font)
        self.blue_score_label.config(font=self.score_label_font)
        self.red_warning_button.config(font=self.warning_font)
        self.blue_warning_button.config(font=self.warning_font)
        self.red_name_entry.config(font=self.name_font)
        self.blue_name_entry.config(font=self.name_font)
        self.weight_entry.config(font=self.weight_font)
        self.btn_timer_plus_1.config(font=self.timer_1_10_button_font)
        self.btn_timer_minus_1.config(font=self.timer_1_10_button_font)
        self.btn_timer_plus_10.config(font=self.timer_1_10_button_font)
        self.btn_timer_minus_10.config(font=self.timer_1_10_button_font)
        self.btn_capture.config(font=self.btn_timer_reset_font)
        self.btn_red_plus.config(font=self.plus_minus_button_font)
        self.btn_red_minus.config(font=self.plus_minus_button_font)
        self.btn_blue_plus.config(font=self.plus_minus_button_font)
        self.btn_blue_minus.config(font=self.plus_minus_button_font)
        self.btn_start_timer.config(font=self.timer_button_font)
        self.btn_timer_reset.config(font=self.btn_timer_reset_font)

        # 메인 타이머
        self.timer_canvas.config(
            width=self.timer_label_width, height=self.timer_label_height
        )
        self.timer_label.config(font=self.timer_label_font)
        self.timer_label.place(
            x=(self.timer_label_width // 2),
            y=(self.timer_label_height // 2),
            anchor="center",
        )
        # 휴식 타이머
        self.timer_canvas_rest.config(
            width=self.timer_label_width, height=self.timer_label_height
        )
        self.timer_label_rest.config(font=self.timer_label_font)
        self.timer_label_rest.place(
            x=(self.timer_label_width // 2),
            y=(self.timer_label_height // 2),
            anchor="center",
        )

    def init_timer_label(self):
        """
        Initialize the timer label widget.
        """
        # Timer
        self.time_remaining = tk.StringVar(self.parent)
        self.time_remaining.set(timer.get_time_remaining())

        self.timer_canvas = tk.Canvas(
            self.parent,
            width=self.timer_label_width,
            height=self.timer_label_height,
            bg="white",
            bd=0,
            relief="solid",
            highlightthickness=2,
            highlightbackground="yellow",
            highlightcolor="yellow",
        )
        self.timer_canvas.place(relx=0.5, rely=self.timer_canvas_rely, anchor="center")

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

    def init_timer_rest_label(self):
        """
        Initialize the rest timer label widget.
        """
        # Timer
        self.time_rest_remaining = tk.StringVar(self.parent)
        self.time_rest_remaining.set(timer_rest.get_time_remaining())

        self.timer_canvas_rest = tk.Canvas(
            self.parent,
            width=self.timer_label_width,
            height=self.timer_label_height,
            bg="yellow",
            bd=0,
            relief="solid",
            highlightthickness=2,
            highlightbackground="yellow",
            highlightcolor="yellow",
        )
        # 휴식 timer 위치
        self.timer_canvas_rest.place(
            relx=0.5,
            rely=self.timer_canvas_rest_rely,
            anchor="center",
        )

        self.timer_label_rest = tk.Label(
            self.timer_canvas_rest,
            textvariable=self.time_rest_remaining,
            font=self.timer_label_font,
            bg="yellow",
        )
        self.timer_label_rest.place(
            x=(self.timer_label_width // 2),
            y=(self.timer_label_height // 2),
            anchor="center",
        )

    def init_weight_entry(self):
        """
        Initialize the weight entry widget.
        """
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
            relx=0.5, rely=0.678, anchor="center", relwidth=0.284, relheight=0.118
        )

        # Set initial text
        initial_weight_text = "부별체급"
        self.weight_entry.insert(0, initial_weight_text)
        # self.text_var.trace("w", lambda name, index, mode, sv=self.text_var: self.adjust_font_size())

    def load_images(self):
        # Warning circles
        self.yellow_circle_photo = None
        self.red_circle_photo = None
        self.resize_logo_image = None
        self.log_yellow_circle_photo = None

        # --- Load Yellow Circle ---
        try:
            image_path = self.resource_path("yellow_circle.png")
            img = Image.open(image_path)
            adjust_image_size = self.adjust_widget_size(80)
            img_resized = img.resize(
                (adjust_image_size, adjust_image_size),
                Image.Resampling.LANCZOS,  # Use Image.Resampling for newer Pillow versions
            )
            self.yellow_circle_photo = ImageTk.PhotoImage(
                img_resized, master=self.parent
            )

        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}", file=sys.stderr)
        except UnidentifiedImageError:
            print(
                f"Error: Cannot identify image file (corrupted or unsupported format) at {image_path}",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Error loading yellow circle image: {e}", file=sys.stderr)

        # --- Load Red Circle ---
        try:
            image_path = self.resource_path("red_circle.png")
            img = Image.open(image_path)
            # Assuming adjust_image_size is still valid from yellow circle loading
            adjust_image_size = self.adjust_widget_size(80)  # Recalculate if needed
            img_resized = img.resize(
                (adjust_image_size, adjust_image_size), Image.Resampling.LANCZOS
            )
            # self.red_circle_image = img_resized # Store if needed
            self.red_circle_photo = ImageTk.PhotoImage(img_resized, master=self.parent)

        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}", file=sys.stderr)
        except UnidentifiedImageError:
            print(
                f"Error: Cannot identify image file (corrupted or unsupported format) at {image_path}",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Error loading red circle image: {e}", file=sys.stderr)

        # --- Load Logo Image ---
        try:
            image_path = self.resource_path("logo.jpg")
            img = Image.open(image_path)
            logo_adjust_image_size = self.adjust_widget_size(480)
            img_resized = img.resize(
                (logo_adjust_image_size, logo_adjust_image_size),
                Image.Resampling.LANCZOS,
            )
            # self.logo_image = img_resized # Store if needed
            self.resize_logo_image = ImageTk.PhotoImage(img_resized, master=self.parent)

        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}", file=sys.stderr)
        except UnidentifiedImageError:
            print(
                f"Error: Cannot identify image file (corrupted or unsupported format) at {image_path}",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Error loading logo image: {e}", file=sys.stderr)

        # --- Load Log Yellow Circle Image (Smaller version) ---
        # This depends on the yellow_circle_image being successfully loaded and resized earlier
        # Let's reload it to be safe, or use the previously loaded one if available
        try:
            # Option 1: Reload the original yellow circle image
            image_path = self.resource_path("yellow_circle.png")
            img = Image.open(image_path)

            # Option 2: Reuse previously resized image if available (less robust if first load failed)
            # if self.yellow_circle_photo and hasattr(self.yellow_circle_photo, '_PhotoImage__photo'):
            #     # Accessing internal might be fragile, better to resize from original PIL if kept
            #     # Or just reload as in Option 1
            #     pass # Need a reliable way to get PIL image back or store it

            # Proceeding with Option 1 (Reloading)
            log_adjust_image_size = self.adjust_widget_size(15)
            img_log_resized = img.resize(
                (log_adjust_image_size, log_adjust_image_size), Image.Resampling.LANCZOS
            )
            # self.log_yellow_circle_image = img_log_resized # Store if needed
            self.log_yellow_circle_photo = ImageTk.PhotoImage(
                img_log_resized, master=self.parent
            )

        except FileNotFoundError:
            # This error might occur if the file exists for the first load but not the second (unlikely but possible)
            print(f"Error: Log image file not found at {image_path}", file=sys.stderr)
        except UnidentifiedImageError:
            print(
                f"Error: Cannot identify log image file (corrupted or unsupported format) at {image_path}",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Error loading log yellow circle image: {e}", file=sys.stderr)

    def load_utility_images(self):
        """Loads and prepares images for utility buttons."""
        self.pause_icon_photo = None
        self.camera_icon_photo = None
        self.reset_icon_photo = None
        self.log_rest_photo = None

        icon_files = {
            "pause": "pause_icon.png",  # Replace with your actual filenames
            "camera": "camera_icon.png",
            "reset": "reset_icon.png",
        }

        for key, filename in icon_files.items():
            try:
                image_path = self.resource_path(filename)
                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"Image file not found at {image_path}")

                img = Image.open(image_path).convert(
                    "RGBA"
                )  # Use RGBA for transparency
                img_resized = img.resize(
                    (self.util_icon_btn_size, self.util_icon_btn_size),
                    Image.Resampling.LANCZOS,
                )
                photo_image = ImageTk.PhotoImage(img_resized, master=self.parent)

                # Store the PhotoImage object in self
                if key == "pause":
                    self.pause_icon_photo = photo_image
                elif key == "camera":
                    self.camera_icon_photo = photo_image
                elif key == "reset":
                    self.reset_icon_photo = photo_image
                # print(f"Successfully loaded icon: {filename}")

            except FileNotFoundError as e:
                print(f"Error: {e}", file=sys.stderr)
            except UnidentifiedImageError:
                print(
                    f"Error: Cannot identify image file (corrupted or unsupported format): {filename}",
                    file=sys.stderr,
                )
            except Exception as e:
                print(f"Error loading icon '{filename}': {e}", file=sys.stderr)

        try:
            image_path = self.resource_path("pause_log_icon.png")
            img = Image.open(image_path).convert("RGBA")

            log_adjust_image_size = self.adjust_widget_size(15)
            img_log_resized = img.resize(
                (log_adjust_image_size, log_adjust_image_size), Image.Resampling.LANCZOS
            )
            self.log_rest_photo = ImageTk.PhotoImage(
                img_log_resized, master=self.parent
            )
        except FileNotFoundError:
            print(f"Error: Log image file not found at {image_path}", file=sys.stderr)
        except UnidentifiedImageError:
            print(
                f"Error: Cannot identify log image file (corrupted or unsupported format) at {image_path}",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Error loading log yellow circle image: {e}", file=sys.stderr)

    def red_increase(self):
        self.red_score += 1
        self.red_score_label.config(text="{}".format(self.red_score))

    def blue_increase(self):
        self.blue_score += 1
        self.blue_score_label.config(text="{}".format(self.blue_score))

    def red_decrease(self):
        self.red_score -= 1
        self.red_score_label.config(text="{}".format(self.red_score))

    def blue_decrease(self):
        self.blue_score -= 1
        self.blue_score_label.config(text="{}".format(self.blue_score))

    def update_timer(self):
        self.time_remaining.set(self.timer.get_time_remaining())
        self.timer_label.update_idletasks()  # Update only the timer label widget

    def update_timer_rest(self):
        self.time_rest_remaining.set(self.timer_rest.get_time_remaining())
        self.timer_label_rest.update_idletasks()  # Update only the timer_rest label widget

    def show_btn_start_timer(self, isStart):
        if isStart:
            self.btn_start_timer.config(text="멈춤")
            # Hide Button
            self.btn_timer_minus_10.pack_forget()
            self.btn_timer_minus_1.pack_forget()
            self.btn_timer_plus_10.pack_forget()
            self.btn_timer_plus_1.pack_forget()
            self.btn_timer_rest_frame.grid_remove()
            self.btn_capture_frame.grid_remove()
            self.btn_timer_reset_frame.grid_remove()
        else:
            self.btn_start_timer.config(text="시작")
            # Show Buttons
            self.show_timer_config_buttons()

    def show_btn_start_timer_rest(self, isStart):
        if isStart:
            self.btn_start_timer_rest.config(text="멈춤")
            # Hide Button
            self.btn_timer_minus_10.pack_forget()
            self.btn_timer_minus_1.pack_forget()
            self.btn_timer_plus_10.pack_forget()
            self.btn_timer_plus_1.pack_forget()
            self.btn_timer_rest_frame.grid_remove()
            self.btn_capture_frame.grid_remove()
            self.btn_timer_reset_frame.grid_remove()
        else:
            self.btn_start_timer_rest.config(text="휴식")
            # Show Buttons
            self.show_timer_config_buttons()

    def toggle_rest_mode(self):
        """
        Switches between main timer display and rest timer display/controls.
        """
        if self.is_rest:
            self.timer_canvas_rest.place(
                relx=0.5,
                rely=self.timer_canvas_rest_rely,
                anchor="center",
            )
            self.timer_label_rest.place(
                x=(self.timer_label_width // 2),
                y=(self.timer_label_height // 2),
                anchor="center",
            )
            self.btn_start_timer.pack_forget()
            self.btn_start_timer_rest.pack(fill=tk.BOTH, expand=True)

            # 눌림 상태
            if hasattr(self, "btn_timer_rest"):
                self.btn_timer_rest.config(
                    relief=tk.SUNKEN,
                    bg="gray20",
                )
        else:
            # hide widget
            self.timer_canvas_rest.place_forget()
            self.timer_label_rest.place_forget()
            self.btn_start_timer_rest.pack_forget()

            self.timer_rest.reset()
            self.update_timer_rest()

            # show widget
            self.btn_start_timer.pack(fill=tk.BOTH, expand=True)
            # 눌림 상태 해제
            if hasattr(self, "btn_timer_rest"):
                self.btn_timer_rest.config(
                    relief=tk.FLAT,
                    bg="gray35",
                )

    def show_timer_config_buttons(self):
        self.btn_timer_minus_10.pack(pady=1)
        self.btn_timer_minus_1.pack(pady=1)
        self.btn_timer_plus_10.pack(pady=1)
        self.btn_timer_plus_1.pack(pady=1)
        self.btn_timer_rest_frame.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        self.btn_capture_frame.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
        self.btn_timer_reset_frame.grid(row=1, column=2, sticky="nsew", padx=1, pady=1)

    def play_sound(self):
        # Play an MP3 file when the timer ends
        pygame.mixer.music.play()

    def reset_timer(self):
        self.timer.reset()
        self.timer_rest.reset()
        self.update_timer()
        self.update_timer_rest()

        # Reset scores
        self.round = 1
        self.red_score = 0
        self.blue_score = 0
        self.red_score_label.config(text="{}".format(self.red_score))
        self.blue_score_label.config(text="{}".format(self.blue_score))
        self.red_warning_state = -1
        self.blue_warning_state = -1

        self.timer.is_start = True  # 경고 상태 초기화
        self.red_warning()
        self.blue_warning()

        # Reset Timer Button
        self.timer.timer_running = False
        self.timer.is_start = False
        self.timer_rest.timer_running = False
        self.timer_rest.is_start = False
        self.btn_start_timer.config(text="시작")
        self.btn_start_timer_rest.config(text="휴식")

        # Show Buttons
        self.show_timer_config_buttons()

    def save_warning_widgets(self):
        self.red_yellow_circle_place_info = self.red_yellow_circle.place_info()
        self.red_red_circle_place_info = self.red_red_circle.place_info()
        self.red_yellow_circle1_place_info = self.red_yellow_circle1.place_info()
        self.red_red_circle1_place_info = self.red_red_circle1.place_info()
        self.red_yellow_circle2_place_info = self.red_yellow_circle2.place_info()
        self.red_red_circle2_place_info = self.red_red_circle2.place_info()

        self.blue_yellow_circle_place_info = self.blue_yellow_circle.place_info()
        self.blue_red_circle_place_info = self.blue_red_circle.place_info()
        self.blue_yellow_circle1_place_info = self.blue_yellow_circle1.place_info()
        self.blue_red_circle1_place_info = self.blue_red_circle1.place_info()
        self.blue_yellow_circle2_place_info = self.blue_yellow_circle2.place_info()
        self.blue_red_circle2_place_info = self.blue_red_circle2.place_info()

    def red_warning(self):
        # if self.timer.is_start:
        self.red_warning_state += 1

        if self.red_warning_state == 1:
            self.red_red_circle.place_forget()
            self.red_yellow_circle1.place_forget()
            self.red_red_circle1.place_forget()
            self.red_yellow_circle2.place_forget()
            self.red_red_circle2.place_forget()

            self.red_yellow_circle.place(**self.red_yellow_circle_place_info)
        elif self.red_warning_state == 2:
            self.red_yellow_circle.place_forget()
            self.red_yellow_circle1.place_forget()
            self.red_red_circle1.place_forget()
            self.red_yellow_circle2.place_forget()
            self.red_red_circle2.place_forget()

            self.red_red_circle.place(**self.red_red_circle_place_info)
        elif self.red_warning_state == 3:
            self.red_yellow_circle.place_forget()
            self.red_red_circle1.place_forget()
            self.red_yellow_circle2.place_forget()
            self.red_red_circle2.place_forget()

            self.red_red_circle.place(**self.red_red_circle_place_info)
            self.red_yellow_circle1.place(**self.red_yellow_circle1_place_info)

        elif self.red_warning_state == 4:
            self.red_yellow_circle.place_forget()
            self.red_yellow_circle1.place_forget()
            self.red_yellow_circle2.place_forget()
            self.red_red_circle2.place_forget()

            self.red_red_circle.place(**self.red_red_circle_place_info)
            self.red_red_circle1.place(**self.red_red_circle1_place_info)

        elif self.red_warning_state == 5:
            self.red_yellow_circle.place_forget()
            self.red_yellow_circle1.place_forget()
            self.red_red_circle2.place_forget()

            self.red_red_circle.place(**self.red_red_circle_place_info)
            self.red_red_circle1.place(**self.red_red_circle1_place_info)
            self.red_yellow_circle2.place(**self.red_yellow_circle2_place_info)
        else:
            self.red_warning_state = 0
            self.red_yellow_circle.place_forget()
            self.red_red_circle.place_forget()
            self.red_yellow_circle1.place_forget()
            self.red_red_circle1.place_forget()
            self.red_yellow_circle2.place_forget()
            self.red_red_circle2.place_forget()

    def blue_warning(self):
        # if self.timer.is_start:
        self.blue_warning_state += 1

        if self.blue_warning_state == 1:
            self.blue_red_circle.place_forget()
            self.blue_yellow_circle1.place_forget()
            self.blue_red_circle1.place_forget()
            self.blue_yellow_circle2.place_forget()
            self.blue_red_circle2.place_forget()

            self.blue_yellow_circle.place(**self.blue_yellow_circle_place_info)
        elif self.blue_warning_state == 2:
            self.blue_yellow_circle.place_forget()
            self.blue_yellow_circle1.place_forget()
            self.blue_red_circle1.place_forget()
            self.blue_yellow_circle2.place_forget()
            self.blue_red_circle2.place_forget()

            self.blue_red_circle.place(**self.blue_red_circle_place_info)
        elif self.blue_warning_state == 3:
            self.blue_yellow_circle.place_forget()
            self.blue_red_circle1.place_forget()
            self.blue_yellow_circle2.place_forget()
            self.blue_red_circle2.place_forget()

            self.blue_red_circle.place(**self.blue_red_circle_place_info)
            self.blue_yellow_circle1.place(**self.blue_yellow_circle1_place_info)

        elif self.blue_warning_state == 4:
            self.blue_yellow_circle.place_forget()
            self.blue_yellow_circle1.place_forget()
            self.blue_yellow_circle2.place_forget()
            self.blue_red_circle2.place_forget()

            self.blue_red_circle.place(**self.blue_red_circle_place_info)
            self.blue_red_circle1.place(**self.blue_red_circle1_place_info)

        elif self.blue_warning_state == 5:
            self.blue_yellow_circle.place_forget()
            self.blue_yellow_circle1.place_forget()
            self.blue_red_circle2.place_forget()

            self.blue_red_circle.place(**self.blue_red_circle_place_info)
            self.blue_red_circle1.place(**self.blue_red_circle1_place_info)
            self.blue_yellow_circle2.place(**self.blue_yellow_circle2_place_info)
        else:
            self.blue_warning_state = 0
            self.blue_yellow_circle.place_forget()
            self.blue_red_circle.place_forget()
            self.blue_yellow_circle1.place_forget()
            self.blue_red_circle1.place_forget()
            self.blue_yellow_circle2.place_forget()
            self.blue_red_circle2.place_forget()

    def resource_path(self, relative_path):
        """
        Get the absolute path to a resource file.

        Args:
            relative_path (str): Relative path to the resource.

        Returns:
            str: Absolute path to the resource.
        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def adjust_widget_size(self, base_size, base_resolution=(1920, 1080)):
        """
        Adjust widget size based on screen resolution.

        Args:
            base_size (int): Base size of the widget.
            base_resolution (tuple): Base resolution for scaling.

        Returns:
            int: Adjusted size.
        """
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
            self.red_score_label.config(fg="white")
            self.blue_score_label.config(fg="white")
            self.parent.update_idletasks()
            return

        if is_blue_win:
            self.blue_score_label.config(
                fg="yellow" if self.blue_score_label.cget("fg") == "white" else "white"
            )
        else:
            self.red_score_label.config(
                fg="yellow" if self.red_score_label.cget("fg") == "white" else "white"
            )

        self.parent.update_idletasks()
        self.parent.after(500, self.blink_winner, count - 1, is_blue_win)

    def blink_timer_rest(self):
        if self.timer_rest.timer_running:
            # self.timer_canvas_rest.config(
            #     bg=(
            #         "yellow"
            #         if self.timer_canvas_rest.cget("bg") == "white"
            #         else "white"
            #     )
            # )
            self.timer_label_rest.config(
                bg=(
                    "yellow" if self.timer_label_rest.cget("bg") == "white" else "white"
                )
            )
        else:
            # self.timer_canvas_rest.config(bg="yellow")
            self.timer_label_rest.config(bg="yellow")

        # self.parent.update_idletasks()
        self.parent.update_idletasks()
        # self.timer_label_rest.update_idletasks()
        self.parent.after(1000, self.blink_timer_rest)


class ControlPanel(tk.Toplevel):
    """
    Control panel class for managing user interactions and scoreboard updates.
    """

    def __init__(self, master, scoreboard, monitor, timer, timer_rest):
        """
        Initialize the control panel with UI components and event bindings.

        Args:
            master (tk.Tk): Root window.
            scoreboard (ViewPanel): The scoreboard view panel.
            monitor (screeninfo.Monitor): Monitor information for positioning.
            timer (Timer): Timer object for managing countdowns.
        """
        super().__init__(master)
        self.scoreboard = scoreboard
        self.monitor = monitor
        self.timer = timer
        self.timer_rest = timer_rest

        self.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        self.overrideredirect(False)

        self.screen_width = self.monitor.width
        self.screen_height = self.monitor.height

        self.widgets = ScoreBoard(
            self, self.screen_width, self.screen_height, self.timer, self.timer_rest
        )

        self.title("컨트롤 패널")

        self.widgets.btn_red_plus.config(command=self.update_red_score)
        self.widgets.btn_red_minus.config(command=self.update_red_decrease)
        self.widgets.red_warning_button.config(command=self.update_red_warning)
        self.widgets.btn_blue_plus.config(command=self.update_blue_score)
        self.widgets.btn_blue_minus.config(command=self.update_blue_decrease)
        self.widgets.blue_warning_button.config(command=self.update_blue_warning)
        self.widgets.btn_timer_plus_1.config(
            command=lambda: self.update_increase_timer(100)
        )
        self.widgets.btn_timer_minus_1.config(
            command=lambda: self.update_decrease_timer(100)
        )
        self.widgets.btn_timer_plus_10.config(
            command=lambda: self.update_increase_timer(1000)
        )
        self.widgets.btn_timer_minus_10.config(
            command=lambda: self.update_decrease_timer(1000)
        )
        self.widgets.btn_start_timer.config(command=self.update_start_timer)
        self.widgets.btn_start_timer_rest.config(command=self.update_start_timer_rest)
        self.widgets.btn_timer_rest.config(command=self.update_toggle_rest_mode)
        self.widgets.btn_capture.config(command=self.save_screenshot)
        self.widgets.btn_timer_reset.config(command=self.update_reset_timer)
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
        """
        점수 로그 화면 표시
          - 시간-행위 쌍으로 표시(01:22 +1)
        """
        style = ttk.Style(root)
        style.theme_use("clam")

        def fixed_map(option):
            # Fix for setting text colour for Tkinter 8.6.9
            # From: https://core.tcl.tk/tk/info/509cafafae
            #
            # Returns the style map for 'option' with any styles starting with
            # ('!disabled', '!selected', ...) filtered out.

            # style.map() returns an empty list for missing options, so this
            # should be future-safe.
            return [
                elm
                for elm in style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")
            ]

        style.map(
            "Treeview",
            foreground=fixed_map("foreground"),
            background=fixed_map("background"),
            fieldbackground=fixed_map("fieldbackground"),
        )

        log_font = (
            self.widgets.str_number_font,
            self.widgets.adjust_widget_size(15),
        )
        log_rowheight = self.widgets.adjust_widget_size(30)
        style.configure(
            "Red.Treeview",
            background="#F5E6D3",
            foreground="black",
            fieldbackground="red",
            font=log_font,
            rowheight=log_rowheight,
        )
        style.configure(
            "Blue.Treeview",
            background="#F5E6D3",
            foreground="black",
            fieldbackground="blue",
            font=log_font,
            rowheight=log_rowheight,
        )

        # red
        self.red_log_panel = tk.Frame(self.widgets.red_panel, bg="black")
        self.red_log_panel.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.88)

        self.red_log_view = ttk.Treeview(
            self.red_log_panel, columns=("time",), show="tree", style="Red.Treeview"
        )

        self.red_log_view.column("#0", width=35, anchor=tk.CENTER)
        self.red_log_view.column("time", width=75, anchor=tk.CENTER)

        # Red Treeview 태그 설정
        self.red_log_view.tag_configure("odd_row", background="#FFD1D1")
        self.red_log_view.tag_configure("even_row", background="#FFE8E8")
        self.red_log_view.tag_configure(
            "round_row", background="#8B0000", foreground="white"
        )

        self.red_log_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # blue
        self.blue_log_panel = tk.Frame(self.widgets.blue_panel)
        self.blue_log_panel.place(relx=0, rely=0, relwidth=0.15, relheight=0.88)

        self.blue_log_view = ttk.Treeview(
            self.blue_log_panel, columns=("time",), show="tree", style="Blue.Treeview"
        )

        self.blue_log_view.column("#0", width=35, anchor=tk.CENTER)
        self.blue_log_view.column("time", width=75, anchor=tk.CENTER)

        # Blue Treeview 태그 설정
        self.blue_log_view.tag_configure("odd_row", background="#D1D1FF")
        self.blue_log_view.tag_configure("even_row", background="#E8E8FF")
        self.blue_log_view.tag_configure(
            "round_row", background="#00008B", foreground="white"
        )

        self.blue_log_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def add_log_item(self, treeview, time, image=None, text=None):
        """
        Add a log item to the specified Treeview widget.

        Args:
            treeview (ttk.Treeview): The Treeview widget to update.
            time (str): The time of the event.
            image (ImageTk.PhotoImage, optional): Image to display in the log.
            text (str, optional): Text to display in the log.
        """
        item_count = len(treeview.get_children())
        tag = "odd_row" if item_count % 2 == 0 else "even_row"

        if image:
            treeview.insert("", tk.END, values=(time,), image=image, tags=(tag,))
        elif text is not None:
            treeview.insert("", tk.END, values=(time,), text=text, tags=(tag,))

    def _add_empty_item(self, treeview):
        item_count = len(treeview.get_children())
        tag = "odd_row" if item_count % 2 == 0 else "even_row"
        treeview.insert("", tk.END, values=("",), tags=(tag,))

    def balance_log_views(self):
        """
        Ensure the log views for both teams have the same number of rows.
        """
        red_count = len(self.red_log_view.get_children())
        blue_count = len(self.blue_log_view.get_children())

        target_count = max(red_count, blue_count)

        while len(self.red_log_view.get_children()) < target_count:
            self._add_empty_item(self.red_log_view)

        while len(self.blue_log_view.get_children()) < target_count:
            self._add_empty_item(self.blue_log_view)

    def add_round_row(self):
        """
        Add a new round row to the log views.
        """
        self.balance_log_views()

        self.red_log_view.insert(
            "", tk.END, values=("Round",), text=self.widgets.round, tags=("round_row",)
        )
        self.blue_log_view.insert(
            "", tk.END, values=("Round",), text=self.widgets.round, tags=("round_row",)
        )

    def init_menu(self):
        """
        Initialize the top menu bar with help options.
        """
        menubar = tk.Menu(self)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="프로그램 정보", command=self.help_dialog)

        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)
        self.menubar = menubar

        self.help_dialog = None

    def help_dialog(self):
        """
        Display a help dialog with program information and shortcuts.
        """

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
        """
        Center the specified window on the screen.

        Args:
            window (tk.Toplevel): The window to center.
        """
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
        """
        Handle the close event for the control panel.
        """
        # Close both the control panel and the view panel
        self.destroy()
        self.scoreboard.destroy()

        # Terminate the mainloop
        self.master.quit()

    def update_red_score(self):
        """
        Update the red team's score and log the event.
        """
        self.scoreboard.widgets.red_increase()
        self.widgets.red_increase()
        self.add_log_item(self.red_log_view, self.timer.get_time_remaining(), text="+1")

    def update_red_decrease(self):
        self.scoreboard.widgets.red_decrease()
        self.widgets.red_decrease()
        self.add_log_item(self.red_log_view, self.timer.get_time_remaining(), text="-1")

    def update_red_warning(self):
        self.widgets.red_warning()
        self.scoreboard.widgets.red_warning()
        self.add_log_item(
            self.red_log_view,
            self.timer.get_time_remaining(),
            image=self.widgets.log_yellow_circle_photo,
        )

    def update_blue_score(self):
        """
        Update the blue team's score and log the event.
        """
        self.scoreboard.widgets.blue_increase()
        self.widgets.blue_increase()
        self.add_log_item(
            self.blue_log_view, self.timer.get_time_remaining(), text="+1"
        )

    def update_blue_decrease(self):
        self.scoreboard.widgets.blue_decrease()
        self.widgets.blue_decrease()
        self.add_log_item(
            self.blue_log_view, self.timer.get_time_remaining(), text="-1"
        )

    def update_blue_warning(self):
        self.scoreboard.widgets.blue_warning()
        self.widgets.blue_warning()
        self.add_log_item(
            self.blue_log_view,
            self.timer.get_time_remaining(),
            image=self.widgets.log_yellow_circle_photo,
        )

    def update_decrease_timer(self, value):
        self.timer.decrease_timer(value)
        self.scoreboard.widgets.update_timer()
        self.widgets.update_timer()

    def update_increase_timer(self, value):
        self.timer.increase_timer(value)
        self.scoreboard.widgets.update_timer()
        self.widgets.update_timer()

    def update_decrease_timer_rest(self, value):
        self.timer_rest.decrease_timer(value)
        self.scoreboard.widgets.update_timer_rest()
        self.widgets.update_timer_rest()

    def update_increase_timer_rest(self, value):
        self.timer_rest.increase_timer(value)
        self.scoreboard.widgets.update_timer_rest()
        self.widgets.update_timer_rest()

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
            elif key_code == 50:  # 2
                self.update_blue_decrease()
            elif key_code == 189:  # -
                self.update_red_score()
            elif key_code == 187:  # =
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
        self.start_timer()

    def update_start_timer_rest(self):
        self.start_timer_rest()

    def update_toggle_rest_mode(self):
        self.widgets.is_rest = not self.widgets.is_rest

        # change command btn_timer_minus_*, btn_timer_plus_*
        if self.widgets.is_rest:
            self.widgets.btn_timer_plus_1.config(
                command=lambda: self.update_increase_timer_rest(100)
            )
            self.widgets.btn_timer_minus_1.config(
                command=lambda: self.update_decrease_timer_rest(100)
            )
            self.widgets.btn_timer_plus_10.config(
                command=lambda: self.update_increase_timer_rest(1000)
            )
            self.widgets.btn_timer_minus_10.config(
                command=lambda: self.update_decrease_timer_rest(1000)
            )
        else:
            self.widgets.btn_timer_plus_1.config(
                command=lambda: self.update_increase_timer(100)
            )
            self.widgets.btn_timer_minus_1.config(
                command=lambda: self.update_decrease_timer(100)
            )
            self.widgets.btn_timer_plus_10.config(
                command=lambda: self.update_increase_timer(1000)
            )
            self.widgets.btn_timer_minus_10.config(
                command=lambda: self.update_decrease_timer(1000)
            )

        self.widgets.toggle_rest_mode()
        self.scoreboard.widgets.is_rest = self.widgets.is_rest
        self.scoreboard.widgets.toggle_rest_mode()

    def update_reset_timer(self):
        """
        reset_timer 재정의
        """
        self.widgets.reset_timer()
        self.scoreboard.widgets.reset_timer()
        # delete logs
        self.red_log_view.delete(*self.red_log_view.get_children())
        self.blue_log_view.delete(*self.blue_log_view.get_children())
        # 1R add
        self.add_round_row()

    def swap_positions(self):
        """
        듀얼 화면 표시를 위해 red, blue 패널 위치를 바꾼다.
        """
        # print("Setting initial swapped positions: Blue Left, Red Right")
        if hasattr(self.widgets, "blue_panel") and hasattr(self.widgets, "red_panel"):
            # Re-place Blue panel to the left
            self.widgets.blue_panel.place_configure(relx=0)
            # Re-place Red panel to the right
            self.widgets.red_panel.place_configure(relx=0.5)
        else:
            print("Error: Panels not initialized before calling swap_position.")

        self.widgets.save_warning_widgets()
        # 위치 초기화
        self.widgets.red_warning_state = -1
        self.widgets.blue_warning_state = -1
        self.scoreboard.widgets.red_warning_state = -1
        self.scoreboard.widgets.blue_warning_state = -1
        self.widgets.red_warning()
        self.scoreboard.widgets.red_warning()
        self.widgets.blue_warning()
        self.scoreboard.widgets.blue_warning()

    def start_timer(self):
        """
        Start or stop the timer and update the UI accordingly.
        """
        if self.timer.start_timer_seconds > 0:
            if not self.timer.timer_running:
                self.timer.start(True)
                self.timer.is_start = True
                self.widgets.show_btn_start_timer(True)  # Show '멈춤' and Hide widgets
                self.countdown()
            else:
                self.timer.start(False)
                self.widgets.show_btn_start_timer(False)  # Show '시작' and Show widgets
        else:
            # 2라운드 시작 버튼 눌렀을 때
            self.timer.timer_running = False
            self.timer.is_start = False
            self.timer.start_timer_seconds = 3000
            self.timer.timer_seconds = 3000
            self.widgets.update_timer()
            self.scoreboard.widgets.update_timer()
            self.widgets.show_btn_start_timer(False)  # Show '시작' and Show widgets

    def start_timer_rest(self):
        """
        Start or stop the rest timer and update the UI accordingly.
        """
        if self.timer_rest.start_timer_seconds > 0:
            if not self.timer_rest.timer_running:
                self.timer_rest.start(True)
                self.timer_rest.is_start = True
                self.widgets.show_btn_start_timer_rest(
                    True
                )  # Show '멈춤' and Hide widgets

                # Add rest log
                self.balance_log_views()
                self.add_log_item(
                    self.blue_log_view,
                    self.timer_rest.get_time_remaining(),
                    image=self.widgets.log_rest_photo,
                )
                self.add_log_item(
                    self.red_log_view,
                    self.timer_rest.get_time_remaining(),
                    image=self.widgets.log_rest_photo,
                )

                self.countdown_rest()
                self.widgets.blink_timer_rest()
                self.scoreboard.widgets.blink_timer_rest()
            else:
                self.timer_rest.start(False)
                self.widgets.show_btn_start_timer_rest(
                    False
                )  # Show '휴식' and Show widgets

    def countdown(self):
        if self.timer.timer_running:
            self.timer.update_timer_seconds()

            if self.timer.timer_seconds > 0:
                self.widgets.update_timer()
                self.scoreboard.widgets.update_timer()
                self.after(10, self.countdown)
            elif self.timer.timer_seconds <= 0:  # 시간 종료. 경기 끝
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
                self.widgets.btn_start_timer.config(
                    text="{} Round".format(self.widgets.round)
                )

                # Add round log
                self.add_round_row()

                # Blink the winner's score
                # self.blink_winner(6)  # Blink 3 times (6 because it's a half cycle of blinking)

    def countdown_rest(self):
        if self.timer_rest.timer_running:
            self.timer_rest.update_timer_seconds()

            if self.timer_rest.timer_seconds > 0:
                self.widgets.update_timer_rest()
                self.scoreboard.widgets.update_timer_rest()
                self.after(10, self.countdown_rest)
            elif self.timer_rest.timer_seconds <= 0:  # 시간 종료. 휴식 끝
                # Reset Rest Timer Button
                self.timer_rest.reset()
                self.widgets.show_btn_start_timer_rest(False)

                self.widgets.update_timer_rest()
                self.scoreboard.widgets.update_timer_rest()

                # Play an MP3 file when the timer ends
                self.widgets.play_sound()
                self.scoreboard.widgets.play_sound()

                # 휴식모드 종료
                self.update_toggle_rest_mode()

    def save_screenshot(self):
        """
        Save a screenshot of the current scoreboard view.
        """
        """현재 폴더에 스크린샷을 저장한다.
        1. 파일 이름 : title_entry.get() + '_' + weight_entry.get() + '_' + round_entry.get() +
                       '_' + red_name_entry.get() + '_' + red_score_label.get() + '_' + blue_name_entry.get() + '_' + blue_score_label.get() + '.png'
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
        # Create the file name
        file_name_view = (
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
            + "점_view.png"
        )

        def save_screenshot_bitmap(file_name, hwnd):

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

        # Save the screenshot of the control panel
        save_screenshot_bitmap(file_name, self.winfo_id())

        # Save the screenshot of the scoreboard view
        # save_screenshot_bitmap(file_name_view, self.scoreboard.winfo_id())


class ViewPanel(tk.Toplevel):
    """
    View panel class for displaying the scoreboard to the audience.
    """

    def __init__(self, master, monitor, timer, timer_rest):
        """
        Initialize the view panel with UI components.

        Args:
            master (tk.Tk): Root window.
            monitor (screeninfo.Monitor): Monitor information for positioning.
            timer (Timer): Timer object for managing countdowns.
        """
        super().__init__(master)

        self.title("스코어보드")
        self.monitor = monitor
        self.timer = timer
        self.timer_rest = timer_rest
        self.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        self.overrideredirect(False)

        self.screen_width = self.monitor.width
        self.screen_height = self.monitor.height
        self.widgets = ScoreBoard(
            self, self.screen_width, self.screen_height, timer, timer_rest
        )

        # view panel에서 숨김
        self.widgets.control_frame.place_forget()
        self.widgets.weight_entry.place_forget()

        # timer 위젯 위치 조정
        self.widgets.timer_canvas_rely = 0.73
        self.widgets.timer_canvas_rest_rely = 0.53
        self.widgets.timer_canvas.place(
            relx=0.5, rely=self.widgets.timer_canvas_rely, anchor="center"
        )
        # self.widgets.timer_canvas_rest.place(
        #     relx=0.5,
        #     rely=0.63,
        #     anchor="center",
        # )
        self.widgets.toggle_rest_mode()

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
        self.widgets.red_score_label.config(pady=60, padx=20)
        self.widgets.blue_score_label.config(pady=60, padx=20)

        self.widgets.save_warning_widgets()

    def init_geometry(self):
        self.geometry(
            f"{self.screen_width}x{self.screen_height}+{self.monitor.x}+{self.monitor.y}"
        )

    def start_timer(self):
        """
        Start the timer countdown in the view panel.
        """
        if self.timer.start_timer_seconds > 0:
            self.focus()

            if not self.timer.timer_running:
                self.widgets.countdown()
        else:
            self.widgets.update_timer()

    def reset_timer(self):
        """
        Reset the timer and scores in the view panel.
        """
        self.widgets.update_timer()

        # Reset scores
        self.widgets.round = 1
        self.widgets.red_score = 0
        self.widgets.blue_score = 0
        self.widgets.red_score_label.config(text="{}".format(self.widgets.red_score))
        self.widgets.blue_score_label.config(text="{}".format(self.widgets.blue_score))
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
    s = ttk.Style()
    root.withdraw()

    monitor = []
    for m in screeninfo.get_monitors():
        monitor.append(m)

    if len(monitor) == 1:
        monitor.append(monitor[0])

    timer = Timer()
    timer_rest = Timer()
    timer_rest.init_time = 6000  # 60초
    timer_rest.reset()

    score_board = ViewPanel(root, monitor[1], timer, timer_rest)
    control_panel = ControlPanel(root, score_board, monitor[0], timer, timer_rest)
    control_panel.swap_positions()

    root.mainloop()

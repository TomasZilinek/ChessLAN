import chess_lan_figure
from tkinter import *
from PIL import ImageTk, Image, ImageDraw


class Player:
    def __init__(self, color, name, mid_frame, profile_position, margin, board_width, label_color, root):
        self.pause = 0
        self.board = 0
        self.moving = 0
        self.timer_dimensions = []
        self.root = root
        self.timer_label = 0
        self.space = 0
        self.fig_num_drawn = 0
        self.death_label_image = 0
        self.death_figures_label = 0
        self.king_number = 0
        self.thrown_figures = []
        self.thrown_value = 0
        self.opposite_player = 0
        self.value_label = Label
        self.label_color = label_color
        self.board_width = board_width
        self.field_width = self.board_width / 11
        self.margin = margin
        self.mid_frame = mid_frame
        self.profile_frame = 0
        self.color = color
        self.figures = []
        self.name = name
        self.make_figures()
        self.name_label = 0
        self.profile_position = profile_position
        self.draw_profile(profile_position)
        self.time = 0

    def make_figures(self):
            for n in range(16):
                self.figures.append(chess_lan_figure.Figure(self.color, n))
                if self.figures[n].name[5:] == "King":
                    self.king_number = n

    def draw_profile(self, profile_position):
        if self.profile_frame != 0:
            self.profile_frame.place_forget()
        if profile_position == "up":
            y = 0
        else:
            y = self.board_width + self.margin
        self.profile_frame = Frame(self.mid_frame, width=self.board_width, height=self.margin, bg=self.label_color)
        self.profile_frame.place(x=0, y=y)
        self.name_label = Label(self.profile_frame, text=self.name, font="Arial 20 bold", bg=self.label_color, fg="white")
        self.name_label.place(x=10, y=15)
        self.value_label = Label(self.profile_frame, text="", font="Arial 17 bold", bg=self.label_color, fg="white")
        self.value_label.place(x=self.board_width / 4.3, y=3)
        for count, f in enumerate(self.thrown_figures):
            width = self.board_width / 16
            img = Image.new("RGBA", [int(width), int(width)])
            to_paste = Image.open(f[0] + ".png").convert("RGBA")
            to_paste = to_paste.resize([int(width), int(width)])
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, width, width], self.label_color)
            img.paste(to_paste, (0, 0), to_paste)
            reference_image = ImageTk.PhotoImage(img)
            l = Label(self.profile_frame, image=reference_image, bd=0)
            l.image = reference_image
            l.place(x=self.board_width / 3.45 + count * width / 1.2, y=0)
        try:
            self.update_thrown_value_label()
        except:
            pass

    def add_to_death_list(self, f_name):
        label_width = int(self.board_width - self.board_width / 3.45)
        label_img = Image.new("RGBA", [int(label_width), int(self.field_width)])
        draw = ImageDraw.Draw(label_img)
        draw.rectangle([0, 0, label_width, self.field_width], self.label_color)
        reference_image = ImageTk.PhotoImage(label_img)
        if self.death_figures_label == 0:
            self.death_figures_label = Label(self.profile_frame, width=label_width, height=self.field_width, image=reference_image, bd=0, bg=self.label_color)
        self.death_figures_label.image = reference_image
        self.death_figures_label.place(x=self.board_width / 3.45, y=0)
        self.death_label_image = label_img
        self.fig_num_drawn = 0
        self.thrown_figures.append([f_name, 0])  # [figure name, whether drawn]
        self.space = 0
        for f in self.thrown_figures:
            f[1] = 0
        self.draw_to_death_picture("Pawn")

    def draw_to_death_picture(self, fig_name):
        sequence = {"Pawn": "Bishop", "Bishop": "Knight", "Knight": "Rook", "Rook": "Queen"}
        for fig in self.thrown_figures:
            if fig[0][5:] == fig_name and fig[1] == 0:
                if fig_name == "Pawn":
                    shift = 0.4
                else:
                    shift = 0.46
                fig_img = Image.open(fig[0] + ".png").convert("RGBA").resize([int(self.field_width), int(self.field_width)])
                label_img = self.death_label_image
                label_img.paste(fig_img, (int(shift * self.fig_num_drawn * self.field_width + self.space), 0), fig_img)
                self.death_label_image = label_img
                reference_image = ImageTk.PhotoImage(label_img)
                self.death_figures_label.config(image=reference_image)
                self.death_figures_label.image = reference_image
                self.fig_num_drawn += 1
                fig[1] = 1
        if fig_name == "Pawn":
            shift2 = -0.13
        else:
            shift2 = 0.22
        self.space += shift2 * self.field_width
        if self.fig_num_drawn != len(self.thrown_figures):
            self.draw_to_death_picture(sequence[fig_name])

    def update_thrown_value_label(self):
        if self.thrown_value == self.opposite_player.thrown_value:
            self.value_label.config(text="")
        else:
            if self.thrown_value > self.opposite_player.thrown_value:
                self.value_label.config(text="")
            else:
                self.value_label.config(text="+" + str(self.opposite_player.thrown_value - self.thrown_value))

    def get_info(self, pl, board):  # opposite player, board object
        self.opposite_player = pl
        self.board = board

    def update_timer(self, minutes="None", resume=0, timer_dimensions=0, pause="None"):
        if pause != "None":
            self.pause = pause
        if timer_dimensions != 0:
            self.timer_dimensions = timer_dimensions
        if minutes != "None":
            self.time = int(float(minutes) * 60)
        if resume == 1 and self.moving == 1 and self.pause == 0:
            if minutes == "None":
                self.time -= 0.05
        timer_mins = int((self.time - self.time % 60) / 60)
        timer_secs = int(self.time - timer_mins * 60)
        timer_hundredths = int((self.time - timer_mins * 60 - timer_secs) * 10)
        if self.time < 19:
            timer_hundredths = "." + str(timer_hundredths)
            if self.timer_label[1] == 0:
                self.timer_label[0].place_forget()
                self.timer_label[0].place(x=5, y=0.25 * self.timer_dimensions[1])
        else:
            timer_hundredths = ""
        if timer_mins == 0:
            timer_mins = " 0"
        elif timer_mins < 10:
            timer_mins = " " + str(timer_mins)
        if timer_secs == 0:
            timer_secs = "00"
        elif timer_secs < 10:
            timer_secs = "0" + str(timer_secs)
        timer_text = str(timer_mins) + ":" + str(timer_secs) + timer_hundredths
        self.timer_label[0].config(text=timer_text)
        if self.time <= 0:
            self.board.show_results(self.opposite_player, "on time")
            self.timer_label[0].config(text=" 0:00.0")
        else:
            if resume == 1 and self.moving == 1 and self.pause == 0:
                self.root.after(50, lambda: self.update_timer(resume=1))

from tkinter import *
from PIL import ImageTk, Image, ImageDraw
from pygame import mixer
from chess_lan_functions import detect_check, detect_check_mate, check_movement_correctness, get_position, detect_draw
import copy


class Board:
    def __init__(self, Environment, master, master_of_master, width, player_view, board_border_color, players,
                 game_time, root):
        self.Environment = Environment
        self.root = root
        self.game_time = game_time
        self.log_line_height = 25
        self.scale_length = 0
        self.log_number = [0, 0]  # [0] -> row, [1] -> column
        self.log = []  # log = [master frame, scale object, master frame bg color]
        self.log_entries = []
        self.players = players
        self.change_let_to_upp = {"white": "White", "black": "Black"}
        self.change_right = {"white": self.players[0], "black": self.players[1]}
        self.change_opp = {"white": self.players[1], "black": self.players[0]}
        self.denotation_labels = []
        self.click_color = "#e0e038"
        self.moving = "white"
        self.black_color_mode = "#99734d"
        self.white_color_mode = "#f5f5dc"
        self.board_border_color = board_border_color
        self.player_view = player_view
        self.num_to_lett = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", "X": "X"}
        self.lett_to_num = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "X": "X"}
        self.width = width
        self.master = master
        self.master_of_master = master_of_master
        self.view_side = ""
        self.position = []
        self.black_field_image = 0
        self.white_field_image = 0
        self.field_width = 0
        self.field_border = 0
        self.fields = []
        self.create_fields()
        self.draw_fields()
        self.draw_figures("players")
        self.marked = [0, 0, 0]
        self.choose_fig_frame = 0
        self.choosing_opened = [0, [0, 0, 0]]  # [open/closed choosing window, [parameters for case of switching screen while choosing]]
        self.all_moves = []
        self.moves_list_index = 0
        self.observing = 0
        mixer.init()
        mixer.music.load('game_opening.mp3')
        mixer.music.play()

    def create_fields(self):
        self.field_border = self.width * 0.05
        self.field_width = (self.width - self.field_border * 2) / 8
        img = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, self.field_width, self.field_width], self.black_color_mode)
        self.black_field_image = ImageTk.PhotoImage(img)
        draw.rectangle([0, 0, self.field_width, self.field_width], self.white_color_mode)
        self.white_field_image = ImageTk.PhotoImage(img)
        line = 0
        color = "black"
        for count in range(1, 65):
            if color == "black":
                label = Label(self.master, image=self.black_field_image, bd=0)
                label.image = self.black_field_image
                self.fields.append([label, count, color])
            else:
                label = Label(self.master, image=self.white_field_image, bd=0)
                label.image = self.white_field_image
                self.fields.append([label, count, color])
            if count % 8 == 0 and count != 0:
                line += 1
            if count % 8 != 0:
                if color == "black":
                    color = "white"
                else:
                    color = "black"
        for n in range(1, 9):
            number_label = Label(self.master, text=str(n), font="Arial 15 bold", bg=self.board_border_color, fg="white",
                                 bd=0)
            letter_label = Label(self.master, text=self.num_to_lett[abs(n - 9)], font="Arial 15 bold",
                                 bg=self.board_border_color, fg="white", bd=0)
            if self.player_view == "white":
                number_label.place(x=self.field_border / 3.2, y=abs(n - 9) * self.field_width - self.field_width * 0.2)
                letter_label.place(x=abs(n - 9) * self.field_width - self.field_width * 0.14,
                                   y=self.width - self.field_border * 0.85)
            else:
                number_label.place(x=self.field_border / 3.2, y=n * self.field_width - self.field_width * 0.2)
                letter_label.place(x=abs(n) * self.field_width - self.field_width * 0.14,
                                   y=self.width - self.field_border * 0.85)
            self.denotation_labels.append(number_label)
            self.denotation_labels.append(letter_label)

    def draw_fields(self):
        for count, field in enumerate(self.fields):
            if self.player_view == "white":
                num = abs(field[1] - 65)
            else:
                num = field[1]
            t = 8
            if num % 8 == 0:
                t = 0
            line = int((num + t - num % 8) / 8)
            pos_x = self.field_border + abs((num - line * 8 - 1) + 1) * int(self.field_width) + 3
            pos_y = self.field_border + (line - 1) * int(self.field_width)
            self.fields[count].append([pos_x, pos_y])
            field[0].place(x=pos_x, y=pos_y)
            field[0].bind("<Button-1>", lambda z="event_str", x=field, y=get_position(self, field[1]):
                                                 self.clicked_field(z, x, y))

    def draw_figures(self, from_where="players"):
        if from_where == "players":
            for pl in self.players:
                for fig in pl.figures:
                    if int((self.lett_to_num[fig.position[0]]) % 2 == 0 and int(fig.position[1]) % 2 == 0) or \
                            int((self.lett_to_num[fig.position[0]]) % 2 != 0 and int(fig.position[int(1)]) % 2 != 0):
                        color = self.black_color_mode
                    else:
                        color = self.white_color_mode
                    img_with_fig = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
                    change = {"white": fig.white_types, "black": fig.black_types}
                    to_paste = Image.open(str(change[fig.color][fig.number]) + ".png").convert("RGBA")
                    to_paste = to_paste.resize([int(self.field_width), int(self.field_width)])
                    draw = ImageDraw.Draw(img_with_fig)
                    draw.rectangle([0, 0, self.field_width, self.field_width], color)
                    img_with_fig.paste(to_paste, (0, 0), to_paste)
                    this_field = self.fields[get_position(self, fig.position) - 1]
                    reference_image = ImageTk.PhotoImage(img_with_fig)
                    this_field[0].config(image=reference_image)
                    this_field[0].image = reference_image
                    if fig.color == self.moving:
                        this_field[0].bind("<Button-1>", lambda z="event_str", x=this_field,
                                                                y=fig.position: self.clicked_field(z, x, y))
                        this_field[0].config(cursor="fleur")
        elif from_where == "log_figures":
            pass

    def clicked_field(self, event, label, pos):
        can_move = 0
        for fig in self.change_right[self.moving].figures:
            if fig.position == pos:
                self.unmark()
                img = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
                to_paste = Image.open(str(fig.name) + ".png").convert("RGBA")
                to_paste = to_paste.resize([int(self.field_width), int(self.field_width)])
                draw = ImageDraw.Draw(img)
                draw.rectangle([0, 0, self.field_width, self.field_width], self.click_color)
                img.paste(to_paste, (0, 0), to_paste)
                reference_image = ImageTk.PhotoImage(img)
                label[0].config(image=reference_image)
                label[0].image = reference_image
                self.marked = [label[0], pos, str(fig.name) + ".png"]
                break
            elif self.marked != [0, 0, 0] and fig.position == self.marked[1] and pos not in \
                    [f.position for f in self.change_right[self.moving].figures] and self.observing == 0:
                event = check_movement_correctness(self, fig.position, pos, fig)
                if event in [1, 3.0, 3.5] or (type(event).__name__ != "int" and type(event).__name__ != "float" and "4" in event):
                    buff_fig_pos = fig.position
                    fig.position = pos
                    a = 0
                    for count, opp_fig in enumerate(self.change_opp[self.moving].figures):
                        if pos == opp_fig.position:
                            a = 1
                            opp_fig_buff = opp_fig
                            if count < self.change_opp[self.moving].king_number:
                                self.change_opp[self.moving].king_number -= 1
                            self.change_opp[self.moving].figures.pop(count)
                            if detect_check(self, "self") == 0:
                                self.change_opp[self.moving].figures.append(opp_fig_buff)
                                fig.position = buff_fig_pos
                                can_move = 1
                            else:
                                self.unmark()
                    if detect_check(self, "self") == 1 and a == 0:
                        if self.marked[2][5:len(self.marked[2]) - 4] != "King":
                            mixer.music.load('check_warning.mp3')
                            mixer.music.play()
                            self.mark_king("red", 1)
                        a = 1
                    if a == 0:
                        can_move = 1
                    if can_move == 1:
                        fig.position = buff_fig_pos
                        if type(event).__name__ != "int" and type(event).__name__ != "float" and "4" in event:
                            self.move_to(label[0], pos, fig, [0, "enpassant", "write"])
                        elif event == 3.0:
                            self.move_to(label[0], pos, fig, [0, "castlingLeft", "write"])
                        elif event == 3.5:
                            self.move_to(label[0], pos, fig, [0, "castlingRight", "write"])
                        else:
                            self.move_to(label[0], pos, fig, [0, "just_move", "write"])
                        if type(event).__name__ != "int" and type(event).__name__ != "float" and "4" in event:
                            position = event[1:]
                            field_color = self.get_color(position)
                            img = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
                            draw = ImageDraw.Draw(img)
                            draw.rectangle([0, 0, self.field_width, self.field_width], field_color)
                            reference_image1 = ImageTk.PhotoImage(img)
                            for field in self.fields:
                                if field[1] == get_position(self, position):
                                    field[0].config(image=reference_image1)
                                    field[0].image = reference_image1
                        elif event == 3.0:
                            for f in self.change_right[self.moving].figures:
                                if f.name[5:] == "Rook" and f.special == "LeftRook":
                                    if self.moving == "white":
                                        left_rook_label = self.fields[3]
                                        self.marked = [self.fields[0][0], "A1", str(f.name) + ".png"]
                                    else:
                                        left_rook_label = self.fields[59]
                                        self.marked = [self.fields[59][0], "A8", str(f.name) + ".png"]
                                    self.move_to(left_rook_label[0], get_position(self, get_position(self, f.position) + 3), f, [0, "castlingLeft", ""])
                        elif event == 3.5:
                            for f in self.change_right[self.moving].figures:
                                if f.name[5:] == "Rook" and f.special == "RightRook":
                                    if self.moving == "white":
                                        right_rook_label = self.fields[5]
                                        self.marked = [self.fields[7][0], "H1", str(f.name) + ".png"]
                                    else:
                                        right_rook_label = self.fields[61]
                                        self.marked = [self.fields[63][0], "H8", str(f.name) + ".png"]
                                    self.move_to(right_rook_label[0], get_position(self, get_position(self, f.position) - 2), f, [0, "castlingRight", ""])
                        if self.moving == "white":
                            self.moving = "black"
                        else:
                            self.moving = "white"
                        self.change_opp[self.moving].moving = 0
                        self.change_opp[self.moving].update_timer()
                        self.change_right[self.moving].moving = 1
                        self.change_right[self.moving].update_timer(resume=1)
                    else:
                        fig.position = buff_fig_pos
                        self.unmark()
                elif check_movement_correctness(self, fig.position, pos, fig) == 2:
                    self.choose_figure(label[0], pos, fig)
                else:
                    self.unmark()
                break
            elif self.observing == 1:
                self.unmark()

    def switch_view(self):
        if self.player_view == "white":
            self.player_view = "black"
        else:
            self.player_view = "white"
        self.draw_fields()
        if self.choosing_opened != [0, [0, 0, 0]]:
            self.choose_fig_frame.place_forget()
            self.choose_fig_frame.destroy()
            self.choose_fig_frame = 0
            self.choosing_opened = [0, [0, 0, 0]]
            self.choose_figure(self.choosing_opened[1][0], self.choosing_opened[1][1], self.choosing_opened[1][2])
        for l in self.denotation_labels:
            del l
        for n in range(1, 9):
            number_label = Label(self.master, text=str(n), font="Arial 15 bold", bg=self.board_border_color, fg="white",
                                 bd=0)
            letter_label = Label(self.master, text=self.num_to_lett[abs(n - 9)], font="Arial 15 bold",
                                 bg=self.board_border_color, fg="white", bd=0)
            if self.player_view == "white":
                number_label.place(x=self.field_border / 3.2, y=abs(n - 9) * self.field_width - self.field_width * 0.2)
                letter_label.place(x=abs(n - 9) * self.field_width - self.field_width * 0.14,
                                   y=self.width - self.field_border * 0.85)
            else:
                number_label.place(x=self.field_border / 3.2, y=n * self.field_width - self.field_width * 0.2)
                letter_label.place(x=abs(n) * self.field_width - self.field_width * 0.14,
                                   y=self.width - self.field_border * 0.85)
            self.denotation_labels.append(number_label)
            self.denotation_labels.append(letter_label)
        l = self.players[0].timer_label
        self.players[0].timer_label = self.players[1].timer_label
        self.players[1].timer_label = l
        for pl in self.players:
            pl.update_timer()
        for pl in self.players:
            if pl.profile_position == "up":
                pl.draw_profile("down")
                pl.profile_position = "down"
            else:
                pl.draw_profile("up")
                pl.profile_position = "up"

    def get_color(self, coord):
        if int((self.lett_to_num[coord[0]]) % 2 == 0 and int(coord[1]) % 2 == 0) or \
                int((self.lett_to_num[coord[0]]) % 2 != 0 and int(coord[int(1)]) % 2 != 0):
            return self.black_color_mode
        else:
            return self.white_color_mode

    def unmark(self):
        if self.marked != [0, 0, 0]:
            img = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
            to_paste = Image.open(self.marked[2]).convert("RGBA")
            to_paste = to_paste.resize([int(self.field_width), int(self.field_width)])
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, self.field_width, self.field_width], self.get_color(self.marked[1]))
            img.paste(to_paste, (0, 0), to_paste)
            reference_image = ImageTk.PhotoImage(img)
            self.marked[0].config(image=reference_image)
            self.marked[0].image = reference_image
            self.marked = [0, 0, 0]

    def move_to(self, label, pos, fig, special):  # special=[destroy_choosing_frame: 0 or 1, type of move, write to log]
        if special[1] != "x":
            prev_pos = fig.position
            change_fig_name = {"white": "Black", "black": "White"}
            img = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
            if special[1] != "just_move" and special[1] != "enpassant" and "castling" not in special[1]:
                to_paste = Image.open(special[1] + ".png").convert("RGBA")
                fig.name = special[1]
                fig.made_on_last_line = 1
                self.choose_fig_frame.place_forget()
                self.choose_fig_frame.destroy()
                self.choose_fig_frame = 0
            else:
                to_paste = Image.open(self.marked[2]).convert("RGBA")
            to_paste = to_paste.resize([int(self.field_width), int(self.field_width)])
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, self.field_width, self.field_width], self.get_color(pos))
            img.paste(to_paste, (0, 0), to_paste)
            reference_image = ImageTk.PhotoImage(img)
            label.config(image=reference_image)
            label.image = reference_image
            label.config(cursor="fleur")
            draw_empty_field = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
            draw_1 = ImageDraw.Draw(draw_empty_field)
            draw_1.rectangle([0, 0, self.field_width, self.field_width], self.get_color(self.marked[1]))
            reference_image_1 = ImageTk.PhotoImage(draw_empty_field)
            this_field = self.fields[get_position(self, fig.position) - 1]
            this_field[0].config(image=reference_image_1)
            this_field[0].image = reference_image_1
            this_field[0].config(cursor='')
            self.marked = [0, 0, 0]
            fig.position = pos
            self.change_right[self.moving].figures_positions = []
            thrown_out = 0
            if pos in [fig.position for fig in self.change_opp[self.moving].figures]:
                for count, f in enumerate(self.change_opp[self.moving].figures):
                    if f.position == pos:
                        thrown_out = 1
                        if self.change_opp[self.moving].figures[count].made_on_last_line == 1:
                            self.change_opp[self.moving].add_to_death_list(change_fig_name[self.moving] + "Pawn")
                            self.change_opp[self.moving].thrown_value += 1
                        else:
                            self.change_opp[self.moving].add_to_death_list(self.change_opp[self.moving].figures[count].name)
                            self.change_opp[self.moving].thrown_value += self.change_opp[self.moving].figures[count].value
                        self.players[0].update_thrown_value_label()
                        self.players[1].update_thrown_value_label()
                        if count < self.change_opp[self.moving].king_number:
                            self.change_opp[self.moving].king_number -= 1
                        print("poped", self.change_opp[self.moving].figures[count].name, "on", f.position)
                        self.change_opp[self.moving].figures.pop(count)
                        break
            if special[1] == "enpassant":
                if self.moving == "white":
                    x = 1
                else:
                    x = -1
                for count, figure in enumerate(self.change_opp[self.moving].figures):
                    if get_position(self, figure.position) == get_position(self, pos) - 8 * x:
                        self.change_opp[self.moving].add_to_death_list(self.change_opp[self.moving].figures[count].name)
                        self.change_opp[self.moving].thrown_value += self.change_opp[self.moving].figures[count].value
                        self.players[0].update_thrown_value_label()
                        self.players[1].update_thrown_value_label()
                        if count < self.change_opp[self.moving].king_number:
                            self.change_opp[self.moving].king_number -= 1
                        # print("poped", self.change_opp[self.moving].figures[count].name, "on", figure.position)
                        self.change_opp[self.moving].figures.pop(count)
                        break
            for l in self.fields:
                l[0].config(cursor='')
            for curs_fig in [fig.position for fig in self.change_opp[self.moving].figures]:
                self.fields[get_position(self, curs_fig) - 1][0].config(cursor="fleur")
            if detect_check_mate(self, "opp") == 1:
                self.show_results(self.change_right[self.moving], "by checkmate")
            elif detect_draw(self, "opp") == 1:
                self.show_results(self.change_right[self.moving], "draw")
            elif detect_check(self, "opp") == 1:
                mixer.music.load('check.mp3')
            elif "castling" in special[1]:
                mixer.music.load('castling.mp3')
            elif "0" in special[2]:
                mixer.music.load('last_line.mp3')
            elif thrown_out == 1 or special[1] == "enpassant":
                mixer.music.load('throw_out.mp3')
            else:
                mixer.music.load('move.mp3')
            mixer.music.play()
            if "write" in special[2]:
                if "0" in special[2]:
                    last_line = "1" + special[2][special[2].find("0") + 1:]
                else:
                    last_line = "0"
                if special[1] == "castlingLeft":
                    castling = 3.0
                elif special[1] == "castlingRight":
                    castling = 3.5
                else:
                    castling = 0
                if special[1] == "enpassant":
                    enpassant = 1
                    thrown_out = 1
                else:
                    enpassant = 0
                self.add_log_entry(fig, prev_pos, pos, thrown_out, last_line, castling, enpassant, detect_check(self, "opp"))
            for op_fig in self.change_opp[self.moving].figures:
                if op_fig.name[5:] == "Pawn":
                    op_fig.special = 0
            if special[1] != "just_move" and "castling" not in special[1] and special[1] != "enpassant":
                if self.moving == "white":
                    self.moving = "black"
                else:
                    self.moving = "white"
                self.change_right[self.moving].moving = 1
                self.change_right[self.moving].update_timer(resume=1)
                self.change_opp[self.moving].moving = 0
                self.change_opp[self.moving].update_timer()
        else:
            self.choose_fig_frame.place_forget()
            self.choose_fig_frame.destroy()
            self.choose_fig_frame = 0
            self.unmark()
        self.choosing_opened = [0, [0, 0, 0]]

    def choose_figure(self, label, pos, fig):
        if self.choosing_opened == [0, [0, 0, 0]]:
            self.choose_fig_frame = Frame(self.master, bg="white", width=self.field_width,
                                          height=4 * self.field_width + 21)
            if self.moving == "white":
                if self.player_view == "white":
                    frame_x = self.field_border + (self.lett_to_num[pos[0]] - 1) * self.field_width
                    frame_y = self.field_border
                else:
                    frame_x = self.field_border + abs((self.lett_to_num[pos[0]] - 1) - 7) * self.field_width
                    frame_y = self.field_border + 4.2 * self.field_width
            else:
                if self.player_view == "white":
                    frame_x = self.field_border + (self.lett_to_num[pos[0]] - 1) * self.field_width
                    frame_y = self.field_border + 4.2 * self.field_width
                else:
                    frame_x = self.field_border + abs((self.lett_to_num[pos[0]] - 1) - 7) * self.field_width
                    frame_y = self.field_border
            self.choose_fig_frame.place(x=frame_x, y=frame_y)
            for count, figname in enumerate(["Queen", "Bishop", "Knight", "Rook"]):
                img = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
                to_paste = Image.open(self.change_let_to_upp[self.moving] + figname + ".png").convert("RGBA")
                to_paste = to_paste.resize([int(self.field_width), int(self.field_width)])
                draw = ImageDraw.Draw(img)
                draw.rectangle([0, 0, self.field_width, self.field_width], "white")
                img.paste(to_paste, (0, 0), to_paste)
                reference_image = ImageTk.PhotoImage(img)
                b = Button(self.choose_fig_frame, image=reference_image, command=lambda x=figname, y=self.change_let_to_upp[self.moving] + figname:
                    self.move_to(label, pos, fig, [1, y, "write0" + x]))
                b.image = reference_image
                b.place(x=0, y=count * self.field_width)
            f = Frame(self.choose_fig_frame, height=20, width=self.field_width)
            f.pack_propagate(0)
            f.place(x=0, y=4*self.field_width)
            b = Button(f, text="x", font="Arial 12", bg="white", relief=SUNKEN, bd=1,
                       command=lambda: self.move_to(label, pos, fig, [1, "x", ""]))
            b.pack(fill=BOTH, expand=1)
            self.choosing_opened = [1, [label, pos, fig]]

    def mark_king(self, color, n):
        n = n
        n += 1
        if color == "field_color":
            if int((self.lett_to_num[self.change_right[self.moving].figures[
                    self.change_right[self.moving].king_number].position[0]]) % 2 == 0 and int(self.change_right[self.moving].figures[
                    self.change_right[self.moving].king_number].position[1]) % 2 == 0) or \
                    int((self.lett_to_num[self.change_right[self.moving].figures[
                    self.change_right[self.moving].king_number].position[0]]) % 2 != 0 and int(self.change_right[self.moving].figures[
                    self.change_right[self.moving].king_number].position[int(1)]) % 2 != 0):
                color = self.black_color_mode
            else:
                color = self.white_color_mode
        img = Image.new("RGBA", [int(self.field_width), int(self.field_width)])
        to_paste = Image.open(self.change_let_to_upp[self.moving] + "King" + ".png").convert("RGBA")
        to_paste = to_paste.resize([int(self.field_width), int(self.field_width)])
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, self.field_width, self.field_width], color)
        img.paste(to_paste, (0, 0), to_paste)
        reference_image = ImageTk.PhotoImage(img)
        self.fields[get_position(self, self.change_right[self.moving].figures[
            self.change_right[self.moving].king_number].position) - 1][0].config(image=reference_image)
        self.fields[get_position(self, self.change_right[self.moving].figures[
            self.change_right[self.moving].king_number].position) - 1][0].image = reference_image
        if n < 7:
            if n % 2 != 0:
                self.master.after(90, lambda: self.mark_king("red", n))
            else:
                self.master.after(90, lambda: self.mark_king("field_color", n))

    def add_log_entry(self, fig, prev_pos, pos, thrown_out, last_line, castling, enpassant, check):
        shortcuts = {"King": "K", "Queen": "Q", "Bishop": "B", "Knight": "N", "Rook": "R", "Pawn": ""}
        lowered_pos = pos.lower()
        lower_prev_pos = prev_pos.lower()
        figures = []
        button_text = 0
        self.moves_list_index += 1
        for f in self.change_right[self.moving].figures:
            if f.name == fig.name:
                figures.append(f)
        true_table = []
        if len(figures) > 1:
            buffer_pos = fig.position
            fig.position = prev_pos
            for fi in figures:
                event = check_movement_correctness(self, fi.position, pos, fi, "normal")
                if (event == 1 or event == 2 or (type(event).__name__ != "int" and "4" in event)) and fi.position != prev_pos:
                    true_table.append(fi)
            true_table.append(fig)
            if len(true_table) > 1:
                if true_table[0].position[0] == true_table[1].position[0]:
                    to_add = lower_prev_pos[1]
                elif true_table[0].position[1] == true_table[1].position[1]:
                    to_add = lower_prev_pos[0]
                else:
                    to_add = lower_prev_pos[0].lower()
            else:
                to_add = ""
            fig.position = buffer_pos
        else:
            to_add = ""
        if castling not in [3.0, 3.5]:
            if "1" not in last_line:
                if thrown_out == 1:
                    if fig.name[5:] != "Pawn":
                        button_text = shortcuts[fig.name[5:]] + to_add + "x" + lowered_pos
                    else:
                        button_text = lower_prev_pos[0] + shortcuts[fig.name[5:]] + "x" + lowered_pos
                else:
                    button_text = shortcuts[fig.name[5:]] + to_add + lowered_pos
            else:
                if thrown_out == 1:
                    button_text = lower_prev_pos[0] + "x" + lowered_pos + "=" + shortcuts[last_line[last_line.find("1") + 1:]]
                else:
                    button_text = lowered_pos + "=" + shortcuts[last_line[last_line.find("1") + 1:]]
        else:
            if castling == 3.0:
                button_text = "O-O-O"
            if castling == 3.5:
                button_text = "O-O"
        if check == 1:
            button_text += "+"
        if enpassant == 1 and check != 1:
            button_text += "e.p."
        if self.log_number[0] % 2 == 0:
            frame_color = "#f8f8f8"
        else:
            frame_color = "white"
        if self.log_number[1] == 0:
            entry_frame = Frame(self.log[0], width=self.log[0].winfo_width() - 20, height=self.log_line_height, bg=frame_color)
        else:
            entry_frame = self.log_entries[len(self.log_entries) - 1][0]
        entry_frame.place(x=0, y=self.log_number[0] * self.log_line_height)
        if self.log_number[1] == 0:
            empty_n_label = Label(entry_frame, text=str(self.log_number[0] + 1) + ".", bg=frame_color, font="Arial, 12")
            empty_n_label.place(x=0, y=0)
            empty_button = Button(entry_frame, text=button_text, bg=frame_color, font="Arial, 12", bd=0, relief=FLAT,
                                  command=(lambda x=self.moves_list_index: self.place_figures_from_log(x)))
            empty_button.place(x=(self.log[2] - 20) * 0.3, y=0)
        else:  # if self.log_number[1] == 1:
            empty_button = Button(entry_frame, text=button_text, bg=frame_color, font="Arial, 12", bd=0, relief=FLAT,
                                  command=(lambda x=self.moves_list_index: self.place_figures_from_log(x)))
            empty_button.place(x=(self.log[2] - 20) * 0.6, y=0)
        empty_button.config(cursor="hand2")
        if self.log_number[1] == 1:
            self.log_number[0] += 1
            self.log_number[1] = 0
        else:
            self.log_number[1] += 1
            self.log_entries.append([entry_frame, button_text])
        this_move_figures = []
        for pl in self.players:
            for figure in pl.figures:
                this_move_figures.append(copy.copy(figure))
        self.all_moves.append(button_text)
        self.change_log_scale(self.log[0].winfo_height())

    def change_log_scale(self, log_frame_height):
        if len(self.log_entries) * self.log_line_height <= log_frame_height:
            self.scale_length = int(log_frame_height)
        else:
            self.scale_length = log_frame_height * (log_frame_height / (len(self.log_entries) * self.log_line_height))

        res = log_frame_height / len(self.log_entries)
        self.log[1].config(sliderlength=self.scale_length, resolution=res)
        self.log[1].set(log_frame_height)
        self.change_log_frame(self.log[1].get())

    def change_log_frame(self, scale_value):
        frame_height = self.log[0].winfo_height()
        for entry1 in self.log_entries:
            entry1[0].place_forget()
        upper_entries_border = (len(self.log_entries) * self.log_line_height) * (int(scale_value) / frame_height)
        to_show = []
        for count, entry2 in enumerate(self.log_entries):
            if upper_entries_border - frame_height <= count * self.log_line_height <= int(upper_entries_border + frame_height):
                to_show.append(entry2[0])
        for count, e in enumerate(to_show):
            e.place(x=0, y=self.log_line_height * count)

    def show_results(self, winner, win_type):
        def destroy_table():
            end_game_frame.place_forget()
            end_game_frame.destroy()

        def start_new_game(self):
            for entry in self.log_entries:
                entry[0].place_forget()
                entry[0].destroy()
            self.log_entries = []
            destroy_table()
            for pl in self.players:
                pl.update_timer(minutes="10")
            del self.players[0]
            del self.players[0]

            self.Environment.open_page(self.Environment.initialize_tkinter)
            self.Environment.open_page(self.Environment.show_start_window)
            del self
        for pl in self.players:
            pl.update_timer(pause=1)
        mixer.music.load("game_end.mp3")
        mixer.music.play()
        window_w = 0.5 * self.width
        window_h = 0.4 * self.width
        tk_width = self.width
        tk_height = self.master.winfo_screenheight()
        window_x = (tk_width - window_w) / 2
        window_y = (tk_height - window_h) / 2
        end_game_frame = Frame(self.master, width=window_w, height=window_h, bg="white", bd=4, relief=SUNKEN)
        end_game_frame.place(x=window_x, y=window_y)
        end_game_frame.pack_propagate(0)

        if win_type == "draw":
            color_label_text = "Draw!"
        else:
            color_label_text = winner.color[0].upper() + winner.color[1:] + " won"
        color_label = Label(end_game_frame, text=color_label_text, font="Arial, 20", bg="white")
        color_label.pack()

        if win_type == "draw":
            name_label_text = "draw by stalemate"
        else:
            name_label_text = winner.name + " won " + win_type
        name_label = Label(end_game_frame, text=name_label_text, font="Arial, 17", bg="white")
        name_label.pack()

        exit_button = Button(end_game_frame, text="    Exit    ", font="Arial, 15", command=lambda: self.root.destroy())
        exit_button.pack(side=BOTTOM)

        back_to_game_button = Button(end_game_frame, text="Back to game", font="Arial, 15", command=destroy_table)
        back_to_game_button.pack(side=BOTTOM)

        new_game_button = Button(end_game_frame, text="  New game  ", font="Arial, 15", command=lambda: start_new_game(self))
        new_game_button.pack(side=BOTTOM)

    def get_fieled_from_coords(self):
        pass

    def place_figures_from_log(self, move_index):
        moves_to_do = self.all_moves[:move_index]
        shortcuts = {"K": "King", "Q": "Queen", "B": "Bishop", "N": "Knight", "R": "Rook", "": "Pawn"}
        if move_index != len(self.all_moves):
            self.observing = 1
        else:
            self.observing = 0
        print(moves_to_do, self.observing, move_index)

        self.create_fields()
        self.draw_fields()

        for field in self.fields:
            field[0].unbind("<Button 1>")

        for count, str_move in enumerate(moves_to_do):
            if count % 2 == 0:  # white
                if "x" in str_move:
                    x_index = str_move.find("x")
                    if str_move[x_index - 1].islower():
                        pass


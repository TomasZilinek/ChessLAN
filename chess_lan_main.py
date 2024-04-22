from tkinter import *
import chess_lan_board
import chess_lan_player
from PIL import ImageTk, Image
from chess_lan_functions import get_possible_moves
# from chess_lan_communicator import Communicator


class Environment:
    def __init__(self):
        self.root = 0
        self.game_root = 0
        self.tk_width = 0
        self.tk_height = 0
        self.Board = 0
        self.window_w = self.tk_width * 0.5
        self.window_h = self.tk_height * 0.65
        self.window_x = (self.tk_width - self.window_w) / 2
        self.window_y = (self.tk_height - self.window_h) / 2
        # self.communicator = Communicator(self.root)
        self.open_page(self.initialize_tkinter)
        self.show_start_window()

    def start_game(self, white_player_name, black_player_name, game_time):
        def switch_view():
            self.Board.switch_view()
        game_time = game_time.replace(" min", "")

        def pressed_key(event):
            if event.char == "w":
                for count, f in enumerate(WhitePlayer.figures):
                    print(f.name, "on", f.position, "possible moves:", get_possible_moves(self.Board, f))
                print("___________________________________________________")
            elif event.char == "b":
                for count, f in enumerate(BlackPlayer.figures):
                    print(f.name, "on", f.position, "possible moves:", get_possible_moves(self.Board, f))
                print("___________________________________________________")
            elif event.char == "l":
                print(self.Board.all_moves)

        self.root.attributes("-fullscreen", True)
        bg_color = "#404040"
        self.root.config(bg=bg_color)

        # middle frame #
        tool_frame_width = self.tk_width * 0.25
        board_border_color = "#553f2b"
        board_width = self.tk_height * 0.85
        margin = (self.tk_height - board_width) / 2
        middle_frame = Frame(self.root, width=board_width, height=self.tk_height, bg=bg_color)
        middle_frame_x = int((self.tk_width - board_width - tool_frame_width) / 1.65)
        middle_frame_y = 0
        middle_frame.place(x=middle_frame_x, y=middle_frame_y)
        board_frame = Frame(middle_frame, width=board_width, height=board_width, bg=board_border_color, bd=2, relief=RAISED)
        board_frame.place(x=0, y=margin)

        self.root.bind("<Key>", pressed_key)

        white_player_n = white_player_name
        black_player_n = black_player_name
        if white_player_n == "":
            white_player_n = "player1"
        if black_player_n == "":
            black_player_n = "player2"
        WhitePlayer = chess_lan_player.Player("white", white_player_n, middle_frame, "down", margin, board_width, bg_color, self.root)
        BlackPlayer = chess_lan_player.Player("black", black_player_n, middle_frame, "up", margin, board_width, bg_color, self.root)

        self.Board = chess_lan_board.Board(self, board_frame, middle_frame, board_width, "white", board_border_color,
                                  [WhitePlayer, BlackPlayer], game_time, self.root)
        WhitePlayer.get_info(BlackPlayer, self.Board)
        BlackPlayer.get_info(WhitePlayer, self.Board)

        # tool frame #
        tool_frame_width = self.tk_width * 0.25
        tool_frame = Frame(self.root, width=tool_frame_width, height=self.tk_height, relief=SUNKEN, bd=3, bg="#737373")
        tool_frame.place(x=self.tk_width - tool_frame_width, y=0)

        switch_but_image = ImageTk.PhotoImage(Image.open("switch.png").resize([40, 40]))
        switch_button = Button(tool_frame, image=switch_but_image, command=switch_view)
        switch_button.image = switch_but_image
        switch_button.place(x=20, y=20)

        log_frame_height = 0.5 * self.tk_height
        log_frame_width = 0.9 * tool_frame_width
        log_frame = Frame(tool_frame, width=log_frame_width, height=log_frame_height, bg="white", bd=2, relief=SUNKEN)
        log_frame.place(x=0.05 * tool_frame_width, y=100)
        in_log_frame = Frame(log_frame, width=log_frame_width, height=log_frame_height, bg="white")
        in_log_frame.place(x=0, y=0)
        log_scale = Scale(in_log_frame, from_=0, to=int(log_frame_height), width=15, resolution=20)
        log_scale.config(length=log_frame_height, showvalue=0, borderwidth=0, sliderlength=log_frame_height)
        log_scale.place(x=log_frame_width - 20, y=0)
        log = [in_log_frame, log_scale, log_frame_width, "white"]
        self.Board.log = log
        self.Board.log[1].config(command=self.Board.change_log_frame)

        resign_but_img = ImageTk.PhotoImage(Image.open("resign_flag.jpg").resize([40, 40]))
        resign_image_button = Button(tool_frame, image=resign_but_img, bd=0,
                                     command=lambda: self.Board.show_results(self.Board.change_right[self.Board.moving],
                                                                             "by resignation"))
        resign_image_button.image = resign_but_img
        resign_image_button.place(x=20, y=120 + log_frame_height)
        resign_text_button = Button(tool_frame, text="resign", font="Arial, 17", bd=0,
                                    command=lambda: self.Board.show_results(self.Board.change_right[self.Board.moving],
                                                                            "by resignation"))
        resign_text_button.place(x=60, y=120 + log_frame_height)

        draw_but_img = ImageTk.PhotoImage(Image.open("draw_picture.png").resize([40, 40]))
        draw_image_button = Button(tool_frame, image=draw_but_img, bd=0)
        draw_image_button.image = draw_but_img
        draw_image_button.place(x=170, y=120 + log_frame_height)
        draw_text_button = Button(tool_frame, text="draw", font="Arial, 17", bd=0)
        draw_text_button.place(x=210, y=120 + log_frame_height)

        exit_button = Button(tool_frame, text="Exit", font=("Arial", 20), command=lambda: self.root.destroy())
        exit_button.place(x=20, y=self.tk_height * 0.9)

        # left frame
        left_frame_width = middle_frame_x
        left_frame = Frame(self.root, width=left_frame_width, height=self.tk_height, bg=bg_color)
        left_frame.place(x=0, y=0)

        clock_width = left_frame_width * 0.7
        clock_height = self.tk_height * 0.35
        clock_frame = Frame(left_frame, width=clock_width, height=clock_height, bg=board_border_color, bd=1, relief=SUNKEN)
        clock_frame.place(x=int((left_frame_width - clock_width) / 2), y=int((self.tk_height - clock_height) / 2))
        timer_height = clock_height * 0.6 / 2
        timer_width = clock_width * 0.7
        timer_margin = 0.125  # % from timer_height

        timer_color = "#e8e9b8"
        upper_timer_frame = Frame(clock_frame, width=timer_width, height=timer_height, bg=timer_color)
        upper_timer_frame.place(x=(clock_width - timer_width) / 2, y=clock_height * timer_margin)
        upper_timer_label = Label(upper_timer_frame, text=game_time + ":00", font="Arial 25", bg=timer_color)
        upper_timer_label.place(x=0.14 * timer_width, y=0.25 * timer_height)

        lower_timer_frame = Frame(clock_frame, width=timer_width, height=timer_height, bg=timer_color)
        lower_timer_frame.place(x=(clock_width - timer_width) / 2, y=clock_height * (1 - timer_margin) - timer_height)
        lower_timer_label = Label(lower_timer_frame, text=game_time + ":00", font="Arial 25", bg=timer_color)
        lower_timer_label.place(x=0.14 * timer_width, y=0.25 * timer_height)

        WhitePlayer.timer_label = [lower_timer_label, 0]  # [label, whether placed normally or shifted]
        BlackPlayer.timer_label = [upper_timer_label, 0]
        WhitePlayer.update_timer(minutes=game_time, timer_dimensions=[timer_width, timer_height])
        BlackPlayer.update_timer(minutes=game_time, timer_dimensions=[timer_width, timer_height])
        self.root.mainloop()

    def new_game_window(self):
        self.root.title("Chess: New game")

        p1_label = Label(self.root, text=" White player name:  ", font="Arial 22")
        p1_label.grid(row=0)
        p2_label = Label(self.root, text=" Black player name:  ", font="Arial 22")
        p2_label.grid(row=1)
        p3_label = Label(self.root, text=" time:  ", font="Arial 22")
        p3_label.grid(row=2, sticky=E)

        textvar1 = StringVar()
        textvar1.set("player 1")
        p1_entry = Entry(self.root, width=17, font="Arial 18", textvariable=textvar1)
        p1_entry.grid(row=0, column=1, ipady=5)

        textvar2 = StringVar()
        textvar2.set("player 2")
        p2_entry = Entry(self.root, width=17, font="Arial 18", text=textvar2)
        p2_entry.grid(row=1, column=1, ipady=5)

        optionvar = StringVar()
        optionvar.set("10 min")
        time_dropdown = OptionMenu(self.root, optionvar, "2 min", "3 min", "5 min", "10 min", "15 min", "45 min")
        time_dropdown.config(font="Arial, 15", width=10)
        time_dropdown.grid(row=2, column=1, columnspan=2, sticky=W)

        submit_button = Button(self.root, text="Submit", font="Arial 17",
                               command=lambda: self.start_game(textvar1.get(), textvar2.get(), optionvar.get()))
        submit_button.grid(row=3, columnspan=2, sticky=W+E)

        connect_button = Button(self.root, text="connect")  # command=self.communicator.connect
        connect_button.grid(row=4, columnspan=2, sticky=W+E)
        self.root.mainloop()

    def show_start_window(self):
        self.root.title("Chess")

        title_label = Label(text="Chess", font="Arial 60 italic")
        title_label.pack(anchor=CENTER)

        new_game_button = Button(self.root, text="New game", font=("Arial", 20),
                                 command=lambda: self.open_page(self.new_game_window))
        new_game_button.pack(pady=20, side=TOP)

        credits_button = Button(self.root, text="Credits", font=("Arial", 20),
                                 command=lambda: self.open_page(self.credits_window))
        credits_button.pack(side=TOP)

        exit_button = Button(self.root, text="Exit", font=("Arial", 20), command=lambda: self.root.destroy())
        exit_button.pack(side=BOTTOM, pady=(0, 60))

        self.root.mainloop()

    def credits_window(self):
        self.root.title("Chess: Credits")

        title_label = Label(text="Credits", font="Arial 40 italic")
        title_label.pack(anchor=CENTER)

        back_button = Button(self.root, text="Back", font=("Arial", 20), command=lambda: self.open_page(self.show_start_window))
        back_button.pack(side=BOTTOM, anchor=W, pady=40, padx=40)

    def open_page(self, function):
        if self.root != 0:
            self.root.destroy()
        self.root = Tk()
        self.get_window_params()
        self.root.geometry('%dx%d+%d+%d' % (self.window_w, self.window_h, self.window_x, self.window_y))
        function()

    def initialize_tkinter(self):
        self.tk_width = self.root.winfo_screenwidth()
        self.tk_height = self.root.winfo_screenheight()
        self.root.title("Chess")

    def get_window_params(self):
        self.tk_width = self.root.winfo_screenwidth()
        self.tk_height = self.root.winfo_screenheight()
        self.window_w = self.tk_width * 0.5
        self.window_h = self.tk_height * 0.65
        self.window_x = (self.tk_width - self.window_w) / 2
        self.window_y = (self.tk_height - self.window_h) / 2


Env = Environment()

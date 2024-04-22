def check_movement_correctness(self, prev_pos, pos, fig, check="normal"):
    opposite_player_figures_pos = [fig.position for fig in self.change_opp[self.moving].figures]
    self_player_figures_pos = [fig.position for fig in self.change_right[self.moving].figures]
    if prev_pos != pos and pos not in self_player_figures_pos:
        if fig.name[5:] == "Pawn":
            if self.moving == "white":
                x = 1
            else:
                x = -1
            if fig.already_moved == 0 and (get_position(self, prev_pos) - get_position(self, pos)) * x == -16 and \
                    get_position(self, get_position(self, prev_pos) + 8 * x) not in self_player_figures_pos and \
                    get_position(self, get_position(self, prev_pos) + 8 * x) not in opposite_player_figures_pos and \
                    pos not in opposite_player_figures_pos:
                if check == "normal":
                    fig.already_moved = 1
                fig.special = "enpassant_possible"
                return 1
            elif (get_position(self, prev_pos) - get_position(self, pos)) * x == -8 and pos not in \
                    opposite_player_figures_pos:
                if pos[1] != "1" and pos[1] != "8":
                    if check == "normal":
                        fig.already_moved = 1
                    return 1
                else:
                    return 2  # got to last line
            else:
                if ((get_position(self, prev_pos) - get_position(self, pos)) * x == -9 or
                        (get_position(self, prev_pos) - get_position(self, pos)) * x == -7) and \
                        pos in opposite_player_figures_pos:
                    if pos[1] != "1" and pos[1] != "8":
                        return 1
                    else:
                        return 2  # got to last line
                elif ((get_position(self, prev_pos) - get_position(self, pos)) * x == -9 or
                        (get_position(self, prev_pos) - get_position(self, pos)) * x == -7) and \
                        pos not in opposite_player_figures_pos:
                    if get_position(self, pos) - 8 * x in [get_position(self, f.position) for f in self.change_opp[self.moving].figures]:
                        for opp_fig in self.change_opp[self.moving].figures:
                            if get_position(self, pos) - 8 * x == get_position(self, opp_fig.position) and \
                                    opp_fig.name[5:] == "Pawn" and opp_fig.special == "enpassant_possible":
                                return "4" + get_position(self, get_position(self, pos) - 8 * x)  # en passant => 4 + passed pawn position
        elif fig.name[5:] == "Knight":
            prev_position_x = int(get_position(self, prev_pos, "line_column")[1]) * self.field_width
            prev_position_y = int(get_position(self, prev_pos, "line_column")[0]) * self.field_width
            dest_x = int(get_position(self, pos, "line_column")[1]) * self.field_width
            dest_y = int(get_position(self, pos, "line_column")[0]) * self.field_width
            if get_position(self, prev_pos) - get_position(self, pos) in [6, 10, 15, 17, -6, -10, -15, -17] and\
                    prev_position_x - 3 * self.field_width <= dest_x <= prev_position_x + 3 * self.field_width and \
                    prev_position_y - 3 * self.field_width <= dest_y <= prev_position_y + 3 * self.field_width:
                return 1
        elif fig.name[5:] == "King":
            if get_position(self, prev_pos) - get_position(self, pos) in [1, 7, 8, 9, -1, -7, -8, -9] and \
                            abs(self.lett_to_num[fig.position[0]] - self.lett_to_num[pos[0]]) < 2:
                if fig.already_moved == 0:
                    if check == "normal":
                        fig.already_moved = 1
                return 1
            # casling start #
            ch = 0
            for self_fig in [f for f in self.change_right[self.moving].figures]:
                if get_position(self, self_fig.position) == get_position(self, fig.position) - 1:
                    ch = 1
            if get_position(self, prev_pos) - get_position(self, pos) == 2 and fig.already_moved == 0 and \
                    detect_check(self, "self") == 0 and ch == 0:
                fig.position = get_position(self, get_position(self, fig.position) - 1)
                if detect_check(self, "self") == 0:
                    fig.position = get_position(self, get_position(self, fig.position) - 1)
                    if detect_check(self, "self") == 0:
                        fig.position = prev_pos
                        for f in self.change_right[self.moving].figures:
                            if f.name[5:] == "Rook" and f.special == "LeftRook" and f.already_moved == 0:
                                return 3.0  # castling left (.0)
                    else:
                        fig.position = prev_pos
                        return 0
                else:
                    fig.position = prev_pos
                    return 0
            ch = 0
            for self_fig in [f for f in self.change_right[self.moving].figures]:
                if get_position(self, self_fig.position) == get_position(self, fig.position) + 1:
                    ch = 1
            if get_position(self, prev_pos) - get_position(self, pos) == -2 and fig.already_moved == 0 and \
                    detect_check(self, "self") == 0 and ch == 0:
                fig.position = get_position(self, get_position(self, fig.position) + 1)
                if detect_check(self, "self") == 0:
                    fig.position = get_position(self, get_position(self, fig.position) + 1)
                    if detect_check(self, "self") == 0:
                        fig.position = prev_pos
                        for f in self.change_right[self.moving].figures:
                            if f.name[5:] == "Rook" and f.special == "RightRook" and f.already_moved == 0:
                                return 3.5  # castling right (.5)
                    else:
                        fig.position = prev_pos
                        return 0
                else:
                    fig.position = prev_pos
                    return 0
            # castling end #
        elif fig.name[5:] == "Bishop":
            ch = 0
            if self.lett_to_num[prev_pos[0]] < self.lett_to_num[pos[0]]:
                hor_k = 1
            else:
                hor_k = -1
            if int(prev_pos[1]) < int(pos[1]):
                ver_k = 1
            else:
                ver_k = -1
            currant_pos = prev_pos
            while currant_pos != pos:
                try:
                    currant_pos = str(self.num_to_lett[self.lett_to_num[currant_pos[0]] + hor_k]) + str(int(currant_pos[1]) + ver_k)
                except:
                    ch = 1
                    break
                if currant_pos in self_player_figures_pos or (currant_pos in opposite_player_figures_pos and currant_pos != pos):
                    ch = 1
                    break
            if ch == 0:
                return 1
        elif fig.name[5:] == "Rook":
            ch = 0
            if pos[0] in prev_pos or pos[1] in prev_pos:
                if self.lett_to_num[prev_pos[0]] < self.lett_to_num[pos[0]]:
                    hor_k = 1
                elif self.lett_to_num[prev_pos[0]] > self.lett_to_num[pos[0]]:
                    hor_k = -1
                else:
                    hor_k = 0
                if int(prev_pos[1]) < int(pos[1]):
                    ver_k = 1
                elif int(prev_pos[1]) > int(pos[1]):
                    ver_k = -1
                else:
                    ver_k = 0
                currant_pos = prev_pos
                while currant_pos != pos:
                    currant_pos = str(self.num_to_lett[self.lett_to_num[currant_pos[0]] + hor_k]) + str(int(currant_pos[1]) + ver_k)
                    if currant_pos in self_player_figures_pos or (currant_pos in opposite_player_figures_pos and currant_pos != pos):
                        ch = 1
                        break
                if ch == 0:
                    return 1
                else:
                    return 0
            else:
                return 0
        elif fig.name[5:] == "Queen":
            ch = 0
            if pos[0] in prev_pos or pos[1] in prev_pos:
                if self.lett_to_num[prev_pos[0]] < self.lett_to_num[pos[0]]:
                    hor_k = 1
                elif self.lett_to_num[prev_pos[0]] > self.lett_to_num[pos[0]]:
                    hor_k = -1
                else:
                    hor_k = 0
                if int(prev_pos[1]) < int(pos[1]):
                    ver_k = 1
                elif int(prev_pos[1]) > int(pos[1]):
                    ver_k = -1
                else:
                    ver_k = 0
                currant_pos = prev_pos
                while currant_pos != pos:
                    currant_pos = str(self.num_to_lett[self.lett_to_num[currant_pos[0]] + hor_k]) + str(
                        int(currant_pos[1]) + ver_k)
                    if currant_pos in self_player_figures_pos or (
                            currant_pos in opposite_player_figures_pos and currant_pos != pos):
                        ch = 1
                        break
                if ch == 0:
                    return 1
                else:
                    return 0
            else:
                if self.lett_to_num[prev_pos[0]] < self.lett_to_num[pos[0]]:
                    hor_k = 1
                else:
                    hor_k = -1
                if int(prev_pos[1]) < int(pos[1]):
                    ver_k = 1
                else:
                    ver_k = -1
                currant_pos = prev_pos
                while currant_pos != pos:
                    try:
                        currant_pos = str(self.num_to_lett[self.lett_to_num[currant_pos[0]] + hor_k]) + str(
                            int(currant_pos[1]) + ver_k)
                    except:
                        ch = 1
                        break
                    if currant_pos in self_player_figures_pos or (
                            currant_pos in opposite_player_figures_pos and currant_pos != pos):
                        ch = 1
                        break
                if ch == 0:
                    return 1
    return 0


def get_position(self, input, tp="normal"):
    if tp == "line_column":
        if type(input).__name__ == "int":
            if input >= 8:
                t = 8
                if input % 8 == 0:
                    t = 0
                line = int((input + t - input % 8) / 8)
                column = int(self.lett_to_num[get_position(self, input, "normal")[0]])
                return [line, column]
            else:
                column = int(self.lett_to_num[get_position(self, input, "normal")[0]])
                return [1, column]
        else:
            return get_position(self, get_position(self, input, "normal"), "line_column")
    else:
        if type(input).__name__ == "int":
            if input >= 8:
                t = 8
                if input % 8 == 0:
                    t = 0
                line = int((input + t - input % 8) / 8)
                if t == 0:
                    letter = "H"
                else:
                    letter = self.num_to_lett[input % 8]
                return letter + str(line)
            else:
                if input == 0:
                    return "H1"
                else:
                    return self.num_to_lett[input] + "1"
        else:
            return self.lett_to_num[input[0].upper()] + (int(input[1]) - 1) * 8


def detect_check(self, who, b="f"):
    got_check = 0
    if who == "self":
        got_check = self.moving
    elif who == "opp":
        if self.moving == "white":
            got_check = "black"
        else:
            got_check = "white"
    checking_player_figures = [fig for fig in self.change_opp[got_check].figures]
    not_checking_player_figures = [fig for fig in self.change_right[got_check].figures]
    str_king_position = self.change_right[got_check].figures[self.change_right[got_check].king_number].position
    for fig in checking_player_figures:
        if fig.name[5:] == "Pawn":
            if got_check == "white":
                x = 1
            else:
                x = -1
            if (get_position(self, str_king_position) + x * 8 + 1 == get_position(self, fig.position) or
                    get_position(self, str_king_position) + x * 8 - 1 == get_position(self, fig.position)) and\
                    abs(self.lett_to_num[str_king_position[0]] - self.lett_to_num[fig.position[0]]) != 7:
                if b == "g":
                    print(fig.name, "on", fig.position, "checked", got_check, "king on", str_king_position)
                return 1
        elif fig.name[5:] == "Knight":
            for p in [6, 10, 15, 17, -6, -10, -15, -17]:
                prev_position_x = int(get_position(self, fig.position, "line_column")[0]) * self.field_width
                prev_position_y = int(get_position(self, fig.position, "line_column")[1]) * self.field_width
                if get_position(self, fig.position) + p >= 0:
                    dest_x = int(get_position(self, get_position(self, fig.position) + p, "line_column")[0]) * self.field_width
                    dest_y = int(get_position(self, get_position(self, fig.position) + p, "line_column")[1]) * self.field_width
                    if get_position(self, str_king_position) == get_position(self, fig.position) + p and \
                            get_position(self, fig.position) - get_position(self, fig.position) + p in [6, 10, 15, 17, -6, -10, -15, -17] and \
                            prev_position_x - 5 * self.field_width <= dest_x < prev_position_x + 5 * self.field_width and \
                            prev_position_y - 5 * self.field_width <= dest_y < prev_position_y + 5 * self.field_width:
                        if b == "g":
                            print(fig.name, "on", fig.position, "checked", got_check, "king on", str_king_position)
                        return 1
        elif fig.name[5:] == "Bishop":
            for direction in [[1, 1], [1, -1], [-1, -1], [-1, 1]]:
                currant_pos = fig.position
                while currant_pos != str_king_position:
                    try:
                        if self.lett_to_num[currant_pos[0]] + direction[0] != 0 and int(currant_pos[1]) + direction[1] != 0:
                            if len(currant_pos) != 3 and currant_pos[1] != 9:
                                currant_pos = str(self.num_to_lett[self.lett_to_num[currant_pos[0]] + direction[0]]) + str(int(currant_pos[1]) + direction[1])
                            else:
                                break
                        else:
                            break
                    except:
                        break
                    if currant_pos in [f.position for f in checking_player_figures] or (currant_pos in [f.position for f in not_checking_player_figures] and
                            currant_pos != str_king_position):
                        break
                if currant_pos == str_king_position:
                    if b == "g":
                        print(fig.name, "on", fig.position, "checked", got_check, "king on", str_king_position)
                    return 1
        elif fig.name[5:] == "Rook":
            for direction in [[1, 0], [0, -1], [-1, 0], [0, 1]]:
                currant_pos = fig.position
                if str_king_position[0] in fig.position or str_king_position[1] in fig.position:
                    while currant_pos != str_king_position:
                        try:
                            if self.lett_to_num[currant_pos[0]] + direction[0] != 0 and int(currant_pos[1]) + direction[1] != 0:
                                currant_pos = str(self.num_to_lett[self.lett_to_num[currant_pos[0]] + direction[0]]) + str(int(currant_pos[1]) + direction[1])
                            else:
                                break
                        except:
                            break
                        if currant_pos in [f.position for f in checking_player_figures] or (currant_pos in [f.position for f in not_checking_player_figures] and currant_pos != str_king_position):
                            break
                        if currant_pos == str_king_position:
                            if b == "g":
                                print(fig.name, "on", fig.position, "checked", got_check, "king on", str_king_position)
                            return 1
        elif fig.name[5:] == "Queen":
            for direction in [[1, 0], [0, -1], [-1, 0], [0, 1]]:
                currant_pos = fig.position
                if str_king_position[0] in fig.position or str_king_position[1] in fig.position:
                    while currant_pos != str_king_position:
                        try:
                            if self.lett_to_num[currant_pos[0]] + direction[0] != 0 and int(currant_pos[1]) + direction[1] != 0:
                                currant_pos = str(self.num_to_lett[self.lett_to_num[currant_pos[0]] + direction[0]]) + str(int(currant_pos[1]) + direction[1])
                                if len(currant_pos) == 3 or currant_pos[1] == 9:
                                    break
                            else:
                                break
                        except:
                            break
                        if currant_pos in [f.position for f in checking_player_figures] or (currant_pos in [f.position for f in not_checking_player_figures] and currant_pos != str_king_position):
                            break
                        if currant_pos == str_king_position:
                            if b == "g":
                                print(fig.name, "on", fig.position, "checked 1", got_check, "king on", str_king_position)
                            return 1
            for direction in [[1, 1], [1, -1], [-1, -1], [-1, 1]]:
                currant_pos = fig.position
                while currant_pos != str_king_position:
                    try:
                        if self.lett_to_num[currant_pos[0]] + direction[0] != 0 and int(currant_pos[1]) + direction[1] != 0:
                            currant_pos = str(self.num_to_lett[self.lett_to_num[currant_pos[0]] + direction[0]]) + str(int(currant_pos[1]) + direction[1])
                            if len(currant_pos) == 3 or currant_pos[1] == 9:
                                break
                        else:
                            break
                    except:
                        break
                    if currant_pos in [f.position for f in checking_player_figures] or (currant_pos in [f.position for f in not_checking_player_figures] and
                            currant_pos != str_king_position):
                        break
                if currant_pos == str_king_position:
                    if b == "g":
                        print(fig.name, "on", fig.position, "checked 2", got_check, "king on", str_king_position)
                    return 1
        elif fig.name[5:] == "King":
            for direction in [7, 8, 9, -1, 1, -7, -8, -9]:
                if get_position(self, str_king_position) == get_position(self, fig.position) + direction and \
                                abs(self.lett_to_num[str_king_position[0]] - self.lett_to_num[fig.position[0]]) < 2:
                    if b == "g":
                        print(fig.name, "on", fig.position, "checked", got_check, "king on", str_king_position)
                    return 1
    return 0


def get_possible_moves(self, fig):
    possible_moves = []
    thrown_out = 0
    thrown_figures = []
    for count, field in enumerate(self.fields):
        event = check_movement_correctness(self, fig.position, get_position(self, count), fig, "find")
        if event in [1, 2, 3.0, 3.5] or (type(event).__name__ != "int" and type(event).__name__ != "float" and "4" in event):
            buff_fig_pos = fig.position
            fig.position = get_position(self, count)
            for count1, opp_fig in enumerate(self.change_opp[fig.color].figures):
                if fig.position == opp_fig.position and opp_fig.name[5:] != "King":
                    thrown_out = 1
                    thrown_figures.append(opp_fig)
                    if count1 < self.change_opp[self.moving].king_number:
                        self.change_opp[self.moving].king_number -= 1
                    print("kicked", self.change_opp[self.moving].figures[count1].name, "on", opp_fig.position)
                    self.change_opp[self.moving].figures.pop(count1)
            if detect_check(self, "self") == 0:
                possible_moves.append(get_position(self, count))
            if thrown_out == 1:
                for op_fig in thrown_figures:
                    self.change_opp[self.moving].figures.append(op_fig)
                thrown_figures = []
                thrown_out = 0
            fig.position = buff_fig_pos
    return possible_moves


def detect_check_mate(self, who):
    if detect_check(self, who) == 1:
        got_check = ""
        if who == "self":
            got_check = self.moving.color
        elif who == "opp":
            if self.moving == "white":
                got_check = "black"
            else:
                got_check = "white"
        not_checking_player_figures = [fig for fig in self.change_right[got_check].figures]
        moving = self.moving
        self.moving = got_check
        for fig in not_checking_player_figures:
            moves = get_possible_moves(self, fig)
            if len(moves) > 0:
                self.moving = moving
                return 0
        self.moving = moving
        return 1


def detect_draw(self, who):
    got_draw = ""
    if who == "self":
        got_draw = self.moving.color
    elif who == "opp":
        if self.moving == "white":
            got_draw = "black"
        else:
            got_draw = "white"
    got_draw_player_figures = [fig for fig in self.change_right[got_draw].figures]
    moving = self.moving
    self.moving = got_draw
    all_moves = 0
    for fig in got_draw_player_figures:
        all_moves += len(get_possible_moves(self, fig))
        if all_moves > 0:
            self.moving = moving
            return 0
    self.moving = moving
    return 1

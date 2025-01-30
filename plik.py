import wx
import random


# Okienko aplikacji
class NoughtsAndCrossesApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Noughts and Crosses", size=(500, 600))
        self.panel = wx.Panel(self)
        self.Centre()
        self.CreateUI_Items()
        self.game = NoughtsAndCrossesLogic()
        self.BindEvents()
        self.reset_game()


    def CreateUI_Items(self):
        # Player selection
        self.mode_label = wx.StaticText(self.panel, label="Choose game mode:")
        self.mode_choice = wx.Choice(self.panel, choices=["Play with Friend", "Play with Computer"])

        self.player1_label = wx.StaticText(self.panel, label="Player 1 Name:")
        self.player1_name = wx.TextCtrl(self.panel)

        self.player2_label = wx.StaticText(self.panel, label="Player 2 Name (or Computer):")
        self.player2_name = wx.TextCtrl(self.panel)

        self.first_player_label = wx.StaticText(self.panel, label="Who goes first?")
        self.first_player_choice = wx.Choice(self.panel, choices=["Player 1", "Player 2"])

        self.start_button = wx.Button(self.panel, label="Start Game")

        # Game field
        self.grid = wx.GridSizer(3, 3, 5, 5)
        self.buttons = [wx.Button(self.panel, id=i, label="") for i in range(1, 10)]
        for button in self.buttons:
            self.grid.Add(button, 0, wx.EXPAND)

        self.message = wx.StaticText(self.panel, label="Welcome to Noughts and Crosses!")
        self.message.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.reset_button = wx.Button(self.panel, label="Reset Game")

        # Main layout
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.mode_label, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.mode_choice, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.player1_label, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.player1_name, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.player2_label, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.player2_name, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.first_player_label, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.first_player_choice, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 10)
        self.main_sizer.Add(self.message, 0, wx.ALL | wx.CENTER, 10)
        self.main_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)
        self.main_sizer.Add(self.reset_button, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)


    def BindEvents(self):
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_click)
        for button in self.buttons:
            button.Bind(wx.EVT_BUTTON, self.on_square_click)
        self.reset_button.Bind(wx.EVT_BUTTON, self.on_reset_click)


    def reset_game(self):
        self.game.reset()
        for button in self.buttons:
            button.SetLabel("")
            button.Enable(False)
        self.message.SetLabel("Welcome to Noughts and Crosses!")
        self.player1_name.SetValue("")
        self.player2_name.SetValue("")
        self.mode_choice.SetSelection(-1)
        self.first_player_choice.SetSelection(-1)


    def on_start_click(self, event):
        mode = self.mode_choice.GetStringSelection()
        player1 = self.player1_name.GetValue().strip()
        player2 = self.player2_name.GetValue().strip()
        first_player = self.first_player_choice.GetStringSelection()

        if not player1 or (not player2 and mode == "Play with Friend"):
            self.message.SetLabel("Please enter valid names for both players!")
            return

        if mode == "Play with Computer":
            player2 = "Computer"

        self.game.set_players(player1, player2)
        self.game.set_first_player(first_player)

        self.message.SetLabel(f"{player1} (X) vs {player2} (O). {first_player} goes first!")

        for button in self.buttons:
            button.Enable(True)

        # If computer goes first, make its move
        if player2 == "Computer" and first_player == "Player 2":
            self.computer_move()


    def on_square_click(self, event):
        button_id = event.GetId()
        button = self.FindWindowById(button_id)
        index = self.buttons.index(button)

        if not self.game.is_square_empty(index):
            return

        symbol = self.game.current_player()
        button.SetLabel(symbol)
        self.game.make_move(index, symbol)

        winner = self.game.check_winner()
        if winner:
            self.message.SetLabel(f"{winner} wins!")
            self.disable_all_buttons()
        elif self.game.is_draw():
            self.message.SetLabel("It's a draw!")
        else:
            self.game.switch_player()
            if self.game.current_player() == "O" and self.game.player2 == "Computer":
                self.computer_move()


    def computer_move(self):
        empty_squares = [i for i, square in enumerate(self.game.board) if square is None]
        if empty_squares:
            move = random.choice(empty_squares)
            self.buttons[move].SetLabel("O")
            self.game.make_move(move, "O")

            winner = self.game.check_winner()
            if winner:
                self.message.SetLabel(f"{winner} wins!")
                self.disable_all_buttons()
            elif self.game.is_draw():
                self.message.SetLabel("It's a draw!")
            else:
                self.game.switch_player()


    def on_reset_click(self, event):
        self.reset_game()


    def disable_all_buttons(self):
        for button in self.buttons:
            button.Enable(False)



class NoughtsAndCrossesLogic:
    def __init__(self):
        self.reset()


    def reset(self):
        self.board = [None] * 9
        self.current_symbol = "X"
        self.player1 = None
        self.player2 = None


    def set_players(self, player1, player2):
        self.player1 = player1
        self.player2 = player2


    def set_first_player(self, first_player):
        if first_player == "Player 2":
            self.current_symbol = "O"
        else:
            self.current_symbol = "X"


    def is_square_empty(self, index):
        return self.board[index] is None


    def make_move(self, index, symbol):
        if self.is_square_empty(index):
            self.board[index] = symbol


    def current_player(self):
        return self.current_symbol


    def switch_player(self):
        self.current_symbol = "O" if self.current_symbol == "X" else "X"


    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] and self.board[combo[0]] is not None:
                return self.player1 if self.board[combo[0]] == "X" else self.player2
        return None


    def is_draw(self):
        return all(square is not None for square in self.board)


if __name__ == "__main__":
    app = wx.App()
    frame = NoughtsAndCrossesApp()
    frame.Show()
    app.MainLoop()
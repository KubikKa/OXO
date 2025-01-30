import wx
import random


# Okienko aplikacji
class NoughtsAndCrossesApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(None, title = "Noughts and Crosses", size=(600, 700))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.Centre()

        self.CreateUI_Items(panel, sizer, buttons)
        self.game = NoughtsAndCrossesLogic()
        self.BindEvents(self.buttons)
        self.reset_game()
        
        self.mode_choice.Bind(wx.EVT_CHOICE, self.mode_name_change)
        sizer.Add(buttons, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=10)


    def CreateUI_Items(self, panel, sizer, buttons):
    # Etykiety i pola tekstowe do wprowadzania danych
        self.message = wx.StaticText(panel, label="Welcome to Noughts and Crosses!")
        sizer.Add(self.message, 0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=10)
        self.message.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # Tryb - komputer/przyjaciel
        self.mode_label = wx.StaticText(panel, label = "Choose game mode:")
        sizer.Add(self.mode_label, 0, wx.ALL | wx.CENTER, border=5)
        self.mode_choice = wx.Choice(panel, choices = ["Play with Friend", "Play with Computer"])
        sizer.Add(self.mode_choice, 0, wx.ALL | wx.CENTER, border=5)

        # Pierwszy gracz - imię
        self.player1_label = wx.StaticText(panel, label = "First player name:")
        sizer.Add(self.player1_label, 0, wx.ALL | wx.CENTER, border=5)
        self.input_player1_name = wx.TextCtrl(panel)
        sizer.Add(self.input_player1_name, 0, wx.ALL | wx.CENTER, border=5)

        # Drugi gracz - imię/Komputer
        self.player2_label = wx.StaticText(panel, label = "Second player name:")
        sizer.Add(self.player2_label, 0, wx.ALL | wx.CENTER, border=5)
        self.input_player2_name = wx.TextCtrl(panel)
        sizer.Add(self.input_player2_name, 0, wx.ALL | wx.CENTER, border=5)

        # Wybór pierwszeństwa
        self.set_out_label = wx.StaticText(panel, label = "Who goes first?")
        sizer.Add(self.set_out_label, 0, wx.ALL | wx.CENTER, border=5)
        self.set_out_choice = wx.Choice(panel, choices=["First player", "Second player"])
        sizer.Add(self.set_out_choice, 0, wx.ALL | wx.CENTER, border=5)

        # Przycisk start
        self.start_button = wx.Button(panel, label = "Start Game")
        sizer.Add(self.start_button,  0, wx.ALL | wx.CENTER, border=10)

        # Plansza
        grid = wx.GridSizer(3, 3, 3, 3)
        self.buttons = [wx.Button(panel, id = i, label = "") for i in range(1, 10)]
        for button in self.buttons:
            grid.Add(button, 0, wx.EXPAND)
        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, border=10)

        # Od nowa 
        self.reset_button = wx.Button(panel, label="Reset Game")
        sizer.Add(self.reset_button, 0, wx.ALL | wx.CENTER, border=10)


    # Zablokuj wprowadzanie drugiego imienia, jeśli grasz z komputerem
    def mode_name_change(self, event):
        mode = self.mode_choice.GetStringSelection()
        if mode == "Play with Computer":
            self.input_player2_name.SetValue("Computer")
            self.input_player2_name.Disable()
        else:
            self.input_player2_name.SetValue("")
            self.input_player2_name.Enable()  
    
    
    def start(self, events):
        mode = self.mode_choice.GetStringSelection()
        player1 = self.input_player1_name.GetValue().strip()
        player2 = self.input_player2_name.GetValue().strip()
        first_player = self.set_out_choice.GetStringSelection()

        if not player1 or (not player2 and mode == "Play with Friend"):
            self.message.SetLabel("Please enter names for both players!")
            return

        self.game.set_players(player1, player2)
        self.game.set_first_player(first_player)

        self.message.SetLabel("%s (X) vs %s (O). %s goes first!" %(player1, player2, first_player))

        for button in self.buttons:
            button.Enable(True)

        # Komputer musi samodzielnie wykonać ruch jeśli wybierzemy go jako pierwszego gracza
        if player2 == "Computer" and first_player == "Second player":
            self.computer_move()


    def grid_click(self, event):
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
            self.message.SetLabel("%s wins!" %winner)
            self.disable_all_buttons()
        elif self.game.is_draw():
            self.message.SetLabel("It's a draw!")
        else:
            self.game.switch_player()
            if self.game.current_player() == "⭕" and self.game.player2 == "Computer":
                self.computer_move()


    def computer_move(self):
        empty_squares = [i for i, square in enumerate(self.game.board) if square is None]
        if empty_squares:
            move = random.choice(empty_squares)
            self.buttons[move].SetLabel("⭕")
            self.game.make_move(move, "⭕")

            winner = self.game.check_winner()
            if winner:
                self.message.SetLabel("%s wins!" %winner)
                self.disable_all_buttons()
            elif self.game.is_draw():
                self.message.SetLabel("It's a draw!")
            else:
                self.game.switch_player()


    def reset_game(self):
        self.game.reset()
        for button in self.buttons:
            button.SetLabel("")
            button.Enable(False)
        self.message.SetLabel("Welcome to Noughts and Crosses!")
        self.input_player1_name.SetValue("")
        self.input_player2_name.SetValue("")
        self.mode_choice.SetSelection(-1)
        self.set_out_choice.SetSelection(-1)


    def reset_click(self, event):
        self.reset_game()


    # Impuls - reakcja i odpowiedź
    def BindEvents(self, buttons):
        self.start_button.Bind(wx.EVT_BUTTON, self.start)  # start button reaguje (bind) na kliknięcie myszką (wx.EVT_BUTTON) i wywołuje funkcję start
        for button in buttons:
            button.Bind(wx.EVT_BUTTON, self.grid_click)
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset_click)


    def disable_all_buttons(self):
        for button in self.buttons:
            button.Enable(False)



class NoughtsAndCrossesLogic:
    def __init__(self):
        self.reset()


    def reset(self):
        self.board = [None] * 9
        self.current_symbol = "✖️"
        self.player1 = None
        self.player2 = None


    def set_players(self, player1, player2):
        self.player1 = player1
        self.player2 = player2


    def set_first_player(self, first_player):
        if first_player == "Second player":
            self.current_symbol = "⭕"
        else:
            self.current_symbol = "✖️"


    def is_square_empty(self, index):
        return self.board[index] is None


    def make_move(self, index, symbol):
        if self.is_square_empty(index):
            self.board[index] = symbol


    def current_player(self):
        return self.current_symbol


    def switch_player(self):
        self.current_symbol = "⭕" if self.current_symbol == "✖️" else "✖️"


    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] and self.board[combo[0]] is not None:
                return self.player1 if self.board[combo[0]] == "✖️" else (self.player2 if self.player2 else "Computer")
        return None


    def is_draw(self):
        return all(square is not None for square in self.board)


if __name__ == "__main__":
    app = wx.App()
    frame = NoughtsAndCrossesApp(None, title = "Noughts and Crosses")
    frame.Show()
    app.MainLoop()
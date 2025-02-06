import wx
import random


# Okienko aplikacji
class NoughtsAndCrossesApp(wx.Frame):
    def __init__(self, parent):
        super().__init__(None, title = "Noughts and Crosses ⭕✖️⭕", size=(700, 700))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        self.Centre()

        # Elementy interfejsu użytkownika
        self.CreateUI_Items(panel, sizer)
        self.game = NoughtsAndCrossesLogic()
        self.BindEvents()
        self.reset_game()
        self.mode_choice.Bind(wx.EVT_CHOICE, self.mode_name_change)


    # Etykiety i pola tekstowe do wprowadzania danych
    def CreateUI_Items(self, panel, sizer):
        # Etykieta powitalna
        self.message = wx.StaticText(panel, label="Welcome to Noughts and Crosses!", style=wx.ALIGN_CENTER)
        self.message.SetMinSize((600, -1))
        self.message.Wrap(600)
        sizer.Add(self.message, 0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=10)
        self.message.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # Wybór trybu gry: gra z przyjacielem/gra z komputerem
        self.mode_label = wx.StaticText(panel, label = "Choose game mode:")
        sizer.Add(self.mode_label, 0, wx.ALL | wx.CENTER, border=5)
        self.mode_choice = wx.Choice(panel, choices = ["Play with Friend", "Play with Computer"])
        sizer.Add(self.mode_choice, 0, wx.ALL | wx.CENTER, border=5)

        # Wprowadzenie imienia pierwszego gracza
        self.player1_label = wx.StaticText(panel, label = "First player name:")
        sizer.Add(self.player1_label, 0, wx.ALL | wx.CENTER, border=5)
        self.input_player1_name = wx.TextCtrl(panel)
        sizer.Add(self.input_player1_name, 0, wx.ALL | wx.CENTER, border=5)

        # Wprowadzenie imienia drugiego gracza
        self.player2_label = wx.StaticText(panel, label = "Second player name:")
        sizer.Add(self.player2_label, 0, wx.ALL | wx.CENTER, border=5)
        self.input_player2_name = wx.TextCtrl(panel)
        sizer.Add(self.input_player2_name, 0, wx.ALL | wx.CENTER, border=5)

        # Wybór pierwszeństwa - kto wykonuje ruch jako pierwszy
        self.set_out_label = wx.StaticText(panel, label = "Who goes first?")
        sizer.Add(self.set_out_label, 0, wx.ALL | wx.CENTER, border=5)
        self.set_out_choice = wx.Choice(panel, choices=["First player", "Second player"])
        sizer.Add(self.set_out_choice, 0, wx.ALL | wx.CENTER, border=5)

        # Przycisk start
        self.start_button = wx.Button(panel, label = "Start Game")
        sizer.Add(self.start_button,  0, wx.ALL | wx.CENTER, border=10)

        # Plansza do gry
        grid = wx.GridSizer(3, 3, 3, 3)
        self.buttons = [wx.Button(panel, id = i, label = "") for i in range(1, 10)]
        for button in self.buttons:
            grid.Add(button, 0, wx.EXPAND)
        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, border=10)

        # Przycisk resetowania gry 
        self.reset_button = wx.Button(panel, label="Reset Game")
        sizer.Add(self.reset_button, 0, wx.ALL | wx.CENTER, border=10)


    # Blokada wprowadzenia drugiego imienia, jeśli wybrano grę z komputerem
    def mode_name_change(self, event):
        mode = self.mode_choice.GetStringSelection()
        if mode == "Play with Computer":
            self.input_player2_name.SetValue("Computer")
            self.input_player2_name.Disable()
        else:
            self.input_player2_name.SetValue("")
            self.input_player2_name.Enable()  
    
    
    # Uruchamianie gry
    def start(self, event):
        mode = self.mode_choice.GetStringSelection()
        player1 = self.input_player1_name.GetValue().strip()
        player2 = self.input_player2_name.GetValue().strip()
        first_player = self.set_out_choice.GetStringSelection()

        if not player1 or (not player2 and mode == "Play with Friend"):
            self.message.SetLabel("Please enter names for both players!")
            return
        
        if self.mode_choice.GetSelection() == wx.NOT_FOUND:
            self.message.SetLabel("Please select a game mode!")
            return
        
        if self.set_out_choice.GetSelection() == wx.NOT_FOUND:
            self.message.SetLabel("Please choose who goes first!")
            return

        self.game.set_players(player1, player2)
        self.game.set_first_player(first_player)

        self.message.SetLabel("%s (X) vs %s (O). %s goes first!" %(player1, player2, first_player))

        # Wyłączenie pól tekstowych po kliknięciu start
        self.input_player1_name.Disable()
        self.input_player2_name.Disable()
        self.mode_choice.Disable()
        self.set_out_choice.Disable()
        self.start_button.Disable()

        for button in self.buttons:
            button.Enable(True)

        # Komputer musi samodzielnie wykonać ruch, jeśli wybierzemy go jako pierwszego gracza
        if player2 == "Computer" and first_player == "Second player":
            self.computer_move()


    # Obsługa kliknięć na planszy
    def grid_click(self, event):
        button_id = event.GetId()
        button = self.FindWindowById(button_id)
        index = self.buttons.index(button)

        if not self.game.empty_square(index):
            return

        symbol = self.game.current_player()
        button.SetLabel(symbol)  # Ustawienie symbolu, jeśli wybrano przycisk
        button.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # Kolorowanie przycisku zależnie od symbolu
        if symbol == "X":
            button.SetBackgroundColour(wx.Colour(216, 191, 216)) 
        else:
            button.SetBackgroundColour(wx.Colour(255, 192, 203))

        self.game.make_move(index, symbol)

        # Sprawdzenie, czy jest zwycięzca
        winner = self.game.check_winner()
        if winner:
            self.message.SetLabel("%s wins!" %winner)
            self.disable_all_buttons()
        elif self.game.is_draw():
            self.message.SetLabel("It's a draw!")
            self.disable_all_buttons()
        else:
            self.game.switch_player() # Zmiana gracza
            if self.game.current_player() == "O" and self.game.player2 == "Computer":
                self.computer_move()


    # Obsługa ruchów komputera
    def computer_move(self):
        empty_squares = []
        for i in range(9):
            if self.game.board[i] is None:
                empty_squares.append(i)
        if empty_squares:
            move = random.choice(empty_squares)  # Komputer losuje swój ruch/krok
            self.buttons[move].SetLabel("O")
            self.buttons[move].SetBackgroundColour(wx.Colour(255, 192, 203))
            self.buttons[move].SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.game.make_move(move, "O")

            # Sprawdzenie, czy jest zwycięzca
            winner = self.game.check_winner()
            if winner:
                self.message.SetLabel("%s wins!" %winner)
                self.disable_all_buttons()
            elif self.game.is_draw():
                self.message.SetLabel("It's a draw!")
                self.disable_all_buttons()
            else:
                self.game.switch_player()


    # Resetowanie gry
    def reset_game(self):
        self.game.reset()
        for button in self.buttons:
            button.SetLabel("") # Resetowanie etykiet
            button.SetBackgroundColour(wx.Colour(255, 255, 255)) # Resetowanie koloru
            button.Disable() # Wyłączanie przycisków
        self.message.SetLabel("Welcome to Noughts and Crosses!")
        # Przywrócenie pól tekstowych i opcji do stanu początkowego
        self.input_player1_name.Enable(True)
        self.input_player2_name.Enable(True)
        self.mode_choice.Enable(True)
        self.set_out_choice.Enable(True)
        self.start_button.Enable(True)
        self.input_player1_name.SetValue("")
        self.input_player2_name.SetValue("")
        self.mode_choice.SetSelection(-1)
        self.set_out_choice.SetSelection(-1)


    # Reset gry po naciśnięciu przycisku
    def reset_click(self, event):
        self.reset_game()


    # Powiązanie zdarzeń z odpowiednimi funkcjami
    def BindEvents(self):
        self.start_button.Bind(wx.EVT_BUTTON, self.start)
        for button in self.buttons:
            button.Bind(wx.EVT_BUTTON, self.grid_click)
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset_click)


    # Funkcja do wyłączenia wszystkich przycisków na planszy
    def disable_all_buttons(self):
        for button in self.buttons:
            button.Disable()


# Logika gry
class NoughtsAndCrossesLogic:
    def __init__(self):
        self.reset()


    def reset(self):
        self.board = [None] * 9     # Pusta plansza
        self.player1 = None
        self.player2 = None


    # Ustawienie graczy
    def set_players(self, player1, player2):
        self.player1 = player1
        self.player2 = player2


    # Ustawienie pierwszego gracza
    def set_first_player(self, first_player):
        if first_player == "Second player":
            self.current_symbol = "O"
        else:
            self.current_symbol = "X"


    # Sprawdzenie czy pole jest puste
    def empty_square(self, index):
        return self.board[index] is None


    # Wykonanie ruchu
    def make_move(self, index, symbol):
        if self.empty_square(index):
            self.board[index] = symbol


    # Aktualny gracz
    def current_player(self):
        return self.current_symbol


    # Zmiana gracza
    def switch_player(self):
        self.current_symbol = "O" if self.current_symbol == "X" else "X"


    # Sprawdzenie, czy i kto jest zwycięzcą
    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # wiersze
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # kolumny
            [0, 4, 8], [2, 4, 6]              # przekątne
        ]
        for combination in winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] and self.board[combination[0]] is not None:
                winner_symbol = self.board[combination[0]]
                if winner_symbol == "X":
                    return self.player1
                elif winner_symbol == "O":
                    return self.player2
        return None


    # Sprawdzamy, czy wszystkie pola na planszy są już zajęte/czy jest remis
    def is_draw(self):
        for square in self.board:
            if square is None:
                return False  
        return True


if __name__ == "__main__":
    app = wx.App()
    frame = NoughtsAndCrossesApp(None)
    frame.Show()
    app.MainLoop()    
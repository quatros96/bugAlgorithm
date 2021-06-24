import tkinter as tk
import typing as type
from tkinter import filedialog, messagebox
from bugZero import BugZero


class MyGui:

    def __init__(self) -> None:
        self.__bugAlgorithm = BugZero()
        self.__window = tk.Tk()
        self.__canvas: tk.Canvas
        self.__fileSelectButton: tk.Button
        self.__startButton: tk.Button
        self.__endButton: tk.Button
        self.__nextButton: tk.Button
        self.__prevButton: tk.Button
        self.__runButton: tk.Button
        self.__directionLeftCheck: tk.Checkbutton
        self.__directionRightCheck: tk.Checkbutton
        self.__directionLeftCheckState: int = 0
        self.__directionRightCheckState: int = 0
        self.__filePath: str = ''

        self.__noMoves: int = 0
        self._robotMoves: type.List[type.Dict[str, int]] = []
        # calling methods
        self.__configWindow()
        self.__configFileSelectButton()
        self.__configCanvas()
        self.__configNavButtons()
        self.__configRunButton()
        self.__configDirectionButtons()
        self.__window.mainloop()

    def __configWindow(self):
        self.__window.title("Algorytm pluskwy - Mateusz Kozlowski")
        self.__window.wm_attributes("-transparentcolor")
        self.__window.geometry("1000x800")
        self.__window.resizable(False, False)

    def __configFileSelectButton(self):
        self.__fileSelectButton = tk.Button(
            self.__window, text="Wybierz mape", command=self.__fileSelecButtonOnClick, bg="white",  fg="black")
        self.__fileSelectButton.config(height=3, width=14)
        self.__fileSelectButton.grid(column=2, row=0, columnspan=2)

    def __fileSelecButtonOnClick(self):
        self.__filePath = filedialog.askopenfilename(
            title="Wybierz mape do algorytmu", filetypes=[("plik TXT", "*.txt")])

        loadError = self.__bugAlgorithm.loadMapFromFile(self.__filePath)

        if loadError is None:
            print("sukces")
            self.__drawMap()
            self.__runButton['state'] = 'normal'
        else:
            messagebox.showerror("ERROR!", loadError)

    def __configNavButtons(self):
        self.__startButton = tk.Button(
            self.__window, text="|<<", command=self.__startButtonOnClick, bg="white",  fg="black")
        self.__startButton.config(height=3, width=3)
        self.__startButton.grid(column=1, row=1)
        self.__startButton['state'] = "disabled"

        self.__endButton = tk.Button(
            self.__window, text=">>|", command=self.__endButtonOnClick, bg="white",  fg="black")
        self.__endButton.config(height=3, width=3)
        self.__endButton.grid(column=4, row=1)
        self.__endButton['state'] = "disabled"

        self.__prevButton = tk.Button(
            self.__window, text="<-", command=self.__prevButtonOnClick, bg="white",  fg="black")
        self.__prevButton.config(height=3, width=3)
        self.__prevButton.grid(column=2, row=1)
        self.__prevButton['state'] = "disabled"

        self.__nextButton = tk.Button(
            self.__window, text="->", command=self.__nextButtonOnClick, bg="white",  fg="black")
        self.__nextButton.config(height=3, width=3)
        self.__nextButton.grid(column=3, row=1)
        self.__nextButton['state'] = "disabled"

    def __prevButtonOnClick(self):
        self.__noMoves -= 1
        if self.__noMoves < 0:
            self.__noMoves = 0
        self.__drawMap(self._robotMoves)

    def __nextButtonOnClick(self):
        self.__noMoves += 1
        if self.__noMoves > len(self._robotMoves):
            self.__noMoves = len(self._robotMoves)
        self.__drawMap(self._robotMoves)

    def __startButtonOnClick(self):
        self.__noMoves = 0
        self.__drawMap(self._robotMoves)

    def __endButtonOnClick(self):
        self.__noMoves = len(self._robotMoves)
        self.__drawMap(self._robotMoves)

    def __configRunButton(self):
        self.__runButton = tk.Button(
            self.__window, text="Uruchom", command=self.__runButtonOnClick, bg="#98D597",  fg="black")
        self.__runButton.config(height=4, width=15)
        self.__runButton.grid(column=2, row=3, columnspan=2)
        self.__runButton['state'] = "disabled"

    def __runButtonOnClick(self):
        self._robotMoves = self.__bugAlgorithm.findRoute()
        self.__noMoves = len(self._robotMoves)
        self.__drawMap(self._robotMoves)
        self.__startButton['state'] = "normal"
        self.__endButton['state'] = "normal"
        self.__prevButton['state'] = "normal"
        self.__nextButton['state'] = "normal"

    def __configDirectionButtons(self):
        self.__directionLeftCheck = tk.Checkbutton(
            self.__window, text="Do lewej", command=self.__leftOnClicked, variable=self.__directionLeftCheckState)
        self.__directionLeftCheck.grid(column=2, row=4, columnspan=2)
        self.__directionLeftCheck.select()

        self.__directionRightCheck = tk.Checkbutton(
            self.__window, text="Do prawej", command=self.__rightOnClicked, variable=self.__directionRightCheckState)
        self.__directionRightCheck.grid(column=2, row=5, columnspan=2)

    def __leftOnClicked(self):
        if self.__directionLeftCheckState == 1:
            self.__bugAlgorithm.changeDirection('left')
            self.__directionRightCheck.deselect()
            print('left')
        else:
            self.__bugAlgorithm.changeDirection('right')
            self.__directionRightCheck.select()
            print('right')

    def __rightOnClicked(self):
        if self.__directionRightCheckState == 1:
            self.__bugAlgorithm.changeDirection('right')
            self.__directionLeftCheck.deselect()
            print('right')
        else:
            self.__bugAlgorithm.changeDirection('left')
            self.__directionLeftCheck.select()
            print('left')

    def __configCanvas(self):
        self.__canvas = tk.Canvas(
            self.__window, bg="white", width=750, height=750)
        self.__canvas.grid(column=0, row=0, padx=25, pady=25, rowspan=6)

    def __drawMap(self, robotMoves=None):
        self.__canvas.delete("all")
        map = self.__bugAlgorithm.getMap()
        # raczej chce kwadratowe
        y = len(map)
        x = len(map[0])

        boxWidth = 750 / x
        boxHeight = 750 / y
        boxSize: float
        if boxWidth < boxHeight:
            boxSize = boxWidth
        else:
            boxSize = boxHeight

        for ypos, fields in enumerate(map):
            for xpos, field in enumerate(fields):
                if field == 0:
                    self.__canvas.create_rectangle(
                        boxSize * xpos, boxSize * ypos, boxSize*xpos + boxSize, boxSize * ypos + boxSize, fill="#cfcfcf")
                elif field == 1:
                    self.__canvas.create_rectangle(
                        boxSize * xpos, boxSize * ypos, boxSize*xpos + boxSize, boxSize * ypos + boxSize, fill="#000000")
                elif field == 2:
                    self.__canvas.create_rectangle(
                        boxSize * xpos, boxSize * ypos, boxSize*xpos + boxSize, boxSize * ypos + boxSize, fill="#ff0000")
                    self.__canvas.create_text(
                        boxSize*xpos + boxSize / 2, boxSize * ypos + boxSize / 2, text="ROBOT")
                elif field == 3:
                    self.__canvas.create_rectangle(
                        boxSize * xpos, boxSize * ypos, boxSize*xpos + boxSize, boxSize * ypos + boxSize, fill="#FFD700")
                    self.__canvas.create_text(
                        boxSize*xpos + boxSize / 2, boxSize * ypos + boxSize / 2, text="TARGET")
        if robotMoves != None:
            for number, move in enumerate(robotMoves[0:self.__noMoves]):
                self.__canvas.create_rectangle(
                    boxSize * move['x'], boxSize * move['y'], boxSize*move['x'] + boxSize, boxSize * move['y'] + boxSize, fill="#EC6565")
                self.__canvas.create_text(
                    boxSize*move['x'] + boxSize / 2, boxSize * move['y'] + boxSize / 2, text=number)


test = MyGui()

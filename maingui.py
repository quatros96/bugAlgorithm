import tkinter as tk
from tkinter import filedialog, messagebox
from bugZero import BugZero


class MyGui:

    def __init__(self) -> None:
        self.__bugAlgorithm = BugZero()
        self.__window = tk.Tk()
        self.__canvas: tk.Canvas
        self.__fileSelectButton: tk.Button
        self.__filePath: str = ''
        self.__configWindow()
        self.__configFileSelectButton()
        self.__configCanvas()
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
        self.__fileSelectButton.grid(column=1, row=0)

    def __fileSelecButtonOnClick(self):
        self.__filePath = filedialog.askopenfilename(
            title="Wybierz mape do algorytmu", filetypes=[("plik TXT", "*.txt")])

        loadError = self.__bugAlgorithm.loadMapFromFile(self.__filePath)

        if loadError is None:
            print("sukces")
            self.__drawMap()
        else:
            messagebox.showerror("ERROR!", loadError)

    def __configCanvas(self):
        self.__canvas = tk.Canvas(
            self.__window, bg="white", width=750, height=750)
        self.__canvas.grid(column=0, row=0, padx=25, pady=25)

    def __drawMap(self):
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


test = MyGui()

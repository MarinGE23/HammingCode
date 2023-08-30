import tkinter as tk
from tkinter import messagebox
import hamming_code
import converter

class App:
    def __init__(self, master):
        # Window configuration
        master.title("Hamming Code App")
        master.geometry("1200x700")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        master.resizable(False, False) 
        self.data_with_parity = []

        # Scroll
        self.canvasScroll = tk.Canvas(master, bg="#EAECFA")
        self.canvasScroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollBar = tk.Scrollbar(master, command=self.canvasScroll.yview)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvasScroll.config(yscrollcommand=self.scrollBar.set)

        # Sections
        self.mainFrame = tk.Frame(self.canvasScroll, bg="#EAECFA")

        self.basesFrame = tk.Frame(self.mainFrame, bg="#EAECFA")
        self.basesFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.table1 = tk.Frame(self.mainFrame, bg="#EAECFA")
        self.table1.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.parityFrame = tk.Frame(self.mainFrame, bg="#EAECFA")
        self.parityFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.table2 = tk.Frame(self.mainFrame, bg="#EAECFA")
        self.table2.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.errorFrame = tk.Frame(self.mainFrame, bg="#EAECFA")
        self.errorFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.signalFrame = tk.Frame(self.mainFrame, bg="#EAECFA")
        self.signalFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.canvasScroll.create_window((0, 0), window=self.mainFrame, anchor="nw")
        self.mainFrame.bind(
            "<Configure>",
            lambda e: self.canvasScroll.configure(
                scrollregion=self.canvasScroll.bbox("all")
            ),
        )
        self.mainFrame.bind_all(
            "<MouseWheel>",
            lambda e: self.canvasScroll.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            ),
        )

        # Labels
        self.label1 = tk.Label(
            self.basesFrame,
            height=2,
            text="Dato Hexadecimal:",
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
        ).grid(row=1, column=0, padx=5, sticky=tk.W)

        self.label1 = tk.Label(
            self.basesFrame,
            text="Paridad: ",
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
        ).grid(row=1, column=3, padx=5, sticky=tk.W)

        self.label_table1 = tk.Label(
            self.table1,
            text="Tabla No.1",
            bg="#EAECFA",
            fg="#2F5597",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, sticky=tk.W)

        self.label_table2 = tk.Label(
            self.table2,
            text="Tabla No.2",
            bg="#EAECFA",
            fg="#2F5597",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, sticky=tk.W)

        self.label_signalFrame = tk.Label(
            self.signalFrame,
            text="Señal NRZI",
            bg="#EAECFA",
            fg="#2F5597",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, sticky=tk.W)

        # Entry
        entry = tk.Entry(self.basesFrame, width=14, bg="white", fg="black", font=("Arial", 11))
        entry.grid(row=1, column=1, sticky=tk.W)

        # Conversion table
        self.update_conversion_table(["-", "-", "-", "-"])

        # Hamming parity table
        parity_titles = [
            "Hamming",
            "Dato (sin paridad)",
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "Dato (con paridad)",
        ]

        for m in range(8):
            self.cell = tk.Label(
                self.parityFrame,
                height=2,
                width=15,
                bg="#EAECFA",
                fg="black",
                font=("Arial", 11),
                bd=1,
                relief=tk.SOLID,
            )
            self.cell.grid(row=m, column=0, sticky=tk.W)
            self.cell.config(text=parity_titles[m])

        p = 1
        d = 1
        for n in range(1, 18):
            self.cell = tk.Label(
                self.parityFrame,
                height=2,
                width=5,
                bg="#EAECFA",
                fg="black",
                font=("Arial", 11),
                bd=1,
                relief=tk.SOLID,
            )
            self.cell.grid(row=0, column=n)
            if (n != 0) and (n & (n - 1) == 0):
                self.cell.config(text="p" + str(p))
                p += 1
            else:
                self.cell.config(text="d" + str(d))
                d += 1

        for i in range(1, 8):
            for j in range(1, 18):
                self.cell = tk.Label(
                    self.parityFrame,
                    height=2,
                    width=5,
                    bg="#EAECFA",
                    fg="black",
                    font=("Arial", 11),
                    bd=1,
                    relief=tk.SOLID,
                    text="",
                )
                self.cell.grid(row=i, column=j)
                if (j != 0) and (j & (j - 1) == 0):
                    self.cell.configure(fg="black")

        # Update-button function
        def update_button():
            input = entry.get()
            if converter.is_hex(input) and len(input) == 3:
                results = converter.hex_to_all(input)
                self.update_conversion_table(
                    [input, results[0], results[1], results[2]]
                )
                self.update_parity_table(converter.str_to_list(results[0]))
                self.draw_signal(results[0])
            else:
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un número hexadecimal de 3 dígitos \n (De 000 a FFF)",
                )

        self.update = tk.Button(
            self.basesFrame,
            text="PROCESAR",
            bg="#EAECFA",
            fg="#2F5597",
            font=("Arial", 11, "bold"),
            command=update_button,
        )
        self.update.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

        # Parity option
        self.parityOptions = ["Par", "Impar"]
        self.parityVar = tk.StringVar()
        self.parityVar.set(self.parityOptions[0])
        self.parity = tk.OptionMenu(
            self.basesFrame, self.parityVar, *self.parityOptions,
        )
        self.parity.grid(row=1, column=4, sticky=tk.W)
        self.parity.config(
            bg="#EAECFA", fg="#2F5597", font=("Arial", 11, "bold"),
        )

        # Hamming error table
        error_titles = [
            "Detección de error",
            "Dato recibido",
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
        ]

        for m in range(7):
            self.cell = tk.Label(
                self.errorFrame,
                height=2,
                width=15,
                bg="#EAECFA",
                fg="black",
                font=("Arial", 11),
                bd=1,
                relief=tk.SOLID,
            )
            self.cell.grid(row=m, column=0, sticky=tk.W)
            self.cell.config(text=error_titles[m])
    
        p = 1
        d = 1
        for n in range(1, 18):
            self.cell = tk.Label(
                self.errorFrame,
                height=2,
                width=5,
                bg="#EAECFA",
                fg="black",
                font=("Arial", 11),
                bd=1,
                relief=tk.SOLID,
            )
            self.cell.grid(row=0, column=n)
            if (n != 0) and (n & (n - 1) == 0):
                self.cell.config(text="p" + str(p))
                p += 1
            else:
                self.cell.config(text="d" + str(d))
                d += 1
        
        self.cellParity = tk.Label(
            self.errorFrame,
            height=2,
            width=8,
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
            bd=1,
            relief=tk.SOLID,
            text="Prueba de\nparidad",
        )
        self.cellParity.grid(row=0, column=18)

        self.cellParity_1 = tk.Label(
            self.errorFrame,
            height=2,
            width=8,
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
            bd=1,
            relief=tk.SOLID,
            text="",
        )
        self.cellParity_1.grid(row=1, column=18)

        self.cellParity2 = tk.Label(
            self.errorFrame,
            height=2,
            width=8,
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
            bd=1,
            relief=tk.SOLID,
            text="Bit de\nparidad",
        )
        self.cellParity2.grid(row=0, column=19)

        self.cellParity_2 = tk.Label(
            self.errorFrame,
            height=2,
            width=8,
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
            bd=1,
            relief=tk.SOLID,
            text="",
        )
        self.cellParity_2.grid(row=1, column=19)

        for i in range(2, 7):
            for j in range(1, 20):
                self.cell = tk.Label(
                    self.errorFrame,
                    height=2,
                    width=5,
                    bg="#EAECFA",
                    fg="black",
                    font=("Arial", 11),
                    bd=1,
                    relief=tk.SOLID,
                    text="",
                )
                self.cell.grid(row=i, column=j)
                if (j != 0) and (j & (j - 1) == 0):
                    self.cell.configure(fg="black")
                if (j == 18) or (j == 19):
                    self.cell.config(width=8)

        for j in range(1, 18):
            self.cell = tk.Button(
                self.errorFrame,
                height=1,
                width=4,
                bg="#EAECFA",
                fg="black",
                font=("Arial", 11),
                bd=1,
                relief=tk.SOLID,
                text="",
                command=lambda j=j: self.update_error_table(j - 1),
                state=tk.DISABLED,
            )
            self.cell.grid(row=1, column=j)
            if (j != 0) and (j & (j - 1) == 0):
                self.cell.configure(fg="black")

        self.errorPosition = tk.Label(
            self.errorFrame,
            height=2,
            width=8,
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
            text="Error: ",
        )
        self.errorPosition.grid(row=7, column=0)

        self.binaryPosition = tk.Label(
            self.errorFrame,
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
            text="",
        )
        self.binaryPosition.grid(row=7, column=1)

        self.decimalPosition = tk.Label(
            self.errorFrame,
            bg="#EAECFA",
            fg="black",
            font=("Arial", 11),
            text="",
        )
        self.decimalPosition.grid(row=7, column=2)

    # Function that draws the X and Y axes of the unipolar signal with a previous low state
    def draw_signal(self, bin_data):
        # Canvas definition
        self.canvas = tk.Canvas(self.signalFrame, width=955, height=370, bg="white")
        self.canvas.grid(row=1, column=4, sticky=tk.W)

        # X axis
        self.canvas.create_line(120, 200, 830, 200, fill="black", width=1.5)
        self.canvas.create_text(815, 210, fill="black", font="Times 12 bold", text="Tiempo")

        # Y axis
        self.canvas.create_line(130, 310, 130, 80, fill="black", width=1.5)
        self.canvas.create_text(127, 65, fill="black", font="Times 12 bold", text="Amplitud")

        # Initial state of the signal
        self.canvas.create_line(130, 150, 180, 150, fill="red", width=3.0)
        self.canvas.create_line(180, 270, 180, 130, dash=(4, 2), fill="black")
        self.canvas.create_text(155, 120, fill="black", font="Times 10 bold", text="1")
        self.x = 180
        self.y = 150

        self.draw_signal_aux(bin_data)

    # Function that draws the rest of the signal according to the binary data coming from the 
    # entered hexadecimal number
    def draw_signal_aux(self, bin_data):
        if bin_data != "":
            # Input data 0
            if bin_data[0] == "0":
                self.canvas.create_line(self.x, self.y, self.x + 50, self.y, fill="red", width=3.0)
                self.x = self.x + 50

                self.canvas.create_line(self.x, 270, self.x, 130, dash=(4, 2), fill="black")
                self.canvas.create_text(self.x - 25, 120, fill="black", font="Times 10 bold", text="0")

                self.draw_signal_aux(bin_data[1:])

            # Input data 1 and previous state low
            elif bin_data[0] == "1" and self.y == 250:
                self.canvas.create_line(self.x, self.y, self.x, self.y - 100, fill="red", width=3.0)
                self.y = self.y - 100

                self.canvas.create_line(self.x, self.y, self.x + 50, self.y, fill="red", width=3.0)
                self.x = self.x + 50
                self.canvas.create_line(self.x, 270, self.x, 130, dash=(4, 2), fill="black")
                self.canvas.create_text(self.x - 25, 120, fill="black", font="Times 10 bold", text="1")

                self.draw_signal_aux(bin_data[1:])

            # Input data 1 and previous high state
            elif bin_data[0] == "1" and self.y == 150:
                self.canvas.create_line(self.x, self.y, self.x, self.y + 100, fill="red", width=3.0)
                self.y = self.y + 100

                self.canvas.create_line(self.x, self.y, self.x + 50, self.y, fill="red", width=3.0)
                self.x = self.x + 50
                self.canvas.create_line(self.x, 270, self.x, 130, dash=(4, 2), fill="black")
                self.canvas.create_text(self.x - 25, 120, fill="black", font="Times 10 bold", text="1")

                self.draw_signal_aux(bin_data[1:])

    # Update the parity table with the 12-bit list entered
    def update_parity_table(self, data):
        extended_data = hamming_code.add_places(data)
        matrix = hamming_code.get_parity_table(extended_data, self.parityVar.get())
        self.data_with_parity = hamming_code.final_message(matrix)
        table = []
        table.append(extended_data)
        for row in matrix:
            table.append(row)
        table.append(self.data_with_parity)

        for i in range(len(table)):
            for j in range(len(table[i])):
                if table[i][j] != -1:
                    self.parityFrame.grid_slaves(i + 1, j + 1)[0].config(
                        text=str(table[i][j])
                    )
                else:
                    self.parityFrame.grid_slaves(i + 1, j + 1)[0].config(text="")

        # Error
        for j in range(len(self.data_with_parity)):
            self.errorFrame.grid_slaves(1, j + 1)[0].config(
                text=str(self.data_with_parity[j]), state=tk.NORMAL,
            )
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != -1:
                    self.errorFrame.grid_slaves(i + 2, j + 1)[0].config(
                        text=str(matrix[i][j])
                    )
                else:
                    self.errorFrame.grid_slaves(i + 2, j + 1)[0].config(text="")
        for j in range(5):
            self.errorFrame.grid_slaves(j + 2, 18)[0].config(text="Correcto", fg="green")
            self.errorFrame.grid_slaves(j + 2, 19)[0].config(text="0")
        self.errorFrame.grid_slaves(7, 1)[0].config(text="")
        self.errorFrame.grid_slaves(7, 2)[0].config(text="")

    # Change the selected bit and execute the hamming error search
    def update_error_table(self, position):
        if self.data_with_parity[position] == 1:
            self.data_with_parity[position] = 0
        else:
            self.data_with_parity[position] = 1

        for j in range(6):
            if self.errorFrame.grid_slaves(j + 1, position + 1)[0]["text"] != "":
                self.errorFrame.grid_slaves(j + 1, position + 1)[0].config(
                    text=str(self.data_with_parity[position])
                )

        for j in range(len(self.data_with_parity)):
            self.errorFrame.grid_slaves(1, j + 1)[0].config(state=tk.DISABLED)

        results = hamming_code.compare(self.data_with_parity, self.parityVar.get())

        for i in range(5):
            self.errorFrame.grid_slaves(i + 2, 18)[0].config(text=results[0][i])
            if results[0][i] == "Error":
                self.errorFrame.grid_slaves(i + 2, 18)[0].config(fg="red")
            self.errorFrame.grid_slaves(i + 2, 19)[0].config(text=str(results[1][i]))
        errorPos = ""
        for i in range(5):
            errorPos = self.errorFrame.grid_slaves(i + 2, 19)[0]["text"] + errorPos
        self.errorFrame.grid_slaves(7, 1)[0].config(text=errorPos)
        decimalPos = hamming_code.position_of_error(list(errorPos))
        self.errorFrame.grid_slaves(7, 2)[0].config(text=str(decimalPos))

    def update_conversion_table(self, data):
        conversion_titles = [
            "Hexadecimal",
            "Binario",
            "Octal",
            "Decimal",
        ]

        for m in range(4):
            self.cell = tk.Label(
                self.basesFrame,
                height=2,
                width=15,
                bg="#EAECFA",
                fg="black",
                font=("Arial", 11),
                bd=1,
                relief=tk.SOLID,
            )
            self.cell.grid(row=m + 3, column=0, sticky=tk.W)
            self.cell.config(text=conversion_titles[m])

        for i in range(0, 4):
            for j in range(1, 2):
                self.cell = tk.Label(
                    self.basesFrame,
                    height=2,
                    width=15,
                    bg="#EAECFA",
                    fg="black",
                    font=("Arial", 11),
                    bd=1,
                    relief=tk.SOLID,
                    text=data[i],
                )
                self.cell.grid(row=i + 3, column=j)
                if (j != 0) and (j & (j - 1) == 0):
                    self.cell.configure(fg="black")

    def on_closing(self):
        root.destroy()


# Initialize the application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
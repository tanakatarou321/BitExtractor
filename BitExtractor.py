import csv
import sys

import tkinter as tk
from tkinter import ttk, filedialog


class main:
    def __init__(self):
        self.padx = 10
        self.pady = 10
        self.posx = [0, 40, 100, 120, 140]
        self.posy = 100

        self.app = tk.Tk()
        self.app.title("BitExtractor")
        self.app.geometry("500x500")
        self.app.minsize(500, 200)
        self.frame = tk.Frame(self.app, width=500, height=500)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.btn_run = tk.Button(self.frame, command=self._calc, text="Run", cursor="arrow")
        self.btn_add = tk.Button(self.frame, command=self._add_entry, text="Add")
        self.btn_read = tk.Button(self.frame, command=self._read_param, text="Read")
        self.btn_write = tk.Button(self.frame, command=self._write_param, text="Write")

        self.btn_run.place(x=self.padx, y=self.pady)
        self.btn_add.place(x=self.padx + 50, y=self.pady)
        self.btn_read.place(x=self.padx + 100, y=self.pady)
        self.btn_write.place(x=self.padx + 150, y=self.pady)

        self.app.bind("<Return>", self._calc)
        self.app.bind("<Control-a>", self._add_entry)

        tk.Label(self.frame, text="Input:").place(x=self.padx, y=self.pady + 50)
        self.input = tk.Entry(self.frame, width=50)
        self.input.place(x=self.padx + 40, y=self.pady + 50)

        tk.Label(self.frame, text="Label").place(x=self.padx + self.posx[1], y=self.pady + 80)
        tk.Label(self.frame, text="[b :").place(x=self.padx + self.posx[2], y=self.pady + 80)
        tk.Label(self.frame, text="e]").place(x=self.padx + self.posx[3], y=self.pady + 80)
        tk.Label(self.frame, text="out").place(x=self.padx + self.posx[4], y=self.pady + 80)

        self.radix = []
        self.name = []
        self.b = []
        self.e = []
        self.output = []
        self.btn = []

        self._add_entry()

    def _add_entry(self, e=None):
        self.radix.append(ttk.Combobox(self.frame, values=["bin", "hex", "dec"], width=3))
        self.name.append(tk.Entry(self.frame))
        self.b.append(tk.Entry(self.frame, width=10))
        self.e.append(tk.Entry(self.frame, width=10))
        self.output.append(tk.Entry(self.frame, state="readonly", width=50))

        self.radix[-1].place(x=self.padx + self.posx[0], y=self.pady + self.posy)
        self.name[-1].place(x=self.padx + self.posx[1], y=self.pady + self.posy)
        self.b[-1].place(x=self.padx + self.posx[2], y=self.pady + self.posy)
        self.e[-1].place(x=self.padx + self.posx[3], y=self.pady + self.posy)
        self.output[-1].place(x=self.padx + self.posx[4], y=self.pady + self.posy)

        self.posy += 25

    def _calc(self, e=None):
        for (r, b, e, o) in zip(self.radix, self.b, self.e, self.output):
            # When not to be set [b:e]
            if b.get() == "" or e.get() == "":
                continue

            # Get [b:e]
            b = int(b.get())
            e = int(e.get())
            if b < e:
                continue

            # Extract bit from input
            tmp = bin(int(self.input.get(), 16))[2:][::-1][e:b+1][::-1]
            if r.get() == "hex":
                tmp = hex(int(tmp, 2))
            elif r.get() == "dec":
                tmp = int(tmp, 2)

            o.config(state="normal")
            o.delete(0, tk.END)
            o.insert(0, str(tmp))
            o.config(state="readonly")

    def _write_param(self, e=None):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=(("", "*.csv"),))
        if filename:
            with open(filename, "w") as f:
                f.write("radix,name,b,e,output\n")
                for (r, n, b, e, o) in zip(self.radix, self.name, self.b, self.e, self.output):
                    f.write("{0},{1},{2},{3},{4}\n".format(
                        r.get(), n.get(), b.get(), e.get(), o.get()))

    def _read_param(self, e=None):
        filename = filedialog.askopenfilename(filetypes=(("", "*.csv"),))
        if filename:
            self._set_param(filename)

    def _set_param(self, filename):
        with open(filename) as f:
            for i, param in enumerate(csv.DictReader(f)):
                if len(self.radix) <= i:
                    self._add_entry()

                self.radix[i].set(param["radix"])
                self.name[i].delete(0, tk.END)
                self.name[i].insert(0, param["name"])
                self.b[i].delete(0, tk.END)
                self.b[i].insert(0, param["b"])
                self.e[i].delete(0, tk.END)
                self.e[i].insert(0, param["e"])

    def start(self, filename=""):
        # When input file exists.
        if filename != "":
            self._set_param(filename)
        self.app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        input_file = ""
    else:
        input_file = sys.argv[1]

    a = main()
    a.start(input_file)
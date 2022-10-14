import tkinter as tk


class NumEntry(tk.Entry):
    """A Entry widget that only accepts digits"""

    def __init__(self, master=None, **kwargs):
        self.var = tk.StringVar(master)
        self.var.trace('w', self.validate)
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.get, self.set = self.var.get, self.var.set

    def validate(self, *args):
        value = self.get()
        if not value.isdigit():
            self.set(''.join(x for x in value if x.isdigit()))

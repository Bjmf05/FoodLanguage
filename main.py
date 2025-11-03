import tkinter as tk
from ide_window import FoodLanguageIDE


def main():
    """Función principal para iniciar el IDE"""
    root = tk.Tk()
    app = FoodLanguageIDE(root)
    root.mainloop()


if __name__ == '__main__':
    main()

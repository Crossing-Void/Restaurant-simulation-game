from Tkinter_template.Assets.project_management import new_window, making_widget
from Tkinter_template.Assets.font import font_get, check_font, set_font


def check_font_ready():
    # if font exists return True else into download and exit
    def download():
        win.destroy()
        set_font()

    if not check_font():
        win = new_window("Install Font", "favicon.ico", (800, 200))
        making_widget("Label")(win, text="Install Font \"Inconsolata\"",
                               font=font_get(30, True)).pack(pady=10)
        making_widget("Label")(
            win, text="Because your computer does not have the required font for this game\nPress \"Download\" to begin the download",
            font=font_get(20)).pack(pady=5)
        making_widget("Button")(win, text="Download",
                                font=font_get(26), bg="#ffff80", command=download).pack(side="bottom", pady=10)
        win.attributes('-topmost', 1)
        win.wait_window()

        return False
    return True

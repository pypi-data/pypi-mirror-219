from tkadw.windows.theme import AdwTFrame, AdwTButton


class AdwMDI(AdwTFrame):

    """
    多文档窗口
    """

    def create_child(self):
        """
        创建一个子窗口

        :return: AdwTFrame
        """
        child = AdwTFrame(self.frame)
        child.place(x=10, y=10, width=150, height=150)

        child.titlebar = AdwTFrame(child.frame, height=38)
        child.titlebar.frame_border_width = 0
        child.titlebar.frame_border = child.frame_back
        child.closebutton = AdwTButton(child.titlebar.frame, text="✕", width=25, height=25, command=lambda: child.place_forget())
        child.closebutton.pack(anchor="ne", padx=2, pady=2)
        child.titlebar.pack(fill="x", side="top", padx=2, pady=2)

        child.titlebar.frame.bind("<Button-1>", self._click)
        child.titlebar.frame.bind("<B1-Motion>", lambda event: self._move(event, child))

        return child

    def _click(self, event):
        self.x, self.y = event.x, event.y

    def _move(self, event, child):
        child.place(
            x=(event.x-self.x)+child.winfo_x(),
            y=(event.y-self.y)+child.winfo_y()
        )


if __name__ == '__main__':
    from tkadw import Adwite, set_default_theme

    set_default_theme("gtk", "light")

    root = Adwite()

    mdi = AdwMDI()
    mdiChild1 = mdi.create_child()
    mdi.pack(fill="both", expand="yes", padx=10, pady=10)

    root.mainloop()
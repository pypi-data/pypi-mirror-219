from tkadw.windows.canvas.drawengine import AdwDrawEngine


class AdwWidget(AdwDrawEngine):

    """
    基础绘制组件类

    特性：自动将背景颜色设为父组件背景颜色
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Configure>", self._draw, add="+")
        self._other()

    def _other(self):
        self.configure(background=self.master.cget("bg"), borderwidth=0)

    def _draw(self, evt=None):
        pass
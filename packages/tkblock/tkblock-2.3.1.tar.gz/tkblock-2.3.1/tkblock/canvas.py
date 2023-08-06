#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""ResizingCanvas

自動調整されるキャンバス
"""
import tkinter as tk


class BlockCanvas(tk.Canvas):
    """tk.Canvas"""

    def __init__(self, frame, *args, **kwargs):
        super().__init__(frame, *args, **kwargs)


class ResizingCanvas(tk.Canvas):
    """ユーザーがフレームサイズを変更した場合、自動調整されるキャンバス

    既存のCanvasはユーザーがwindowsのサイズを変更した場合追従をしてくれない。
    それを回避するために、サイズ変更のイベントのたびに、変更するクラスを作成。

    Args:
        tk (tk.Canvas): キャンバス
    """

    def __init__(self, frame, *args, **kwargs) -> None:
        """コンストラクタ

        Args:
            frame (tk.Frame): キャンバスを乗せる親フレーム
        """
        super().__init__(frame, *args, **kwargs)
        self.width: int = frame.width
        self.height: int = frame.height
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event: tk.Event) -> None:
        """リサイズを行う

        Args:
            event (tk.Event): イベント
        """
        wscale: float = float(event.width) / self.width
        hscale: float = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        self.config(width=event.width, height=event.height)
        self.scale("all", 0, 0, wscale, hscale)

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""BlockWaitingScreen"""
import time
import tkinter as tk
from tkinter import messagebox


FILL_COLOERS = ['white', 'black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']

class BlockWaitingScreen:
    """BlockWaitingScreenクラスは、Tkinterウィンドウにウェイト画面を表示するために使用されます。"""
    def __init__(self, master, is_force_finish, width=400, height=300):
        self.roop_index = 0
        self.top = tk.Toplevel(master)
        self.top.title("Wait Screen")
        self.top.geometry("{}x{}".format(width, height))
        
        # このWindowsが閉じられたとき
        def click_close():
            if messagebox.askokcancel("確認", "想定外の動き！ばぐるかも！本当に閉じていいですか？"):
                self.stop()
                self.is_thread_run = True
                self.end_thread()
                self.top.destroy()
        self.top.protocol("WM_DELETE_WINDOW", click_close)

        # 回転する円描画用のキャンバスを作成
        self.canvas = tk.Canvas(self.top, width=100, height=100)
        self.canvas.place(relx=0.5, rely=0.4, anchor="center")
        self.arc = self.canvas.create_arc(10, 10, 90, 90, start=0, extent=40, outline="magenta")
        
        # 強制終了ボタン
        def _execute_finish():
            is_force_finish[0] = True
            # raise Exception("gega")
        self.button = tk.Button(self.top, width=100, height=5, text="強制終了[未実装]", command=_execute_finish)
        self.button.place(relx=0.5, rely=0.9, anchor="center")


        # キャンバスの描画を回転させるspinメソッドを定期的に実行
        self.angle = 0
        self.delay = 0.1
        self.is_spin = True
        self.is_thread_run = False

    def _spin(self):
        """canvas.create_arc()で描いた円を回転させるアニメーションを実行"""
        if self.is_spin:
            self.canvas.delete(self.arc)
            self.canvas.create_arc(10, 10, 90, 90, start=self.angle, extent=40, fill="red", width=5)
            self.angle += 40
        self.top.after(int(self.delay * 1000), self._spin)
        

    def start(self):
        """BlockWaitingScreenを表示する"""
        self._spin()
        self.top.update_idletasks()
        self.top.update()

    def stop(self):
        """BlockWaitingScreenの円アニメーションを停止する"""
        self.is_spin = False

    def start_thread(self):
        self.is_thread_run = True
        fill_colors = FILL_COLOERS.copy()
        while self.is_spin:
            if self.angle < 360:
                if len(fill_colors) == 0:
                    fill_colors = FILL_COLOERS.copy()
                color = fill_colors.pop()
                self.canvas.create_arc(10, 10, 90, 90, start=self.angle, extent=40, fill=color, outline=color)
                self.angle += 40
            else:
                self.canvas.delete("all")
                self.angle = 0
            time.sleep(0.5)
            self.roop_index += 1
            self.top.update_idletasks()
        self.is_thread_run = False

    def end_thread(self):
        """BlockWaitingScreenの円アニメーションを停止する
        
        start_thread
        """
        self.is_spin = False
        while self.is_thread_run:
            time.sleep(0.1)
        self.top.destroy()


    def restart(self):
        """BlockWaitingScreenの円アニメーションを再開する"""
        self.is_spin = True
        
    def destroy(self):
        self.top.destroy()



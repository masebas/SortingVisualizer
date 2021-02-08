import numpy as np
import time
import threading
from tkinter import *


# Color Scheme
surface = "#404040"
background = "#404040"
primary = "#BB86FC"
secondary = "#00A367"
tertiery = "#C96F00"
textsurf = "#FFFFFF"
textprim = "#000000"
bars = "#CF6679"

canvas_height = 870
canvas_width = 1910
canvas = None
root = None

ui_args = None
class SortingAlgorithms:

    def __init__(self, *args):
        global canvas, root
        canvas, root = args

    def drawData(self, arr, color_arr):
        canvas.delete("all")
        c_height = canvas_height
        c_width = canvas_width
        x_width = c_width / (len(arr) + 1)
        offset = 30
        spacing = 10

        normalizedArr = [i / max(arr) for i in arr]
        for i, height in enumerate(normalizedArr):
            # Top left
            x0 = i * x_width + offset + spacing
            y0 = c_height - height * (c_height - 50)

            # Bottom right
            x1 = x0 + (1000 / len(arr))
            y1 = c_height
            canvas.create_rectangle(x0, y0, x1, y1, fill=color_arr[i], outline="")
            canvas.create_text(x0 + 2, y0, anchor=SW, text=str(arr[i]), fill=textsurf)

        root.update_idletasks()

    def get_color_arr(self, length, left, pivot, right):
        color_arr = []

        for i in range(length):
            if left <= i <= right:
                if i <= pivot:
                    color_arr.append(primary)
                else:
                    color_arr.append(tertiery)
            else:
                color_arr.append(bars)

        return color_arr

    def qs_get_color_arr(self, length, head, tail, border, k, is_swapping = False):
        color_arr = []
        for i in range(length):
            if head <= i <= tail:
                color_arr.append(bars)
            else:
                color_arr.append("gray")

            if i == tail:
                color_arr[i] = tertiery
            elif i == border:
                color_arr[i] = primary
            elif i == k:
                color_arr[i] = secondary

            if is_swapping:
                if i == border or i == k:
                    color_arr[i] = "blue"

        return color_arr

    # Insertion Sort
    def insertion_sort(self, arr, timeint, exit_flag):
        if not isinstance(exit_flag, threading.Event):
            raise TypeError
        if exit_flag.is_set():
            return

        print("Running Insertion Sort")
        # Check if arr has more than 1 value. If it does not, it is already sorted, so we return the array
        if len(arr) <= 1:
            return arr

        # Determine the index length
        index_len = range(1, len(arr))

        # Iterate over each index in arr
        for i in index_len:
            if exit_flag.is_set():
                break
            k = arr[i]  # Assign the key

            # Compare the key to the element to the left of it and swap them if the key is smaller until the key is larger
            while arr[i-1] > k and i > 0:
                if exit_flag.is_set():
                    break
                arr[i], arr[i-1] = arr[i-1], arr[i]
                i -= 1
                self.drawData(arr, [primary if x == i or x == i - 1 else bars for x in range(len(arr))])
                time.sleep(timeint)

        self.drawData(arr, [secondary for x in range(len(arr))])
        return arr  # Profit

    # Merge Sort
    def merge_sort(self, arr, timeint, exit_flag):
        if not isinstance(exit_flag, threading.Event):
            raise TypeError

        if exit_flag.is_set():
            return

        print("Running Merge Sort")
        self.merge_algo(arr, 0, len(arr)-1, timeint, exit_flag)

    def merge(self, arr, left, pivot, right, timeint, exit_flag):
        if exit_flag.is_set():
            return

        self.drawData(arr, self.get_color_arr(len(arr), left, pivot, right))
        time.sleep(timeint)

        d_left = arr[left:pivot+1]
        d_right = arr[pivot+1:right+1]
        k_left = k_right = 0

        for k_arr in range(left, right+1):
            if exit_flag.is_set():
                break

            if k_left < len(d_left) and k_right < len(d_right):
                if d_left[k_left] <= d_right[k_right]:
                    arr[k_arr] = d_left[k_left]
                    k_left += 1

                else:
                    arr[k_arr] = d_right[k_right]
                    k_right += 1

            elif k_left < len(d_left):
                arr[k_arr] = d_left[k_left]
                k_left += 1

            else:
                arr[k_arr] = d_right[k_right]
                k_right += 1

        self.drawData(arr, [secondary if left <= x <= right else bars for x in range(len(arr))])
        time.sleep(timeint)

    def merge_algo(self, arr, left, right, timeint, exit_flag):
        if exit_flag.is_set():
            return

        if left < right:
            pivot = (left + right) // 2
            self.merge_algo(arr, left, pivot, timeint, exit_flag)
            self.merge_algo(arr, pivot + 1, right, timeint, exit_flag)
            self.merge(arr, left, pivot, right, timeint, exit_flag)

    # Quick sort
    def qs_part(self, arr, head, tail, timeint, exit_flag):
        if exit_flag.is_set():
            return

        border = head
        qs_pivot = arr[tail]

        self.drawData(arr, self.qs_get_color_arr(len(arr), head, tail, border, border))
        time.sleep(timeint)

        for j in range(head, tail):
            if exit_flag.is_set():
                break
            if arr[j] < qs_pivot:
                self.drawData(arr, self.qs_get_color_arr(len(arr), head, tail, border, j, is_swapping=True))
                time.sleep(timeint)

                arr[border], arr[j] = arr[j], arr[border]
                border += 1

            self.drawData(arr, self.qs_get_color_arr(len(arr), head, tail, border, j))
            time.sleep(timeint)

        self.drawData(arr, self.qs_get_color_arr(len(arr), head, tail, border, tail, is_swapping=True))
        time.sleep(timeint)
        arr[border], arr[tail] = arr[tail], arr[border]
        return border

    def quick_sort(self, arr, head, tail, timeint, exit_flag):
        if not isinstance(exit_flag, threading.Event):
            raise TypeError
        if exit_flag.is_set():
            return
        if head < tail:
            k_part = self.qs_part(arr, head, tail, timeint, exit_flag)

            # Left Part
            self.quick_sort(arr, head, k_part-1, timeint, exit_flag)
            # Right Part
            self.quick_sort(arr, k_part+1, tail, timeint, exit_flag)


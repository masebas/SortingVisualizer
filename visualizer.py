from tkinter import *
from tkinter import ttk
import random as rng
import sortingAlgorithms as sa
import threading

# Color Scheme
surface = "#404040"
background = "#404040"
primary = "#BB86FC"
secondary = "#00A367"
textsurf = "#FFFFFF"
textprim = "#000000"
bars = "#CF6679"

root = Tk()
root.title("Sorting Algorithm Visualisation")
root.maxsize(1920, 1080)
root.config(bg=background)

# Variables
selected_alg = StringVar()
canvas_height = 870
canvas_width = 1910
arr = []
alg_thread = threading.Thread(target=None)
exit_flag = threading.Event()
is_exit_flag = False
b = threading.Barrier(2, timeout=5)


# Functions
def generate():
    global arr
    print("Selected Algorithm: " + selected_alg.get())
    if randomseed.get() != "":
        rng.seed(int(randomseed.get()))

    try:
        min_val = int(min_entry.get())
    except:
        min_val = 0

    try:
        max_val = int(max_entry.get())
    except:
        max_val = 10

    try:
        size = int(size_entry.get())
    except:
        size = 10

    if min_val < 0:
        min_val = 0

    if max_val < min_val:
        min_val, max_val = max_val, min_val

    arr = []
    for k in range(size):
        arr.append(rng.randrange(min_val, max_val+1))

    drawData(arr, [bars for x in range(len(arr))])


def drawData(arr, color_arr):
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
        canvas.create_text(x0+2, y0, anchor=SW, text=str(arr[i]), fill=textsurf)

    #root.update_idletasks()


def start_alg():
    global arr
    global alg_thread
    global is_exit_flag

    if not arr:
        return

    exit_flag.clear()
    alg_to_start = None
    args = None
    if alg_menu.get() == "Insertion Sort":
        print("Starting Insertion Sort on new thread")
        alg_to_start = algs.insertion_sort
        args = arr, speedScaler.get()
    elif alg_menu.get() == "Merge Sort":
        alg_to_start = algs.merge_sort
        args = arr, speedScaler.get()
    elif alg_menu.get() == "Quick Sort":
        alg_to_start = algs.quick_sort
        args = arr, 0, len(arr)-1, speedScaler.get(), exit_flag

    alg_thread = threading.Thread(target=alg_to_start, args=(*args, exit_flag))
    alg_thread.start()

    #if is_exit_flag:
        #drawData(arr, ["gray" for x in range(len(arr))])
    #else:
        #drawData(arr, [secondary for x in range(len(arr))])


def stop_alg():
    global is_exit_flag

    if alg_thread.is_alive():
        exit_flag.set()
        is_exit_flag = True



# Frame / Base layout
UI_frame = Frame(root, width=canvas_width, height=200, bg=surface)
UI_frame.grid(row=0, column=0, padx=0, pady=1)

canvas = Canvas(root, width=canvas_width, height=canvas_height, bg=surface, relief="flat", highlightthickness=0)
canvas.grid(row=1, column=0, padx=0, pady=1)
ui_args = canvas, root
algs = sa.SortingAlgorithms(*ui_args)

# UI Area
# Row 0
Label(UI_frame, text="Algorithm: ", bg=surface, fg=textsurf, highlightthickness=0).grid(row=0, column=0, padx=5, pady=5, sticky=W)
alg_menu = ttk.Combobox(UI_frame, textvariable=selected_alg, values=["Insertion Sort", "Merge Sort", "Quick Sort"])
alg_menu.grid(row=0, column=1, padx=5, pady=5)
alg_menu.current(0)

Label(UI_frame, text="Speed (s): ", bg=surface, fg=textsurf, highlightthickness=0).grid(row=0, column=4, padx=5, pady=5, sticky=E)
speedScaler = Scale(UI_frame, from_=0, to=1.0, width=10, length=120, bg=surface, fg=textsurf, digits=5, resolution=0.001, orient=HORIZONTAL, relief="flat", sliderrelief="flat", sliderlength="15", highlightthickness=0)
speedScaler.grid(row=0, column=5, padx=5, pady=5)
Button(UI_frame, text="Run", command=start_alg, bg=secondary, highlightthickness=0, relief="flat", width=10).grid(row=0, column=6, padx=5, pady=5)
Button(UI_frame, text="Stop", command=stop_alg, bg=bars, highlightthickness=0, relief="flat", width=10).grid(row=0, column=7, padx=5, pady=5)
# Row 1
Label(UI_frame, text="Size: ", bg="#404040", fg="white", relief="flat").grid(row=1, column=0, padx=5, pady=5, sticky=E)
size_entry = Entry(UI_frame, relief="flat", highlightthickness=0, width=20)
size_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

Label(UI_frame, text="Min Value: ", bg="#404040", fg="white", relief="flat", highlightthickness=0).grid(row=1, column=2, padx=5, pady=5, sticky=E)
min_entry = Entry(UI_frame, relief="flat", highlightthickness=0, width=20)
min_entry.grid(row=1, column=3, padx=5, pady=5, sticky=W)

Label(UI_frame, text="Max Value: ", bg="#404040", fg="white", relief="flat").grid(row=1, column=4, padx=5, pady=5, sticky=E)
max_entry = Entry(UI_frame, relief="flat", highlightthickness=0, width=20)
max_entry.grid(row=1, column=5, padx=5, pady=5, sticky=W)

Button(UI_frame, text="Generate", command=generate, bg="white", highlightthickness=0, relief="flat", width=10).grid(row=1, column=6, padx=5, pady=5)

Label(UI_frame, text="Seed: ", bg="#404040", fg="white", relief="flat").grid(row=1, column=7, padx=5, pady=5, sticky=E)
randomseed = Entry(UI_frame, relief="flat", highlightthickness=0, width=20)
randomseed.grid(row=1, column=8, padx=5, pady=8, sticky=W)

root.after(1, )
root.mainloop()


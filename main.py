import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from PIL import Image
from mpl_toolkits.axes_grid1 import make_axes_locatable
import tkinter as tk
from tkinter import filedialog, messagebox

params = {}
def get_params():
    try:
        params['file_path'] = entry_path.get()
        params['q'] = float(entry_q.get())
        params['m'] = float(entry_m.get())
        params['vx'] = float(entry_vx.get())
        params['vy'] = float(entry_vy.get())
        params['x'] = float(entry_x.get())
        params['y'] = float(entry_y.get())

        if not params['file_path']:
            raise ValueError("Wybierz plik obrazu!")

        root.quit()
        root.destroy()
    except ValueError as e:
        messagebox.showerror("Błąd", f"Nieprawidłowe dane: {e}")


def select_file():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    entry_path.delete(0, tk.END)
    entry_path.insert(0, path)


#-----------------Tworzenie okna początkowego------------------
root = tk.Tk()
root.title("Ustawienia symulacji")
window_width = 600
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)

custom_font = ("Arial", 12)
header_font = ("Arial", 14, "bold")


tk.Label(root, text="Parametry Cząstki", font=header_font).grid(row=0, column=0, columnspan=3, pady=20)


tk.Label(root, text="Obraz pola:", font=custom_font).grid(row=1, column=1, sticky="w")
entry_path = tk.Entry(root, font=custom_font)
entry_path.grid(row=2, column=1, sticky="we", pady=(0, 10))
tk.Button(root, text="Wybierz plik...", command=select_file).grid(row=2, column=2, padx=5, pady=(0, 10))

tk.Label(root, text="Ładunek (q):", font=custom_font).grid(row=3, column=1, sticky="w")
entry_q = tk.Entry(root, font=custom_font, justify='center')
entry_q.insert(0, "1.0")
entry_q.grid(row=4, column=1, sticky="we", pady=(0, 10))


tk.Label(root, text="Masa (m):", font=custom_font).grid(row=5, column=1, sticky="w")
entry_m = tk.Entry(root, font=custom_font, justify='center')
entry_m.insert(0, "1.0")
entry_m.grid(row=6, column=1, sticky="we", pady=(0, 10))

tk.Label(root, text="Prędkość x (v0_x):", font=custom_font).grid(row=7, column=1, sticky="w")
entry_vx = tk.Entry(root, font=custom_font, justify='center')
entry_vx.insert(0, "13.0")
entry_vx.grid(row=8, column=1, sticky="we", pady=(0, 10))

tk.Label(root, text="Prędkość y (v0_y):", font=custom_font).grid(row=9, column=1, sticky="w")
entry_vy = tk.Entry(root, font=custom_font, justify='center')
entry_vy.insert(0, "7.5")
entry_vy.grid(row=10, column=1, sticky="we", pady=(0, 10))

tk.Label(root, text="Położenie x:", font=custom_font).grid(row=11, column=1, sticky="w")
entry_x = tk.Entry(root, font=custom_font, justify='center')
entry_x.insert(0, "200")
entry_x.grid(row=12, column=1, sticky="we", pady=(0, 10))

tk.Label(root, text="Położenie y:", font=custom_font).grid(row=13, column=1, sticky="w")
entry_y = tk.Entry(root, font=custom_font, justify='center')
entry_y.insert(0, "200")
entry_y.grid(row=14, column=1, sticky="we", pady=(0, 10))


btn_start = tk.Button(
    root,
    text="URUCHOM SYMULACJĘ",
    command=get_params,
    bg="green",
    fg="white",
    font=header_font,
    height=2
)
btn_start.grid(row=15, column=0, columnspan=3, pady=30, padx=50, sticky="we")

root.mainloop()

#-----------------Wczytanie danych------------------

imgIN = Image.open(params['file_path']).convert('L')
img = imgIN.transpose(Image.FLIP_TOP_BOTTOM)
arr = np.array(img)
B_field = (arr.astype(float) - 128) / 128.0

q = params['q']
m = params['m']
vel = np.array([params['vx'], params['vy']])
file_path = params['file_path']
pos = np.array([params['x'], params['y']])
steps = 3000
dt = 0.1
trajectory = []


for _ in range(steps):
    ix, iy = int(pos[0]), int(pos[1])

    if 0 <= ix < B_field.shape[1] and 0 <= iy < B_field.shape[0]:
        Bz = B_field[iy, ix]

        # Siła Lorentza w 2D: Fx = q * vy * Bz, Fy = -q * vx * Bz
        F = q * np.array([vel[1] * Bz, -vel[0] * Bz])

        acc = F / m

        vel += acc * dt
        pos += vel * dt

        trajectory.append(pos.copy())
    else:
        trajectory.pop([-1][-1])
        break

#-----------------Animacja------------------
traj = np.array(trajectory)
fig, ax = plt.subplots(figsize=(12, 8))
im = ax.imshow(B_field, cmap='PuOr_r', origin='lower')
ax.axis('image')

# Tworzymy pustą linię (trajektoria) i punkt (cząstka)
line, = ax.plot([], [], color='green', linewidth=2, label="Trajektoria")
point, = ax.plot([], [], 'ro', markersize=8, label="Cząstka")  # Czerwona kropka

ax.set_title("Ruch cząstki w zmiennym polu magnetycznym")
ax.legend()

# Dodatki (colorbar itp.)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(im, cax=cax)
cbar.set_ticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0])


def frame(i):
    line.set_data(traj[:i, 0], traj[:i, 1])

    point.set_data([traj[i, 0]], [traj[i, 1]])

    return line, point



anim = FuncAnimation(
    fig=fig,
    func=frame,
    frames=len(traj),
    interval=10,
    blit=True
)

plt.show()

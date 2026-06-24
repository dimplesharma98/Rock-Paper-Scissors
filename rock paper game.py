import tkinter as tk
import random

window = tk.Tk()
window.title("Rock Paper Scissors")
window.geometry("480x630")
window.config(bg="#0a0a0a")
window.resizable(False, False)

user_score = 0
comp_score = 0

# ── Animated background canvas ───────────────────────────────────────────────
canvas = tk.Canvas(window, width=480, height=630,
                   bg="#a3e7f5", highlightthickness=0)
canvas.place(x=0, y=0)

circles = []
circle_data = [
    [40,  80,  30, 1.2, "#ff0055"],
    [400, 150, 20, 0.8, "#ff0055"],
    [200, 520, 25, 1.0, "#cc0044"],
    [80,  400, 18, 1.5, "#ff3377"],
    [420, 450, 22, 0.9, "#ff0055"],
    [320, 60,  15, 1.3, "#cc0044"],
]

for x, y, r, s, c in circle_data:
    cid = canvas.create_oval(x-r, y-r, x+r, y+r,
                             outline=c, width=2, fill="")
    circles.append({"id": cid, "x": x, "y": y,
                    "r": r, "dy": s, "color": c})

def animate():
    for ci in circles:
        ci["y"] += ci["dy"]
        if ci["y"] > 650 or ci["y"] < -20:
            ci["dy"] *= -1
        canvas.coords(ci["id"],
                      ci["x"]-ci["r"], ci["y"]-ci["r"],
                      ci["x"]+ci["r"], ci["y"]+ci["r"])
    window.after(30, animate)

animate()

# ── Title ─────────────────────────────────────────────────────────────────────
tk.Label(window, text="🪨  📄  ✂️",
         font=("Arial", 17,"bold"), bg="#a3e7f5", fg="#1a1f22").place(x=185, y=15)

tk.Label(window, text="ROCK  PAPER  SCISSORS",
         font=("Arial", 18, "bold"),
         bg="#a3e7f5", fg="#dc4e1b").place(x=80, y=43)

tk.Label(window, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
         font=("Arial", 8),  bg="#a3e7f5", fg="#dc4e1b").place(x=50, y=73)

# ── Instructions ─────────────────────────────────────────────────────────────
inst = tk.Frame(window, bg="#FFB6C8",
                highlightbackground="#CC2255", highlightthickness=2)
inst.place(x=18, y=88, width=444, height=105)
 
tk.Label(inst, text="📋  HOW TO PLAY",
         font=("Arial", 12, "bold"),
         bg="#FFB6C8", fg="#222222").pack(pady=(10, 6))
 
row1 = tk.Frame(inst, bg="#FFB6C8")
row1.pack()
tk.Label(row1, text="🪨 Rock  beats  ✂️ Scissors",
         font=("Arial", 9, "bold"), bg="#FFB6C8", fg="#333").pack(side="left", padx=14)
tk.Label(row1, text="✂️ Scissors  beats  📄 Paper",
         font=("Arial", 9, "bold"), bg="#FFB6C8", fg="#333").pack(side="left", padx=14)
 
row2 = tk.Frame(inst, bg="#FFB6C8")
row2.pack(pady=(4,0))
tk.Label(row2, text="📄 Paper  beats  🪨 Rock",
         font=("Arial", 9, "bold"), bg="#FFB6C8", fg="#333").pack(side="left", padx=14)
tk.Label(row2, text="Same choice  =  Tie  🤝",
         font=("Arial", 9, "bold"), bg="#FFB6C8", fg="#333").pack(side="left", padx=14)

# ── Scoreboard ────────────────────────────────────────────────────────────────
you_var = tk.StringVar(value="0")
tie_var = tk.StringVar(value="0")
cpu_var = tk.StringVar(value="0")

for i, (lbl, var, xpos) in enumerate([
        ("YOU",  you_var, 55),
        ("TIE",  tie_var, 185),
        ("CPU",  cpu_var, 315)]):
    f = tk.Frame(window, bg="light pink",
                 highlightbackground="#0a080a", highlightthickness=1)
    f.place(x=xpos, y=200, width=110, height=58)
    tk.Label(f, text=lbl, font=("Arial", 10, "bold"),
             bg="light pink", fg="#1e1918").place(x=38, y=5)
    tk.Label(f, textvariable=var, font=("Arial", 22, "bold"),
             bg="light pink", fg="purple").place(x=38, y=24)

# ── Arena ─────────────────────────────────────────────────────────────────────
arena = tk.Frame(window, bg="light pink",
                 highlightbackground="#110D0E", highlightthickness=1)
arena.place(x=40, y=275, width=400, height=115)

user_lbl = tk.Label(arena, text="❓", font=("Arial", 45),
                    bg="light pink")
user_lbl.place(x=25, y=18)

tk.Label(arena, text="YOU", font=("seougi", 11, "bold"),
         bg="light pink", fg="#8e217a").place(x=55, y=82)

tk.Label(arena, text="VS", font=("seougi", 16, "bold"),
         bg="light pink", fg="#440022").place(x=178, y=40)

comp_lbl = tk.Label(arena, text="❓", font=("seougi", 45),
                    bg="light pink")
comp_lbl.place(x=295, y=18)

tk.Label(arena, text="CPU", font=("seougi", 11, "bold"),
         bg="light pink", fg="#8e217a").place(x=315, y=82)

# ── Result labels ─────────────────────────────────────────────────────────────
result_lbl = tk.Label(window, text="Make your move, Dimple!",
                      font=("seougi", 13, "bold"),
                      bg="#F3EDE8", fg="#120c11")
result_lbl.place(x=75, y=405)

detail_lbl = tk.Label(window, text="",
                      font=("Arial", 10),
                      bg="#F3EDE8", fg="#141111")
detail_lbl.place(x=105, y=432)

# ── Game logic ────────────────────────────────────────────────────────────────
wins_msg = {
    ("rock",     "scissors"): "Rock crushes Scissors! 🪨",
    ("scissors", "paper"):    "Scissors cut Paper! ✂️",
    ("paper",    "rock"):     "Paper covers Rock! 📄",
}

emoji = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

def play(choice):
    global user_score, comp_score
    comp = random.choice(["rock", "paper", "scissors"])

    user_lbl.config(text=emoji[choice])
    comp_lbl.config(text=emoji[comp])

    if choice == comp:
        tie_var.set(str(int(tie_var.get()) + 1))
        result_lbl.config(text="🤝  It's a Tie!", fg="#ea0312")
        detail_lbl.config(text=f"Both chose {choice.capitalize()}")
    elif (choice, comp) in wins_msg:
        user_score += 1
        you_var.set(str(user_score))
        result_lbl.config(text="🎉  You Win!", fg="#1BED22")
        detail_lbl.config(text=wins_msg[(choice, comp)])
    else:
        comp_score += 1
        cpu_var.set(str(comp_score))
        result_lbl.config(text="💀  CPU Wins!", fg="#E65208")
        detail_lbl.config(text=wins_msg.get((comp, choice), "CPU wins!"))

def reset():
    global user_score, comp_score
    user_score = 0
    comp_score = 0
    you_var.set("0")
    cpu_var.set("0")
    tie_var.set("0")
    user_lbl.config(text="❓")
    comp_lbl.config(text="❓")
    result_lbl.config(text="Make your move, Dimple!", fg="#080708")
    detail_lbl.config(text="")

# ── Choice Buttons ────────────────────────────────────────────────────────────
for text, choice, xpos in [
        ("🪨  Rock",     "rock",     45),
        ("📄  Paper",    "paper",    175),
        ("✂️  Scissors", "scissors", 317)]:
    tk.Button(window, text=text,
              font=("seougi", 11, "bold"), width=10,
              bg="light pink", fg="black",
              activebackground="#0d0b0c",
              activeforeground="black",
              relief="raised", cursor="hand2",
              highlightbackground="#2b2628",
              highlightthickness=1,
              command=lambda c=choice: play(c)
              ).place(x=xpos, y=465, width=115, height=48)

# ── Reset Button ──────────────────────────────────────────────────────────────
tk.Button(window, text="↺  RESET",
          font=("Arial", 12, "bold"),
          bg="light pink", fg="#1d1819",
          activebackground="#12100E",
          relief="raised", cursor="hand2",
          highlightbackground="#1F1A1B",
          highlightthickness=2,
          command=reset).place(x=185, y=538, width=110, height=36)

window.mainloop()
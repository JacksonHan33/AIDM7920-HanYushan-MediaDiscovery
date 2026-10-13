"""Generate the VibePick vs MoodFlix wireframe comparison PNG (v2 — fixed)."""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = "/Users/apple/Documents/AIDM7920-HanYushan-MediaDiscovery/docs/wireframes"
os.makedirs(OUT_DIR, exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 11))
fig.suptitle("Phase 1 Prototype Wireframes — VibePick vs MoodFlix",
             fontsize=16, fontweight="bold", y=0.985)

# ============================================================
# LEFT: VibePick
# ============================================================
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.set_aspect("equal")
ax.axis("off")

# Title strip
ax.add_patch(patches.Rectangle((0, 14.7), 10, 0.5, color="#2D5D8A"))
ax.text(5, 14.95, "VibePick  ·  Conversational AI", ha="center", va="center",
        fontsize=14, fontweight="bold", color="white")
ax.text(5, 14.2, "Tell me what you want to watch", ha="center",
        fontsize=10, color="gray", style="italic")

# User chat bubble (y range 11.5 - 13.2)
ax.add_patch(patches.FancyBboxPatch((0.5, 11.4), 9, 1.6, boxstyle="round,pad=0.15",
                                     facecolor="#E8F0F7", edgecolor="#2D5D8A", linewidth=1.2))
ax.text(0.75, 12.7, "You", fontsize=9, color="#2D5D8A", fontweight="bold")
ax.text(0.75, 12.15, "I have 45 minutes,", fontsize=11)
ax.text(0.75, 11.7, "want something light", fontsize=11)

# 3 result cards — start at y=10.5 (well below the chat bubble)
ax.text(5, 10.9, "VibePick picked 3 for you:", ha="center",
        fontsize=10, fontweight="bold", color="#2D5D8A")

movies_left = [
    ("About Time", "2013", "2h 4m",  "Netflix",   "Warm, gentle romantic comedy about time and family — no stress."),
    ("Chef's Table", "2015", "47m",   "Disney+",  "Calm, beautifully-shot food series. Light, warm, perfect for a short break."),
    ("The Nice Guys", "2016", "1h 56m", "HBO Max", "Action-comedy with sharp banter — energetic but not intense."),
]
for i, (title, year, runtime, platform, blurb) in enumerate(movies_left):
    y = 8.0 - i*2.7  # pushed down to clear the 'picked 3 for you' header
    ax.add_patch(patches.FancyBboxPatch((0.5, y), 9, 2.2, boxstyle="round,pad=0.1",
                                         facecolor="white", edgecolor="#2D5D8A", linewidth=1.3))
    ax.add_patch(patches.Rectangle((0.7, y+0.25), 1.3, 1.7, color="#D0D0D0"))
    ax.text(1.35, y+1.1, "poster", ha="center", va="center", fontsize=8, color="gray")
    ax.text(2.2, y+1.7, f"{i+1}. {title} ({year})", fontsize=12, fontweight="bold")
    # Plain ASCII: no ⏱ / no 💚 — use middle dot
    ax.text(2.2, y+1.25, f"· {runtime}   ·   {platform}", fontsize=9.5, color="#444")
    ax.text(2.2, y+0.55, f"\"{blurb}\"", fontsize=8.5, color="#555", style="italic")

# Input box
ax.add_patch(patches.FancyBboxPatch((0.5, 0.3), 9, 0.8, boxstyle="round,pad=0.1",
                                     facecolor="#FAFAFA", edgecolor="gray", linewidth=1))
ax.text(0.75, 0.7, "Type what you want to watch...", fontsize=10, color="gray")
ax.text(9.1, 0.7, "Send", ha="right", fontsize=10, color="#2D5D8A", fontweight="bold")

# ============================================================
# RIGHT: MoodFlix
# ============================================================
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.set_aspect("equal")
ax.axis("off")

ax.add_patch(patches.Rectangle((0, 14.7), 10, 0.5, color="#8A2D5D"))
ax.text(5, 14.95, "MoodFlix  ·  Structured filter", ha="center", va="center",
        fontsize=14, fontweight="bold", color="white")
ax.text(5, 14.2, "Find what to watch in 3 quick steps", ha="center",
        fontsize=10, color="gray", style="italic")

# Step 1 — Time bucket
ax.text(0.5, 13.5, "Step 1 - How much time do you have?", fontsize=11, fontweight="bold")
for i, (label, selected) in enumerate([("< 30m", False), ("30-90m", True), ("> 90m", False)]):
    x = 0.5 + i*3.2
    fc = "#F5E8F0" if selected else "white"
    edge = "#8A2D5D" if selected else "lightgray"
    ax.add_patch(patches.FancyBboxPatch((x, 12.4), 3, 0.8, boxstyle="round,pad=0.05",
                                         facecolor=fc, edgecolor=edge, linewidth=2))
    txt_color = "#8A2D5D" if selected else "black"
    wt = "bold" if selected else "normal"
    ax.text(x+1.5, 12.8, label, ha="center", va="center", fontsize=11,
            color=txt_color, fontweight=wt)

# Step 2 — Mood tags
ax.text(0.5, 11.6, "Step 2 - What mood are you in?", fontsize=11, fontweight="bold")
moods = [("relaxed", True), ("excited", False), ("curious", True),
         ("thoughtful", False), ("need-laugh", True)]
for i, (mood, sel) in enumerate(moods):
    x = 0.5 + (i % 3) * 3.2
    y = 10.7 - (i // 3) * 0.95
    fc = "#F5E8F0" if sel else "white"
    edge = "#8A2D5D" if sel else "lightgray"
    ax.add_patch(patches.FancyBboxPatch((x, y), 2.9, 0.7, boxstyle="round,pad=0.05",
                                         facecolor=fc, edgecolor=edge, linewidth=1.5))
    if sel:
        ax.text(x+0.3, y+0.35, "[x]", fontsize=10, color="#8A2D5D", fontweight="bold", va="center")
    ax.text(x+0.9 if sel else x+1.45, y+0.35, mood, va="center",
            ha="left" if sel else "center", fontsize=10,
            color="#8A2D5D" if sel else "black", fontweight="bold" if sel else "normal")

# Step 3 — Platform toggles
ax.text(0.5, 8.6, "Step 3 - Which platforms do you have?", fontsize=11, fontweight="bold")
platforms = [("Netflix", True), ("Disney+", True), ("Prime", False),
             ("Apple TV+", False), ("HBO Max", False), ("YouTube", False)]
for i, (p, sel) in enumerate(platforms):
    x = 0.5 + (i % 3) * 3.2
    y = 7.5 - (i // 3) * 0.75
    if sel:
        ax.add_patch(patches.Rectangle((x, y+0.1), 0.35, 0.35, facecolor="#8A2D5D", edgecolor="#8A2D5D"))
        ax.text(x+0.175, y+0.275, "x", ha="center", va="center", fontsize=10,
                color="white", fontweight="bold")
    else:
        ax.add_patch(patches.Rectangle((x, y+0.1), 0.35, 0.35, facecolor="white", edgecolor="lightgray"))
    ax.text(x+0.55, y+0.275, p, va="center", fontsize=10,
            color="#8A2D5D" if sel else "black")

# Submit button
ax.add_patch(patches.FancyBboxPatch((3, 5.7), 4, 0.9, boxstyle="round,pad=0.1",
                                     facecolor="#8A2D5D", edgecolor="#8A2D5D"))
ax.text(5, 6.15, "Find 3 movies", ha="center", va="center", fontsize=13,
        color="white", fontweight="bold")

# Result preview
ax.text(0.5, 5.0, "Result - Ranked by match score:", fontsize=10.5, fontweight="bold")
ax.add_patch(patches.FancyBboxPatch((0.5, 2.7), 9, 2.0, boxstyle="round,pad=0.1",
                                     facecolor="#F5E8F0", edgecolor="#8A2D5D", linewidth=1.3))
ax.add_patch(patches.Rectangle((0.7, 2.9), 1.2, 1.6, color="#D0D0D0"))
ax.text(1.3, 3.7, "poster", ha="center", va="center", fontsize=8, color="gray")
ax.text(2.1, 4.2, "1. About Time (2013)", fontsize=11, fontweight="bold")
ax.text(2.1, 3.75, "· 2h 4m   ·   Netflix", fontsize=9, color="#444")
ax.text(2.1, 3.2, "Match 92%  -  time 100% · mood 85% · genre 90%",
        fontsize=8.5, color="#8A2D5D", fontweight="bold")

ax.text(5, 1.8, "Match score:  weighted sum of", ha="center", fontsize=9, color="gray", style="italic")
ax.text(5, 1.45, "time + mood + genre + platform overlap,", ha="center", fontsize=9, color="gray", style="italic")
ax.text(5, 1.1, "calibrated by recent popularity.", ha="center", fontsize=9, color="gray", style="italic")
ax.text(5, 0.5, "→ Transparent criterion, no LLM cost.", ha="center",
        fontsize=9.5, color="#8A2D5D", fontweight="bold")

plt.tight_layout(rect=(0, 0, 1, 0.96))
out = os.path.join(OUT_DIR, "comparison.png")
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
print(f"Saved {out}")

"""Generate the VibePick vs MoodFlix wireframe comparison PNG for the repo."""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("/Users/apple/Documents/AIDM7920-HanYushan-MediaDiscovery/docs/wireframes", exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 11))
fig.suptitle("Phase 1 Prototype Wireframes — VibePick vs MoodFlix",
             fontsize=16, fontweight="bold", y=0.985)

# ============================================================
# LEFT: VibePick — Conversational AI
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

# User chat bubble
ax.add_patch(patches.FancyBboxPatch((0.5, 11.8), 9, 1.7, boxstyle="round,pad=0.15",
                                     facecolor="#E8F0F7", edgecolor="#2D5D8A", linewidth=1.2))
ax.text(0.75, 13.15, "You", fontsize=9, color="#2D5D8A", fontweight="bold")
ax.text(0.75, 12.55, "I have 45 minutes,", fontsize=11)
ax.text(0.75, 12.15, "want something light", fontsize=11)

# AI response header
ax.text(5, 11.0, "VibePick picked 3 for you:", ha="center",
        fontsize=10, fontweight="bold", color="#2D5D8A")

# 3 result cards
for i, (title, year, runtime, platform, blurb) in enumerate([
    ("About Time", 2013, "2h 4m",  "Netflix",   "Warm, gentle romantic comedy about time and family — no stress."),
    ("Chef's Table", 2015, "47m",   "Disney+",  "Calm, beautifully-shot food series. Light, warm, perfect for a short break."),
    ("The Nice Guys", 2016, "1h 56m", "HBO Max", "Action-comedy with sharp banter — energetic but not intense."),
]):
    y = 9.8 - i*2.4
    ax.add_patch(patches.FancyBboxPatch((0.5, y), 9, 2.0, boxstyle="round,pad=0.1",
                                         facecolor="white", edgecolor="#2D5D8A", linewidth=1.3))
    # Movie poster placeholder
    ax.add_patch(patches.Rectangle((0.7, y+0.2), 1.3, 1.6, color="#D0D0D0"))
    ax.text(1.35, y+1.0, "poster", ha="center", va="center", fontsize=8, color="gray")
    # Title
    ax.text(2.2, y+1.55, f"{i+1}. {title} ({year})", fontsize=12, fontweight="bold")
    ax.text(2.2, y+1.15, f"⏱ {runtime}  ·  💚 {platform}", fontsize=9.5, color="#444")
    ax.text(2.2, y+0.5, f"“{blurb}”", fontsize=8.5, color="#555", style="italic", wrap=True)

# Input box
ax.add_patch(patches.FancyBboxPatch((0.5, 0.4), 9, 0.9, boxstyle="round,pad=0.1",
                                     facecolor="#FAFAFA", edgecolor="gray", linewidth=1))
ax.text(0.75, 0.85, "Type what you want to watch...", fontsize=10, color="gray")
ax.text(9.0, 0.85, "⏎", ha="right", fontsize=14, color="#2D5D8A")

# ============================================================
# RIGHT: MoodFlix — Structured filter
# ============================================================
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.set_aspect("equal")
ax.axis("off")

# Title strip
ax.add_patch(patches.Rectangle((0, 14.7), 10, 0.5, color="#8A2D5D"))
ax.text(5, 14.95, "MoodFlix  ·  Structured filter", ha="center", va="center",
        fontsize=14, fontweight="bold", color="white")
ax.text(5, 14.2, "Find what to watch in 3 quick steps", ha="center",
        fontsize=10, color="gray", style="italic")

# Step 1 — Time bucket
ax.text(0.5, 13.5, "Step 1 — How much time do you have?", fontsize=11, fontweight="bold")
for i, (label, selected) in enumerate([("< 30m", False), ("30–90m", True), ("> 90m", False)]):
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
ax.text(0.5, 11.6, "Step 2 — What mood are you in?", fontsize=11, fontweight="bold")
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
        ax.text(x+0.3, y+0.35, "✓", fontsize=11, color="#8A2D5D", fontweight="bold",
                va="center")
    ax.text(x+0.7 if sel else x+1.45, y+0.35, mood, va="center", ha="left" if sel else "center",
            fontsize=10, color="#8A2D5D" if sel else "black", fontweight="bold" if sel else "normal")

# Step 3 — Platform toggles
ax.text(0.5, 8.6, "Step 3 — Which platforms do you have?", fontsize=11, fontweight="bold")
platforms = [("Netflix", True), ("Disney+", True), ("Prime", False),
             ("Apple TV+", False), ("HBO Max", False), ("YouTube", False)]
for i, (p, sel) in enumerate(platforms):
    x = 0.5 + (i % 3) * 3.2
    y = 7.5 - (i // 3) * 0.75
    # checkbox
    if sel:
        ax.add_patch(patches.Rectangle((x, y+0.1), 0.3, 0.3, facecolor="#8A2D5D", edgecolor="#8A2D5D"))
        ax.text(x+0.15, y+0.25, "✓", ha="center", va="center", fontsize=10,
                color="white", fontweight="bold")
    else:
        ax.add_patch(patches.Rectangle((x, y+0.1), 0.3, 0.3, facecolor="white", edgecolor="lightgray"))
    ax.text(x+0.5, y+0.25, p, va="center", fontsize=10, color="#8A2D5D" if sel else "black")

# Submit button
ax.add_patch(patches.FancyBboxPatch((3, 5.7), 4, 0.9, boxstyle="round,pad=0.1",
                                     facecolor="#8A2D5D", edgecolor="#8A2D5D"))
ax.text(5, 6.15, "Find 3 movies", ha="center", va="center", fontsize=13,
        color="white", fontweight="bold")

# Result preview
ax.text(0.5, 5.0, "Result — Ranked by match score:", fontsize=10.5, fontweight="bold")
ax.add_patch(patches.FancyBboxPatch((0.5, 2.7), 9, 2.0, boxstyle="round,pad=0.1",
                                     facecolor="#F5E8F0", edgecolor="#8A2D5D", linewidth=1.3))
ax.add_patch(patches.Rectangle((0.7, 2.9), 1.2, 1.6, color="#D0D0D0"))
ax.text(1.3, 3.7, "poster", ha="center", va="center", fontsize=8, color="gray")
ax.text(2.1, 4.2, "1. About Time (2013)", fontsize=11, fontweight="bold")
ax.text(2.1, 3.75, "⏱ 2h 4m  ·  💚 Netflix", fontsize=9, color="#444")
ax.text(2.1, 3.2, "Match 92%  —  time 100% · mood 85% · genre 90%", fontsize=8.5,
        color="#8A2D5D", fontweight="bold")

# Comparison note
ax.text(5, 1.8, "Match score:  weighted sum of", ha="center", fontsize=9, color="gray", style="italic")
ax.text(5, 1.45, "time + mood + genre + platform overlap,", ha="center", fontsize=9, color="gray", style="italic")
ax.text(5, 1.1, "calibrated by recent popularity.", ha="center", fontsize=9, color="gray", style="italic")
ax.text(5, 0.5, "→ Transparent criterion, no LLM cost.", ha="center",
        fontsize=9.5, color="#8A2D5D", fontweight="bold")

plt.tight_layout(rect=(0, 0, 1, 0.96))
out = "/Users/apple/Documents/AIDM7920-HanYushan-MediaDiscovery/docs/wireframes/comparison.png"
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
print(f"Saved {out}")

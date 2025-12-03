# Snake of Chaos

A chaotic twist on the classic Snake game where speed and risk meet reward!

## 🎮 Game Rules

### Objective
Control the snake to eat apples and grow longer while avoiding walls and your own body.

### Controls
- **Arrow Keys** or **WASD** to change direction
- Snake moves continuously in the current direction

### Items

#### 🍎 Apple (Red)
- **Score:** +1 point (affected by multipliers)
- **Effect:** Snake grows by 1 segment (affected by multipliers)
- Always present on the screen

#### ⚡ Boost (Blue)
- **Duration:** 10 seconds
- **Effect:** Doubles your speed (10 FPS → 20 FPS)
- **STACKABLE:** Collect multiple boosts to go EVEN FASTER!
- **Risk/Reward:** Higher speed = harder control BUT more power-up spawns!
- **Spawn Chance:** 1% per frame

#### ⭐ Multiplier (Yellow)
- **Duration:** 10 seconds
- **Effect:** Doubles both score gained AND snake growth per apple
- **STACKABLE:** Multiple multipliers = exponential growth!
- **Spawn Chance:** 1% per frame

### The Chaos Factor

**Speed creates chaos!** Since power-ups spawn based on frame rate:
- Normal speed (10 FPS) = fewer spawns
- Boosted speed (20 FPS) = **2x more power-up spawns**
- Double boosted (40 FPS) = **4x more spawns!**
- Collect boosts to trigger a cascade of more items = **MAXIMUM CHAOS!**

**But wait, there's more!** Both boosts and multipliers are **STACKABLE**:
- Stack boosts → exponentially faster speed → cascading power-up spawns
- Stack multipliers → exponential score/growth → massive snake in seconds
- Stack BOTH → absolute pandemonium! 🔥

The faster you go, the more opportunities appear... but can you survive the chaos you create?

## ⚙️ Customization

Edit constants in `main.py`:
- `GRID_SIZE`: Change snake/item size (default: 20)
- `WINDOW_SIZE`: Adjust game window dimensions
- `BOOST_CHANCE` / `MULTIPLIER_CHANCE`: Control spawn rates (default: 1%)
- `BOOST_DURATION` / `MULTIPLIER_DURATION`: Adjust effect timers (default: 10s)

## 🎯 Strategy Tips

1. **Chain boosts** for maximum chaos and power-up cascades
2. **Stack multipliers** before eating apples for huge gains
3. **Combine both** for the ultimate high-risk, high-reward gameplay
4. **High speed = high risk** - plan your path carefully!
5. Use walls to create safe zones when overwhelmed by your own chaos

Good luck surviving the chaos! 🐍💥🔥
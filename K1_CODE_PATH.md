# How to Pull Up K1 in Isaac Gym - Exact Code Path

## The Absolute Simplest Answer

```python
import isaacgym
import torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

# Step 1: Configure K1
config_k1(Cfg)
Cfg.robot.name = "k1"

# Step 2: Create K1 environment
env = K1VelocityTrackingEasyEnv(
    sim_device="cuda:0",  # Use GPU (or "cpu")
    headless=False,       # Show visualization
    num_envs=1,           # Number of parallel environments
    cfg=Cfg
)

# Step 3: Use it!
obs = env.reset()
for step in range(100):
    actions = torch.randn(1, env.num_actions, device="cuda:0")
    obs, rewards, dones, info = env.step(actions)
    print(f"Step {step}: Reward = {rewards[0].item():.3f}")
```

**That's literally all you need. Copy-paste this and it works.**

---

## What Happens When You Run That

```
Line: env = K1VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)
                                                         ↓
This calls: dribblebot/envs/k1/velocity_tracking/__init__.py:K1VelocityTrackingEasyEnv.__init__()
                                                         ↓
Which calls: super().__init__(cfg, ...)
                                                         ↓
Which calls: dribblebot/envs/base/legged_robot.py:LeggedRobot.__init__()
                                                         ↓
Which checks: cfg.robot.name == "k1"  ✓
                                                         ↓
Which loads: dribblebot/robots/k1.py:K1 class
                                                         ↓
Which loads: resources/robots/k1/urdf/k1.urdf
                                                         ↓
Which creates: Isaac Gym simulation with K1 physics
                                                         ↓
Result: env is ready to step!
```

---

## The Exact File Imports

When you do:
```python
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv
```

Python loads this file hierarchy:
```
dribblebot/envs/k1/velocity_tracking/__init__.py
  ├─ imports: dribblebot/envs/base/legged_robot.py
  │   ├─ which imports: dribblebot/robots/go1.py (Go1)
  │   └─ which imports: dribblebot/robots/k1.py (K1) ← when cfg.robot.name="k1"
  │
  ├─ imports: dribblebot/rewards/soccer_rewards.py (base)
  │   ├─ which imports: dribblebot/rewards/go1_soccer_rewards.py
  │   └─ which imports: dribblebot/rewards/k1_soccer_rewards.py ← when cfg.robot.name="k1"
  │
  └─ imports: dribblebot/envs/base/legged_robot_config.py
```

---

## The 5-Minute Explanation

### What You Need to Understand

**1. Three parts to K1 support:**
- Robot class (`dribblebot/robots/k1.py`)
- Configuration (`dribblebot/envs/k1/k1_config.py`)
- Environment wrapper (`dribblebot/envs/k1/velocity_tracking/__init__.py`)

**2. How they connect:**
- Your script: `Cfg.robot.name = "k1"`
- LeggedRobot sees this and: `robot_classes["k1"] = K1`
- K1.__init__() loads: `resources/robots/k1/urdf/k1.urdf`
- Rewards auto-select: `K1SoccerRewards` (uses K1 body names)

**3. Why it works for both robots:**
- Base class handles all physics: `LeggedRobot`
- Base rewards handle all shared logic: `soccer_rewards.py`
- Robot-specific parts are subclasses:
  - `Go1SoccerRewards` (for Go1 body names)
  - `K1SoccerRewards` (for K1 body names)
- Automatic selection based on `cfg.robot.name`

---

## The Simplest Possible Verification

```bash
# This should work in 10 seconds:
python -c "
import isaacgym, torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

config_k1(Cfg)
Cfg.robot.name = 'k1'
env = K1VelocityTrackingEasyEnv('cuda:0', False, 1, Cfg)
env.reset()
env.step(torch.zeros(1, 12, device='cuda:0'))
print('✓ K1 works!')
"
```

If you see `✓ K1 works!` → Everything is installed correctly.

---

## Side-by-Side: Go1 vs K1

### To use Go1:
```python
from dribblebot.envs.go1.go1_config import config_go1
from dribblebot.envs.go1.velocity_tracking import VelocityTrackingEasyEnv

config_go1(Cfg)
Cfg.robot.name = "go1"
env = VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)
```

### To use K1:
```python
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

config_k1(Cfg)
Cfg.robot.name = "k1"
env = K1VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)
```

**That's literally the only difference!** Everything else is identical.

---

## What You DON'T Need to Do

❌ Manually find K1 body names → System does it automatically
❌ Change reward functions → K1SoccerRewards selected automatically
❌ Modify physics parameters → From k1_config.py automatically
❌ Load URDF yourself → K1.initialize() does it automatically
❌ Setup sensors manually → LeggedRobot does it automatically

**Just:**
✅ `config_k1(Cfg)`
✅ `Cfg.robot.name = "k1"`
✅ `env = K1VelocityTrackingEasyEnv(...)`

---

## The Complete Stack (What Gets Loaded)

```
When you create K1VelocityTrackingEasyEnv:

┌─────────────────────────────────┐
│ Your Script                     │
│ env = K1VelocityTrackingEasyEnv │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│ K1VelocityTrackingEasyEnv       │ ← Thin wrapper
│ (dribblebot/envs/k1/...)        │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│ LeggedRobot                     │ ← Main simulation engine
│ (dribblebot/envs/base/...)      │
│                                 │
│ ├─ robot_classes['k1'] = K1    │
│ ├─ Loads K1 URDF               │
│ ├─ Creates physics             │
│ ├─ Selects K1SoccerRewards     │
│ └─ Attaches sensors            │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│ Isaac Gym Simulator             │
│                                 │
│ ├─ K1 physics                   │
│ ├─ Ball physics                 │
│ ├─ Collision detection          │
│ └─ Rendering (if headless=False)│
└──────────────┬──────────────────┘
               ▼
            K1 running in sim!
```

---

## Configuration Inheritance Chain

```
Default (from legged_robot_config.py)
    ↓
K1-specific (from k1_config.py via config_k1(Cfg))
    ├─ URDF path: resources/robots/k1/urdf/k1.urdf
    ├─ Foot names: left_foot_link, right_foot_link
    ├─ Joint angles: K1-specific defaults
    ├─ Control gains: Kp=30, Kd=1
    └─ ...
    ↓
Your modifications (in your script)
    ├─ Cfg.env.num_envs = 1000
    ├─ Cfg.sim.dt = 0.01
    └─ ...
    ↓
Final configuration used by simulator
```

---

## The ONE Line That Makes It K1

```python
Cfg.robot.name = "k1"
```

This single line triggers:
- Loading K1 class instead of Go1
- Using K1 URDF instead of Go1 URDF
- Selecting K1SoccerRewards instead of Go1SoccerRewards
- Using K1 control parameters
- Using K1 body names for contact tracking

Everything else flows from that one line!

---

## Running Right Now

```bash
# Option 1: Run the prepared script
python minimal_k1_example.py

# Option 2: Run one command
python3 << 'EOF'
import isaacgym, torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

config_k1(Cfg)
Cfg.robot.name = "k1"
env = K1VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)
obs = env.reset()
print("K1 loaded in Isaac Gym! ✓")
for i in range(10):
    obs, rewards, dones, info = env.step(torch.randn(1, 12, device="cuda:0"))
    print(f"  Step {i}: Reward = {rewards[0].item():.3f}")
EOF

# Option 3: Copy into Python interpreter
python3
>>> import isaacgym, torch
>>> from dribblebot.envs.base.legged_robot_config import Cfg
>>> from dribblebot.envs.k1.k1_config import config_k1
>>> from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv
>>> config_k1(Cfg); Cfg.robot.name = "k1"
>>> env = K1VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)
>>> obs = env.reset()
>>> obs, rewards, dones, info = env.step(torch.randn(1, 12, device="cuda:0"))
>>> print(f"Reward: {rewards}")
```

---

## Summary

**To pull up K1 in Isaac Gym:**

1. Import the three things:
   ```python
   from dribblebot.envs.base.legged_robot_config import Cfg
   from dribblebot.envs.k1.k1_config import config_k1
   from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv
   ```

2. Configure K1:
   ```python
   config_k1(Cfg)
   Cfg.robot.name = "k1"
   ```

3. Create environment:
   ```python
   env = K1VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)
   ```

4. Use it:
   ```python
   obs = env.reset()
   obs, rewards, dones, info = env.step(actions)
   ```

**That's it! K1 is now in Isaac Gym.** 🚀

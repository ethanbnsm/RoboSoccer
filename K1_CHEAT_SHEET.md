# K1 Isaac Gym - Visual Cheat Sheet

## The Absolute Fastest Way (Copy-Paste This!)

```python
# Copy this entire block and run it
import isaacgym, torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

config_k1(Cfg)
Cfg.robot.name = "k1"
env = K1VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)
obs = env.reset()
print("✓ K1 is running!")

# Now you can step:
for _ in range(100):
    obs, rewards, dones, info = env.step(torch.randn(1, 12, device="cuda:0"))
    print(f"Reward: {rewards[0].item():.3f}")
```

**That's it! K1 is now in Isaac Gym.**

---

## File Structure (What Gets Used)

```
When you run:
  K1VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)

The code loads these files in order:

1. dribblebot/envs/k1/velocity_tracking/__init__.py
   └─ Defines K1VelocityTrackingEasyEnv class

2. dribblebot/envs/base/legged_robot.py
   └─ LeggedRobot base class (does the heavy lifting)
   
   Inside _create_envs():
   3a. dribblebot/robots/k1.py
       └─ Loads URDF: resources/robots/k1/urdf/k1.urdf
       
   3b. resources/robots/k1/meshes/*.STL
       └─ Visual geometry for rendering
       
   3c. Finds body names from URDF:
       ✓ left_foot_link, right_foot_link (feet)
       ✓ Left_Shank, Right_Shank (for collisions)
       ✓ Trunk (for termination)
   
   Inside _prepare_reward_function():
   4. dribblebot/rewards/k1_soccer_rewards.py
      └─ K1-specific reward calculations
      └─ Uses Right_Hip_Yaw body for dribbling

5. All sensors get attached
   └─ ObjectSensor, OrientationSensor, etc.

RESULT: K1 physics simulation ready in Isaac Gym!
```

---

## Configuration Cascade

```
Your Script Sets:
  Cfg.robot.name = "k1"
  
This triggers a chain of events:

config_k1(Cfg)
  ├─ Sets Cfg.asset.file = "resources/robots/k1/urdf/k1.urdf"
  ├─ Sets Cfg.asset.foot_name = "foot_link"
  ├─ Sets Cfg.asset.penalize_contacts_on = ["Shank"]
  ├─ Sets Cfg.asset.terminate_after_contacts_on = ["Trunk"]
  ├─ Sets joint default angles for K1
  └─ Sets control parameters (stiffness, damping, etc.)

LeggedRobot sees Cfg.robot.name = "k1":
  ├─ Selects robot_classes["k1"] = K1
  ├─ Instantiates K1 robot class
  ├─ K1.__init__() → loads URDF
  └─ K1VelocityTrackingEasyEnv.step() → uses K1SoccerRewards

K1SoccerRewards sees Cfg.robot.name = "k1":
  ├─ Uses Right_Hip_Yaw for dribbling rewards
  └─ (All other rewards are shared with Go1)

Isaac Gym Simulation:
  ├─ Creates K1 body with all parts from URDF
  ├─ Sets up collision between left/right feet and ball
  ├─ Initializes physics engine
  └─ Ready for stepping!
```

---

## Key Lines of Code (What Actually Does the Work)

### Line 1: Import the environment
```python
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv
```
👆 This imports the K1-specific wrapper

### Line 2: Configure K1
```python
from dribblebot.envs.k1.k1_config import config_k1
config_k1(Cfg)
```
👆 This loads K1-specific parameters

### Line 3: Identify as K1
```python
Cfg.robot.name = "k1"
```
👆 **THIS IS THE KEY LINE** - tells system to use K1 class and K1SoccerRewards

### Line 4: Create environment
```python
env = K1VelocityTrackingEasyEnv("cuda:0", False, 1, Cfg)
```
👆 This instantiates and initializes the K1 environment

### Line 5: Run!
```python
obs, rewards, dones, info = env.step(actions)
```
👆 Step the simulation one timestep

---

## What Each File Does

| File | Purpose | Key Content |
|------|---------|------------|
| `dribblebot/robots/k1.py` | Load K1 URDF | Path to K1 URDF file, asset options |
| `dribblebot/envs/k1/k1_config.py` | K1 parameters | Joint angles, control stiffness, body names |
| `dribblebot/envs/k1/velocity_tracking/__init__.py` | K1 environment | K1VelocityTrackingEasyEnv class (thin wrapper) |
| `dribblebot/rewards/k1_soccer_rewards.py` | K1 rewards | Dribbling reward logic using K1 bodies |
| `dribblebot/envs/base/legged_robot.py` | Physics engine | Main simulation loop, body indexing, physics |
| `resources/robots/k1/urdf/k1.urdf` | Robot model | K1 geometry, joints, inertia |

---

## Decision Tree: Which Method Should I Use?

```
START
  │
  ├─ "I just want to verify K1 works"
  │  └─→ Use Method 2 (One-liner)
  │      Takes 10 seconds
  │
  ├─ "I want to see K1 move around"
  │  └─→ Use Method 1 (Minimal script)
  │      Takes 30 seconds
  │
  ├─ "I want to visualize K1 with smooth motion"
  │  └─→ Use Method 3 (Play script)
  │      Takes 1 minute
  │
  ├─ "I want to train a policy"
  │  └─→ Use Method 4 (Training script)
  │      Takes hours/days
  │
  └─ "I want to explore and experiment"
     └─→ Use Method 5 (Interactive Python)
         Takes 1 minute setup

END
```

---

## Differences from Go1 (One Page Summary)

| Aspect | Go1 | K1 |
|--------|-----|-----|
| Import | `from dribblebot.envs.go1.velocity_tracking import VelocityTrackingEasyEnv` | `from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv` |
| Config | `from dribblebot.envs.go1.go1_config import config_go1` | `from dribblebot.envs.k1.k1_config import config_k1` |
| Robot Name | `Cfg.robot.name = "go1"` | `Cfg.robot.name = "k1"` |
| URDF Path | `go1/urdf/go1.urdf` | `k1/urdf/k1.urdf` |
| Foot Name | `"foot"` | `"foot_link"` |
| Dribble Body | `FR_thigh_shoulder` | `Right_Hip_Yaw` |
| Rewards | Auto-selects `Go1SoccerRewards` | Auto-selects `K1SoccerRewards` |
| Number of Legs | 4 (FL, FR, RL, RR) | 2 (Left, Right) |
| DOF per Leg | 3 (hip, thigh, calf) | 6 (Hip_Pitch/Roll/Yaw, Knee, Ankle_Pitch/Roll) |

**Everything else is identical!** Physics, rewards, training, etc.

---

## Quick Status Check Commands

```bash
# Verify K1 files exist
ls -la dribblebot/robots/k1.py
ls -la dribblebot/envs/k1/k1_config.py
ls -la dribblebot/envs/k1/velocity_tracking/__init__.py
ls -la dribblebot/rewards/k1_soccer_rewards.py
ls -la resources/robots/k1/urdf/k1.urdf

# All should show files exist (no "cannot access" errors)
```

---

## Running on Different Hardware

```python
# On GPU (fastest)
env = K1VelocityTrackingEasyEnv("cuda:0", False, 1000, Cfg)

# On CPU (slower)
env = K1VelocityTrackingEasyEnv("cpu", False, 4, Cfg)

# Multiple GPUs
env = K1VelocityTrackingEasyEnv("cuda:1", False, 500, Cfg)
```

---

## Final Checklist

Before running K1:
- [ ] Isaac Gym installed: `python -c "import isaacgym"`
- [ ] PyTorch installed: `python -c "import torch"`
- [ ] K1 files exist: `ls dribblebot/robots/k1.py`
- [ ] K1 URDF exists: `ls resources/robots/k1/urdf/k1.urdf`
- [ ] CUDA available: `nvidia-smi` (or use CPU if not)

Then run:
```bash
python minimal_k1_example.py
```

Expected output:
```
============================================================
K1 in Isaac Gym - Minimal Example
============================================================

[1] Loading K1 configuration...
    ✓ K1 robot name set
    ✓ Using 1 parallel environment(s)

[2] Creating K1 Isaac Gym environment...
    ✓ Environment created
    ✓ Number of actions: 12
    ✓ Observation size: torch.Size([1, 42])

[3] Resetting environment...
    ✓ Environment reset
    ✓ Initial observation shape: torch.Size([1, 42])

[4] Running 50 simulation steps...
    (Use CTRL+C to exit)
    Step  0 | Reward:    0.234 | Obs norm:  1.234
    Step 10 | Reward:   -0.123 | Obs norm:  1.567
    ...

============================================================
✓ SUCCESS! K1 is running in Isaac Gym!
============================================================
```

---

**You're ready! 🚀**

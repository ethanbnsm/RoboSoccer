# 5 Ways to Pull Up K1 in Isaac Gym

## Quick Reference

| Method | Use Case | Complexity |
|--------|----------|-----------|
| **1. Minimal Script** | Testing/Debugging | ⭐ Easiest |
| **2. Python One-Liner** | Quick verification | ⭐ Easy |
| **3. Play Script** | Visualization/Inference | ⭐⭐ Medium |
| **4. Training Script** | Full training pipeline | ⭐⭐⭐ Advanced |
| **5. Interactive Python** | Exploration/Learning | ⭐⭐ Medium |

---

## 1️⃣ Minimal Script (RECOMMENDED FOR FIRST TIME)

**File**: `minimal_k1_example.py` (already created in repo)

**How to run**:
```bash
cd /home/armaan/RoboSoccer
python minimal_k1_example.py
```

**What it does**:
- Loads K1 in Isaac Gym
- Runs 50 simulation steps
- Shows rewards and observations
- Exits gracefully

**Code**:
```python
import isaacgym
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv
import torch

config_k1(Cfg)
Cfg.robot.name = "k1"
env = K1VelocityTrackingEasyEnv("cuda:0", False, Cfg.env.num_envs, Cfg)
obs = env.reset()

for i in range(50):
    actions = torch.randn(1, env.num_actions, device="cuda:0")
    obs, rewards, dones, info = env.step(actions)
    print(f"Step {i}: Reward = {rewards[0].item():.3f}")
```

---

## 2️⃣ Python One-Liner (FASTEST)

**How to run**:
```bash
cd /home/armaan/RoboSoccer
python -c "
import isaacgym, torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv
config_k1(Cfg); Cfg.robot.name='k1'
env = K1VelocityTrackingEasyEnv('cuda:0', False, 1, Cfg)
obs = env.reset()
[env.step(torch.randn(1, env.num_actions, device='cuda:0')) for _ in range(10)]
print('K1 loaded!')
"
```

**What it does**:
- Verifies K1 loads without errors
- Takes 10 steps
- Exits

**Why use it**: Quick verification that setup is correct

---

## 3️⃣ Play Script (FOR VISUALIZATION)

**File**: Create `scripts/play_dribbling_k1.py`

```python
import isaacgym
import torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

def play_k1(headless=False):
    """Play K1 dribbling without a policy (random actions)."""
    
    # Configure K1
    config_k1(Cfg)
    Cfg.robot.name = "k1"
    
    # Turn off domain randomization for clean visualization
    Cfg.domain_rand.push_robots = False
    Cfg.domain_rand.randomize_friction = False
    Cfg.domain_rand.randomize_gravity = False
    
    # Create environment
    env = K1VelocityTrackingEasyEnv(
        sim_device="cuda:0",
        headless=headless,
        num_envs=4,
        cfg=Cfg
    )
    
    obs = env.reset()
    
    # Run simulation
    for i in range(500):
        # Random smooth actions
        actions = 0.1 * torch.sin(torch.tensor([i * 0.1]))
        actions = actions.repeat(4, 12).to("cuda:0")
        
        obs, rewards, dones, info = env.step(actions)
        
        if i % 50 == 0:
            print(f"Step {i}: Reward = {rewards.mean().item():.3f}")

if __name__ == "__main__":
    play_k1(headless=False)
```

**How to run**:
```bash
python scripts/play_dribbling_k1.py
```

**What it does**:
- Loads K1 with 4 parallel environments
- Applies smooth sinusoidal control inputs
- Visualizes K1 dribbling behavior
- Prints rewards

---

## 4️⃣ Full Training Script (FOR PPO TRAINING)

**File**: Create `scripts/train_dribbling_k1.py`

```python
def train_k1(headless=True):
    import isaacgym
    assert isaacgym
    
    import torch
    from dribblebot.envs.base.legged_robot_config import Cfg
    from dribblebot.envs.k1.k1_config import config_k1
    from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv
    from dribblebot_learn.ppo_cse import Runner
    from dribblebot.envs.wrappers.history_wrapper import HistoryWrapper
    from dribblebot_learn.ppo_cse import RunnerArgs

    # Configure K1
    config_k1(Cfg)
    Cfg.env.num_envs = 1000  # Large batch for training
    Cfg.robot.name = "k1"
    
    # Set up sensors for learning
    Cfg.sensors.sensor_names = [
        "ObjectSensor",
        "OrientationSensor",
        "RCSensor",
        "JointPositionSensor",
        "JointVelocitySensor",
        "ActionSensor",
        "LastActionSensor",
        "ClockSensor",
        "YawSensor",
        "TimingSensor",
    ]
    
    Cfg.sensors.privileged_sensor_names = {
        "BodyVelocitySensor": {},
        "ObjectVelocitySensor": {},
    }

    # Create environment
    env = K1VelocityTrackingEasyEnv(
        sim_device="cuda:0",
        headless=headless,
        cfg=Cfg
    )
    
    # Wrap for learning
    env = HistoryWrapper(env)

    # Configure training
    RunnerArgs.max_iterations = 5000
    RunnerArgs.resume = False

    # Train
    runner = Runner(env, device="cuda:0")
    runner.learn(num_learning_iterations=RunnerArgs.max_iterations)

if __name__ == "__main__":
    train_k1(headless=True)
```

**How to run**:
```bash
python scripts/train_dribbling_k1.py
```

**What it does**:
- Creates 1000 parallel K1 environments
- Runs PPO algorithm
- Saves checkpoint every N iterations
- Trains for 5000 iterations

---

## 5️⃣ Interactive Python (FOR EXPLORATION)

**How to run**:
```bash
cd /home/armaan/RoboSoccer
python3
```

**Then in Python REPL**:
```python
# Import and setup
import isaacgym
import torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

# Configure
config_k1(Cfg)
Cfg.robot.name = "k1"
Cfg.env.num_envs = 2

# Create
env = K1VelocityTrackingEasyEnv("cuda:0", False, Cfg.env.num_envs, Cfg)

# Reset
obs = env.reset()
print(f"Observation shape: {obs.shape}")
print(f"K1 loaded with {Cfg.env.num_envs} environments!")

# Try one step
actions = torch.zeros(Cfg.env.num_envs, env.num_actions, device="cuda:0")
obs, rewards, dones, info = env.step(actions)
print(f"Step complete! Reward: {rewards}")

# Explore info
print(f"\nInfo keys: {info.keys()}")
print(f"Joint positions shape: {info['joint_pos'].shape}")
print(f"Contact states shape: {info['contact_states'].shape}")
```

**What you can do**:
- Step through simulation manually
- Inspect observations/rewards
- Test different action sequences
- Debug configuration issues

---

## Comparison Table

| Aspect | Method 1 | Method 2 | Method 3 | Method 4 | Method 5 |
|--------|----------|----------|----------|----------|----------|
| **Setup time** | 30s | 10s | 1m | 2m | 1m |
| **Visualization** | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ⚙️ Optional |
| **Learning** | ❌ | ❌ | ❌ | ✅ | ⚙️ Manual |
| **Debugging** | ✅ Good | ✅ Best | ✅ Good | ❌ Hard | ✅ Best |
| **Production** | ❌ | ❌ | ⚙️ Maybe | ✅ Yes | ❌ |

---

## Next: What to Do After K1 Loads

### Option A: Train a policy
```bash
python scripts/train_dribbling_k1.py
```

### Option B: Test with a pretrained policy
```bash
# First train a policy, then:
python scripts/play_dribbling_k1.py
```

### Option C: Deploy to real K1
```python
# Load trained checkpoint
policy = torch.jit.load("path/to/body.jit")

# Convert observations to network input
obs_dict = get_k1_observations()

# Get action from policy
with torch.no_grad():
    action = policy(obs_dict)

# Send to K1 robot hardware
k1_robot.send_target_positions(action)
```

---

## Troubleshooting

### Q: "CUDA out of memory"
**A**: Reduce `Cfg.env.num_envs` (e.g., from 1000 to 100)

### Q: "K1 not found in robot_classes"
**A**: Ensure `Cfg.robot.name = "k1"` is set BEFORE creating environment

### Q: "left_foot_link not found"
**A**: K1 URDF must contain this body name (it does ✓)

### Q: Window doesn't show up
**A**: Set `headless=False` and ensure X11 is available

### Q: Simulation is slow
**A**: Set `headless=True` to disable rendering

---

## Summary

**For your first time, use Method 1 (Minimal Script)**:
```bash
python minimal_k1_example.py
```

Then pick the method that matches your use case:
- **Testing**: Method 2 or 5
- **Visualization**: Method 3  
- **Training**: Method 4

All methods use the same underlying K1 configuration and environment! 🎉

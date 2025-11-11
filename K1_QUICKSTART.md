# How to Pull Up K1 in Isaac Gym

Based on the RoboSoccer codebase structure, here are the different ways to instantiate K1:

## Method 1: Simple K1 Environment (Fastest for Testing)

```python
import isaacgym
assert isaacgym

import torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

# Step 1: Create and configure Cfg
Cfg = Cfg()
config_k1(Cfg)

# Step 2: Set robot name
Cfg.robot.name = "k1"

# Step 3: Adjust simulation parameters (optional)
Cfg.env.num_envs = 4  # number of parallel environments
Cfg.sim.physics_engine = "SIM_PHYSX"

# Step 4: Create environment
env = K1VelocityTrackingEasyEnv(
    sim_device="cuda:0",
    headless=False,  # Set to True to run without rendering
    num_envs=Cfg.env.num_envs,
    cfg=Cfg
)

# Step 5: Run simulation
obs = env.reset()
for step in range(1000):
    # Random actions for demo
    actions = torch.randn(Cfg.env.num_envs, env.num_actions, device="cuda:0")
    obs, rewards, resets, info = env.step(actions)
    
    if step % 100 == 0:
        print(f"Step {step}, Reward: {rewards.mean().item():.2f}")
```

## Method 2: With Sensors and Wrappers (For Training)

```python
import isaacgym
assert isaacgym

import torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv
from dribblebot.envs.wrappers.history_wrapper import HistoryWrapper

# Configure
config_k1(Cfg)
Cfg.robot.name = "k1"
Cfg.env.num_envs = 1000

# Set up sensors
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
    headless=True,
    cfg=Cfg
)

# Wrap with history (for neural network input)
env = HistoryWrapper(env)

# Now ready for training
obs = env.reset()
print(f"Observation shape: {obs.shape}")
```

## Method 3: Direct from Play Script Pattern

```python
import isaacgym
import torch
import glob
import yaml

from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

def create_k1_env(headless=False):
    """Create a K1 environment following the play script pattern."""
    
    # Initialize config
    config_k1(Cfg)
    
    # Turn off domain randomization for evaluation
    Cfg.domain_rand.push_robots = False
    Cfg.domain_rand.randomize_friction = False
    Cfg.domain_rand.randomize_gravity = False
    Cfg.domain_rand.randomize_restitution = False
    Cfg.domain_rand.randomize_motor_offset = False
    Cfg.domain_rand.randomize_motor_strength = False
    
    # Set robot
    Cfg.robot.name = "k1"
    
    # Create environment
    env = K1VelocityTrackingEasyEnv(
        sim_device="cuda:0",
        headless=headless,
        num_envs=4,
        cfg=Cfg
    )
    
    return env

# Usage
env = create_k1_env(headless=False)
obs = env.reset()

# Step and visualize
for i in range(100):
    actions = torch.zeros(4, env.num_actions, device="cuda:0")
    obs, rewards, dones, info = env.step(actions)
```

## Method 4: Full Training Script (For Train Job)

Create `scripts/train_dribbling_k1.py`:

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
    from dribblebot_learn.ppo_cse.actor_critic import AC_Args
    from dribblebot_learn.ppo_cse.ppo import PPO_Args
    from dribblebot_learn.ppo_cse import RunnerArgs

    # Configure K1
    config_k1(Cfg)
    Cfg.env.num_envs = 1000
    Cfg.robot.name = "k1"

    # Set up sensors
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
    
    # Wrap with history for neural network
    env = HistoryWrapper(env)

    # Configure PPO trainer
    RunnerArgs.resume = False  # Set to True to continue training
    RunnerArgs.max_iterations = 1000

    # Create runner and train
    runner = Runner(env, device="cuda:0")
    runner.learn(num_learning_iterations=RunnerArgs.max_iterations)

if __name__ == "__main__":
    train_k1(headless=True)
```

Then run with:
```bash
python scripts/train_dribbling_k1.py
```

## Key Differences: K1 vs Go1

The main changes when switching from Go1 to K1:

| Step | Go1 | K1 |
|------|-----|-----|
| Import config | `from dribblebot.envs.go1.go1_config import config_go1` | `from dribblebot.envs.k1.k1_config import config_k1` |
| Call config | `config_go1(Cfg)` | `config_k1(Cfg)` |
| Import env | `from dribblebot.envs.go1.velocity_tracking import VelocityTrackingEasyEnv` | `from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv` |
| Create env | `VelocityTrackingEasyEnv(...)` | `K1VelocityTrackingEasyEnv(...)` |
| Set robot name | `Cfg.robot.name = "go1"` | `Cfg.robot.name = "k1"` |
| Rewards | Uses `Go1SoccerRewards` (auto-selected) | Uses `K1SoccerRewards` (auto-selected) |

## What Happens Automatically

When you set `Cfg.robot.name = "k1"`, the following happens automatically:

1. **Robot Loading**: `dribblebot/robots/k1.py` → loads K1 URDF from `resources/robots/k1/urdf/k1.urdf`
2. **Body Mapping**: Uses K1 body names (`left_foot_link`, `right_foot_link`, `Left_Shank`, `Right_Shank`, `Trunk`)
3. **Rewards**: Automatically selects `K1SoccerRewards` which uses `Right_Hip_Yaw` for dribbling rewards
4. **Physics**: Uses K1 joint limits and control parameters from `k1_config.py`
5. **Visualization**: Renders K1 meshes from `resources/robots/k1/meshes/`

## Quick Start Commands

```bash
# Install dependencies (if not done)
cd /home/armaan/RoboSoccer
pip install -e .

# Option 1: Python script
python -c "
import isaacgym, torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

config_k1(Cfg)
Cfg.robot.name = 'k1'
env = K1VelocityTrackingEasyEnv('cuda:0', False, 4, Cfg)
obs = env.reset()
print('K1 loaded successfully!')
"

# Option 2: Create a simple test script
cat > test_k1.py << 'EOF'
import isaacgym, torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

config_k1(Cfg)
Cfg.robot.name = "k1"
Cfg.env.num_envs = 1

env = K1VelocityTrackingEasyEnv("cuda:0", False, Cfg.env.num_envs, Cfg)
obs = env.reset()

for i in range(10):
    actions = torch.randn(1, env.num_actions, device="cuda:0")
    obs, rewards, dones, info = env.step(actions)
    print(f"Step {i}: Reward = {rewards[0].item():.3f}")

print("Success! K1 is running in Isaac Gym")
EOF

python test_k1.py
```

## Troubleshooting

**Error: "K1 not found in robot_classes"**
- Ensure `cfg.robot.name = "k1"` is set BEFORE creating environment

**Error: "left_foot_link not found"**
- Check that K1 URDF contains `left_foot_link` and `right_foot_link` ✓ (Already verified!)

**Error: "K1SoccerRewards is not defined"**
- Ensure `dribblebot/rewards/k1_soccer_rewards.py` exists ✓ (Already created!)

**Visualization not showing**
- Set `headless=False` when creating environment
- Ensure CUDA is available: `torch.cuda.is_available()`

## Next Steps

1. **Verify K1 loads**: Run the quick start command above
2. **Train K1 policy**: Use Method 4 (Full Training Script)
3. **Evaluate K1**: Use Method 3 (Play Script Pattern)
4. **Deploy on real K1**: Use the trained policy checkpoint

All the infrastructure is in place. You're ready to go! 🚀

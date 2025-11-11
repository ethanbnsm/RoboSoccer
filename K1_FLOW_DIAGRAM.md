# K1 Isaac Gym Flow Diagram

## Code Execution Flow: From Script to Simulation

```
┌─────────────────────────────────────────────────────────────────┐
│ Your Script/Training Code                                        │
│                                                                   │
│  from dribblebot.envs.k1.k1_config import config_k1             │
│  from dribblebot.envs.k1.velocity_tracking import               │
│      K1VelocityTrackingEasyEnv                                  │
│                                                                   │
│  config_k1(Cfg)              ← Loads K1-specific config         │
│  Cfg.robot.name = "k1"       ← Flag to use K1                   │
│  env = K1VelocityTrackingEasyEnv(...) ← Creates env             │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ K1VelocityTrackingEasyEnv.__init__()                             │
│ (dribblebot/envs/k1/velocity_tracking/__init__.py)              │
│                                                                   │
│  super().__init__(cfg, ...)  ← Call LeggedRobot base class      │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ LeggedRobot.__init__()                                            │
│ (dribblebot/envs/base/legged_robot.py)                          │
│                                                                   │
│  ┌─ _create_envs()                                               │
│  │                                                               │
│  └─→ robot_classes = {                                          │
│       'go1': Go1,                                              │
│       'k1': K1,      ← K1 registered here!                      │
│      }                                                           │
│                                                                   │
│      robot = robot_classes[cfg.robot.name](self)  ← Creates K1  │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ K1.__init__() then K1.initialize()                               │
│ (dribblebot/robots/k1.py)                                        │
│                                                                   │
│  asset_file = "resources/robots/k1/urdf/k1.urdf"               │
│  asset = gym.load_asset(asset_root, asset_file, options)       │
│                                                                   │
│  Returns: asset, dof_props_asset, rigid_shape_props_asset       │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │ Isaac Gym Simulator    │
        │                        │
        │ Loads K1 URDF from:    │
        │ resources/robots/k1/   │
        │  urdf/k1.urdf          │
        │                        │
        │ Bodies created:        │
        │ ✓ Trunk                │
        │ ✓ Left_Hip_*           │
        │ ✓ Right_Hip_*          │
        │ ✓ Left_Shank           │
        │ ✓ Right_Shank          │
        │ ✓ left_foot_link       │
        │ ✓ right_foot_link      │
        │ ✓ (head, arms, etc)    │
        │                        │
        │ Physics running! ✓     │
        └────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ Back to LeggedRobot._create_envs() (continued)                  │
│                                                                   │
│  ┌─ Find body indices:                                           │
│  │   feet_names = [bodies with "foot_link"]                    │
│  │            → ["left_foot_link", "right_foot_link"]          │
│  │                                                               │
│  │   penalized_contact_names = [bodies with "Shank"]           │
│  │                → ["Left_Shank", "Right_Shank"]              │
│  │                                                               │
│  │   termination_contact_names = [bodies with "Trunk"]         │
│  │                -> ["Trunk"]                                  │
│  │                                                               │
│  └─ Store as tensors: self.feet_indices, etc.                   │
│                                                                   │
│  ┌─ _prepare_reward_function()                                  │
│  │                                                               │
│  └─→ if cfg.robot.name == "k1":                                │
│       reward_container = K1SoccerRewards(self)                 │
│                                                                   │
│      (K1SoccerRewards uses Right_Hip_Yaw for dribbling)        │
│                                                                   │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ Simulation Ready!                                                │
│                                                                   │
│ Your code can now:                                               │
│  • obs = env.reset()                                             │
│  • obs, rew, done, info = env.step(actions)                     │
│  • Access K1 state: obs, dof_pos, contact_forces, etc.          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## File Dependency Graph: How K1 Gets Loaded

```
Your Script
    │
    ├─→ config_k1(Cfg)
    │        │
    │        └─→ dribblebot/envs/k1/k1_config.py
    │                ├─ default_joint_angles (K1-specific)
    │                ├─ control parameters (stiffness, damping)
    │                ├─ foot_name = "foot_link"
    │                ├─ penalize_contacts_on = ["Shank"]
    │                ├─ terminate_after_contacts_on = ["Trunk"]
    │                └─ URDF path = "resources/robots/k1/urdf/k1.urdf"
    │
    ├─→ K1VelocityTrackingEasyEnv(cfg)
    │        │
    │        └─→ LeggedRobot.__init__(cfg)
    │                │
    │                ├─→ _create_envs()
    │                │    │
    │                │    ├─→ robot_classes['k1'] = K1
    │                │    │    │
    │                │    │    └─→ dribblebot/robots/k1.py
    │                │    │            │
    │                │    │            └─→ Load URDF
    │                │    │                ├─ resources/robots/k1/urdf/k1.urdf
    │                │    │                ├─ resources/robots/k1/meshes/*
    │                │    │                └─ Isaac Gym creates physics
    │                │    │
    │                │    ├─→ Find body indices using URDF body names
    │                │    │    ├─ feet_indices → left_foot_link, right_foot_link
    │                │    │    ├─ penalized_contact_indices → Left_Shank, Right_Shank
    │                │    │    └─ termination_contact_indices → Trunk
    │                │    │
    │                │    └─→ Add all rigid bodies, joints, collisions to sim
    │                │
    │                ├─→ _prepare_reward_function()
    │                │    │
    │                │    ├─ Check: cfg.robot.name == "k1" ✓
    │                │    │
    │                │    └─→ reward_container = K1SoccerRewards(self)
    │                │            │
    │                │            └─→ dribblebot/rewards/k1_soccer_rewards.py
    │                │                    ├─ Inherits from SoccerRewards
    │                │                    ├─ _reward_dribbling_robot_ball_vel()
    │                │                    │   └─ Uses Right_Hip_Yaw body
    │                │                    └─ _reward_dribbling_robot_ball_pos()
    │                │                        └─ Uses Right_Hip_Yaw body
    │                │
    │                └─→ _setup_sensors()
    │                     └─ Attach all sensor plugins
    │
    └─→ env.reset()
         └─ Ready for stepping!
```

## Data Flow: One Simulation Step

```
┌──────────────────────────────────────────────────────────────────┐
│ env.step(actions)                                                │
│ ▲                                                                │
│ │ Returns: obs, rewards, dones, info                            │
└──────────────────────────────────────────────────────────────────┘
                     │
                     │ action shape: [num_envs, 12]
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│ LeggedRobot.step() → Apply PD control to K1 joints              │
│                                                                   │
│  For each of 12 DOFs:                                            │
│   target_pos = actions * action_scale                           │
│   force = Kp * (target_pos - current_pos) +                     │
│           Kd * (0 - current_vel)                                │
│                                                                   │
│  Send forces to Isaac Gym physics engine                        │
└──────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│ Isaac Gym Simulation Step                                        │
│                                                                   │
│  1. Update joint forces (from PD controller)                     │
│  2. Simulate K1 physics (inertia, collisions, contacts)         │
│  3. Update body positions/velocities                            │
│  4. Compute contact forces at feet                              │
│  5. Update ball physics                                         │
│  6. Advance time: t += dt                                       │
└──────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│ K1VelocityTrackingEasyEnv.step() → Extract observations         │
│                                                                   │
│  observations = [                                                │
│    joint positions (from dof_pos),                              │
│    joint velocities (from dof_vel),                             │
│    body orientation (from base_quat),                           │
│    base linear velocity (from base_lin_vel),                    │
│    body angular velocity (from base_ang_vel),                   │
│    contact states (from contact_forces at feet),                │
│    ball position (from object state),                           │
│    ball velocity (from object velocity),                        │
│    ... (other sensors)                                          │
│  ]                                                               │
└──────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│ Compute Rewards                                                  │
│                                                                   │
│  K1SoccerRewards calculates:                                     │
│  ✓ Dribbling rewards (using Right_Hip_Yaw)                      │
│  ✓ Ball velocity tracking reward                                │
│  ✓ Balance penalty                                              │
│  ✓ Contact penalties                                            │
│  ✓ (all other robot-agnostic rewards)                           │
│                                                                   │
│  reward = sum of weighted reward components                     │
└──────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│ Return to your script                                            │
│                                                                   │
│  obs:     observation tensor [num_envs, obs_dim]                │
│  rewards: reward tensor [num_envs]                              │
│  dones:   reset flags [num_envs]                                │
│  info:    extra info dict (joint states, contacts, etc)         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Key Configuration Mappings: K1 ↔ Isaac Gym

| Config Setting | What It Does | K1 Value |
|---|---|---|
| `cfg.robot.name` | Which robot class to instantiate | `"k1"` |
| `cfg.asset.file` | Which URDF file to load | `"resources/robots/k1/urdf/k1.urdf"` |
| `cfg.asset.foot_name` | Which bodies are feet (for contact tracking) | `"foot_link"` → finds `left_foot_link`, `right_foot_link` |
| `cfg.asset.penalize_contacts_on` | Which bodies to penalize collision on | `["Shank"]` → penalizes `Left_Shank`, `Right_Shank` collisions |
| `cfg.asset.terminate_after_contacts_on` | Which bodies trigger reset on collision | `["Trunk"]` → resets if `Trunk` hits ground |
| `cfg.init_state.default_joint_angles` | Starting position for each joint | K1-specific angles for each Hip/Knee/Ankle joint |
| `cfg.control.stiffness['joint']` | PD controller proportional gain | `30.0` N·m/rad |
| `cfg.control.damping['joint']` | PD controller derivative gain | `1.0` N·m·s/rad |
| `cfg.control.action_scale` | Scale factor for action input | `0.25` |

## What Makes K1 Different From Go1

```
Go1 Configuration:
├─ asset.file = "resources/robots/go1/urdf/go1.urdf"
├─ asset.foot_name = "foot"
├─ Reward body reference: FR_thigh_shoulder
├─ K1SoccerRewards:
│   └─ Uses Go1SoccerRewards
│   └─ _reward_dribbling_* use FR_thigh_shoulder
└─ Legs: 4 legs (FL, FR, RL, RR)

K1 Configuration:
├─ asset.file = "resources/robots/k1/urdf/k1.urdf"
├─ asset.foot_name = "foot_link"
├─ Reward body reference: Right_Hip_Yaw
├─ Automatically selects K1SoccerRewards:
│   └─ Uses K1SoccerRewards
│   └─ _reward_dribbling_* use Right_Hip_Yaw
└─ Legs: 2 legs (Left, Right) with 6 DOF each
```

Everything else (physics, sim parameters, domain randomization, etc.) is shared!

# Soccer Rewards Architecture - Robot-Specific Implementation

## Overview
The reward system has been refactored to support multiple robots (Go1 and K1) while maintaining backward compatibility with the existing Go1 pipeline.

## Architecture

```
dribblebot/rewards/
├── rewards.py                 (base Rewards class - unchanged)
├── soccer_rewards.py          (base SoccerRewards class with robot-agnostic rewards)
├── go1_soccer_rewards.py      (Go1-specific implementations)
└── k1_soccer_rewards.py       (K1-specific implementations)
```

## File Changes

### 1. `soccer_rewards.py` (Base Class)
**Status**: Modified

**Changes**:
- Kept all robot-agnostic reward methods:
  - `_reward_orientation()`
  - `_reward_torques()`
  - `_reward_dof_vel()`
  - `_reward_dof_acc()`
  - `_reward_collision()`
  - `_reward_action_rate()`
  - `_reward_tracking_contacts_shaped_force()`
  - `_reward_tracking_contacts_shaped_vel()`
  - `_reward_dof_pos_limits()`
  - `_reward_dof_pos()`
  - `_reward_action_smoothness_1()`
  - `_reward_action_smoothness_2()`
  - `_reward_dribbling_ball_vel()`
  - `_reward_dribbling_robot_ball_yaw()`
  - `_reward_dribbling_ball_vel_norm()`
  - `_reward_dribbling_ball_vel_angle()`

- Made robot-specific methods abstract (raise `NotImplementedError`):
  - `_reward_dribbling_robot_ball_vel()` - NOW ABSTRACT
  - `_reward_dribbling_robot_ball_pos()` - NOW ABSTRACT

**Why**:
- These two methods reference hardcoded body names that differ between robots
- Go1 uses `"FR_thigh_shoulder"` as reference point
- K1 uses `"Right_Hip_Yaw"` as reference point

### 2. `go1_soccer_rewards.py` (New File)
**Status**: Created

**Contains**:
- Class `Go1SoccerRewards(SoccerRewards)` - inherits all base rewards
- Implements:
  - `_reward_dribbling_robot_ball_vel()` - Uses Go1's `"FR_thigh_shoulder"`
  - `_reward_dribbling_robot_ball_pos()` - Uses Go1's `"FR_thigh_shoulder"`

**Why**:
- Contains Go1-specific body name references
- Can be imported and used when training Go1 robots
- Does not affect K1 training

### 3. `k1_soccer_rewards.py` (New File)
**Status**: Created

**Contains**:
- Class `K1SoccerRewards(SoccerRewards)` - inherits all base rewards
- Implements:
  - `_reward_dribbling_robot_ball_vel()` - Uses K1's `"Right_Hip_Yaw"`
  - `_reward_dribbling_robot_ball_pos()` - Uses K1's `"Right_Hip_Yaw"`

**Why**:
- Contains K1-specific body name references
- Can be imported and used when training K1 robots
- Does not affect Go1 training

### 4. `dribblebot/envs/base/legged_robot.py` (Modified)
**Status**: Modified

**Changes** (in `_prepare_reward_function()` method):
- Added imports for both `Go1SoccerRewards` and `K1SoccerRewards`
- Added automatic reward class selection logic:
  ```python
  if self.cfg.rewards.reward_container_name == "SoccerRewards":
      if self.cfg.robot.name == "go1":
          reward_container_cls = Go1SoccerRewards
      elif self.cfg.robot.name == "k1":
          reward_container_cls = K1SoccerRewards
      else:
          reward_container_cls = SoccerRewards
  ```

**Why**:
- Dynamically selects the correct reward implementation based on robot type
- When `cfg.robot.name == "go1"`, uses `Go1SoccerRewards`
- When `cfg.robot.name == "k1"`, uses `K1SoccerRewards`
- Maintains backward compatibility with any custom reward containers

## Usage

### For Go1 Training
No changes needed! The system automatically uses `Go1SoccerRewards` when:
```python
cfg.robot.name = "go1"
cfg.rewards.reward_container_name = "SoccerRewards"  # or not specified (default)
```

### For K1 Training
Simply set:
```python
cfg.robot.name = "k1"
cfg.rewards.reward_container_name = "SoccerRewards"  # or not specified (default)
```

The system will automatically use `K1SoccerRewards` instead.

## Benefits

1. **Robot Isolation**: Go1 and K1 training pipelines are completely isolated
2. **Code Reuse**: ~95% of reward code is shared through base class
3. **Backward Compatible**: Existing Go1 training code works unchanged
4. **Easy to Extend**: Adding a new robot only requires:
   - Creating `<robot>_soccer_rewards.py` with robot-specific implementations
   - Adding it to the import and selection logic in `legged_robot.py`
5. **Maintainability**: Changes to shared rewards only need to be made once in base class

## K1-Specific Implementation Notes

The K1 uses `"Right_Hip_Yaw"` as the reference point instead of Go1's `"FR_thigh_shoulder"` because:
- K1 has a different leg structure (Hip_Pitch, Hip_Roll, Hip_Yaw)
- Hip_Yaw is the last joint before the shank/foot
- This joint is at a similar forward position to Go1's thigh_shoulder reference
- Using this body allows the dribbling logic to work analogously to Go1

## Troubleshooting

If you get an error like "SoccerRewards has no attribute _reward_dribbling_robot_ball_vel":
- Ensure you're using a robot-specific subclass (Go1SoccerRewards or K1SoccerRewards)
- Check that `cfg.robot.name` is set to either "go1" or "k1"
- The base `SoccerRewards` class is now abstract for these methods

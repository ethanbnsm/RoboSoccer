# K1 Quick Reference Card

## 🚀 Launch K1

```bash
# After conda environment is set up
python minimal_k1_example.py
```

Expected output:
```
============================================================
✓ SUCCESS! K1 is running in Isaac Gym!
============================================================
```

---

## 📦 Training Configuration

```python
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv

# Setup
config_k1(Cfg)
Cfg.robot.name = "k1"

# Create environment with 4000 parallel environments
env = K1VelocityTrackingEasyEnv(
    sim_device="cuda:0",
    headless=True,
    num_envs=4000,
    cfg=Cfg
)

# Reset
obs = env.reset()  # Shape: [4000, 65]

# Step
actions = torch.randn(4000, 22)  # 4000 envs, 22 DOF
obs, rewards, dones, extras = env.step(actions)
```

---

## 🤖 K1 Specifications

| Parameter | Value |
|-----------|-------|
| **DOF** | 22 (2 head + 8 arm + 12 leg) |
| **Observation Dim** | 65 |
| **Action Dim** | 22 |
| **Command Dim** | 10 |
| **Control Type** | PD (Proportional-Derivative) |
| **Stiffness** | 30 N·m/rad |
| **Damping** | 1.0 N·m·s/rad |
| **Action Scale** | 0.25 |
| **Physics Dt** | 0.001s |
| **Control Decimation** | 4 (0.004s per action) |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `dribblebot/robots/k1.py` | K1 robot class |
| `dribblebot/envs/k1/k1_config.py` | K1 configuration |
| `dribblebot/envs/k1/velocity_tracking/__init__.py` | Environment wrapper |
| `dribblebot/rewards/k1_soccer_rewards.py` | K1 reward function |
| `resources/robots/k1/urdf/k1.urdf` | K1 URDF model |
| `resources/robots/k1/meshes/` | K1 visual meshes |

---

## 🎯 Observations (65D)

```
[3] Gravity vector (base orientation)
[3] Base angular velocity
[22] Joint positions (one per DOF)
[22] Joint velocities (one per DOF)
[22] Current actions (one per DOF)
[22] Delayed actions (one per DOF)
[2] Clock phase and duty cycle
──────────────
Total: 65 dimensions
```

---

## 📊 Commands (10D)

```
[1] lin_vel_x:        [-0.6,  0.6]  m/s
[1] lin_vel_y:        [-0.6,  0.6]  m/s
[1] ang_vel_yaw:      [-1,    1]    rad/s
[1] body_height:      [0.0,   0.0]  m
[1] gait_frequency:   [2.0,   2.0]  Hz
[1] gait_phase:       [0.0,   0.0]
[1] gait_offset:      [0.0,   0.0]
[1] gait_bound:       [0.0,   0.0]
[1] gait_duration:    [0.5,   0.5]  s
[1] footswing_height: [0.06,  0.06] m
──────────────
Total: 10 dimensions
```

*Note: Gait parameters are minimal for humanoid; mainly velocity commands matter*

---

## 🔧 Common Configuration Changes

### Increase Training Envs
```python
Cfg.env.num_envs = 8000  # Default: 4000
```

### Adjust Velocity Ranges
```python
Cfg.commands.lin_vel_x = [-1.0, 1.0]  # Default: [-0.6, 0.6]
Cfg.commands.lin_vel_y = [-1.0, 1.0]  # Default: [-0.6, 0.6]
Cfg.commands.ang_vel_yaw = [-2, 2]    # Default: [-1, 1]
```

### Modify Reward Weights
```python
Cfg.reward_scales.dribbling_robot_ball_pos = 2.0
Cfg.reward_scales.dribbling_robot_ball_vel = 0.5
Cfg.reward_scales.torques = -0.0002
```

### Change Action Scale
```python
Cfg.control.action_scale = 0.5  # Default: 0.25
```

### Enable Visualization
```python
env = K1VelocityTrackingEasyEnv(
    sim_device="cuda:0",
    headless=False,  # Show GUI
    cfg=Cfg
)
```

---

## 🎓 Training Script

```bash
# Train K1 with default config
python scripts/train_dribbling.py --cfg_name k1

# Train K1 headless (no rendering)
python scripts/train_dribbling.py --cfg_name k1 --headless True

# Train with custom parameters
python scripts/train_dribbling.py \
    --cfg_name k1 \
    --num_envs 8000 \
    --learning_rate 1e-3 \
    --headless True
```

---

## 📚 Documentation

| Document | Content |
|----------|---------|
| `K1_QUICKSTART.md` | Get started in 5 minutes |
| `K1_HOW_TO_RUN.md` | Detailed setup instructions |
| `K1_FLOW_DIAGRAM.md` | Architecture and data flow |
| `K1_CODE_PATH.md` | File structure navigation |
| `K1_CHEAT_SHEET.md` | Common code snippets |
| `K1_FINAL_STATUS.md` | Complete integration summary |
| `K1_RUNTIME_FIX_SUMMARY.md` | Bugs fixed |
| `K1_CHANGELOG.md` | Detailed change log |

---

## ⚠️ Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'isaacgym'`
**Solution:** Initialize conda environment with Isaac Gym installed

### Issue: Mesh loading warnings
**Solution:** Normal - placeholder meshes are used. Physics simulation works fine.

### Issue: Low FPS
**Solution:** 
- Reduce `num_envs` (default 4000)
- Enable `headless=True`
- Reduce rendering frequency

### Issue: K1 falls over
**Solution:**
- Check `default_joint_angles` in config
- Increase `reward_scales.base_height`
- Increase `reward_scales.orientation`

---

## 🔗 Go1 vs K1

| Feature | Go1 | K1 |
|---------|-----|-------|
| **DOF** | 12 (legs only) | 22 (full body) |
| **Body Type** | Quadruped | Humanoid |
| **Dribbling Ref** | FR_thigh_shoulder | Right_Hip_Yaw |
| **Config File** | `go1_config.py` | `k1_config.py` |
| **Reward Class** | `Go1SoccerRewards` | `K1SoccerRewards` |
| **Selection** | `cfg.robot.name="go1"` | `cfg.robot.name="k1"` |

---

## ✅ Verification Checklist

Before training, verify:
- [ ] Isaac Gym environment initialized
- [ ] K1 URDF loads without errors
- [ ] 22 joints detected
- [ ] Observations are 65D
- [ ] Commands are 10D
- [ ] Rewards compute successfully
- [ ] `minimal_k1_example.py` runs

---

## 🎯 Next Steps

1. **Verify Setup:**
   ```bash
   python minimal_k1_example.py
   ```

2. **Check Observations:**
   - Should be 65D tensor
   - 4000 environments (default)

3. **Train Policy:**
   ```bash
   python scripts/train_dribbling.py --cfg_name k1
   ```

4. **Monitor Training:**
   - Open TensorBoard: `tensorboard --logdir runs/`
   - Check rewards in logs
   - Adjust parameters as needed

---

## 📞 Support

For detailed documentation, see:
- Architecture: `K1_FLOW_DIAGRAM.md`
- Code structure: `K1_CODE_PATH.md`
- Problems: `K1_RUNTIME_FIX_SUMMARY.md`
- Full details: `K1_COMPLETE_SUMMARY.md`

---

**K1 Integration Complete** ✅  
Ready for training and deployment!


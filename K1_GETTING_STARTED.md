# Booster K1 Getting Started & Reference

## 🚀 Quick Start

```bash
python minimal_k1_example.py
```
- Loads Booster K1 in Isaac Gym
- Runs 50 simulation steps
- Viewer stays open for demonstration

---

## 📝 Integration Summary
- K1 robot class, URDF, and meshes added
- Configuration, environment wrapper, and reward system implemented
- All runtime, buffer, and mesh errors resolved

---

## 🏗️ Architecture & Code Path
- `minimal_k1_example.py` → loads config → creates K1VelocityTrackingEasyEnv
- Uses LeggedRobot base class, robot_classes registry
- Meshes loaded from `resources/robots/k1/meshes/`
- Rewards selected by robot name

---

## 📦 Features & Specifications
| Parameter         | Value                        |
|-------------------|------------------------------|
| DOF               | 22 (2 head, 8 arm, 12 leg)   |
| Observation Dim   | 65                           |
| Action Dim        | 22                           |
| Command Dim       | 10                           |
| Control Type      | PD (Proportional-Derivative) |
| Stiffness         | 30 N·m/rad                   |
| Damping           | 1.0 N·m·s/rad                |
| Action Scale      | 0.25                         |
| Physics Dt        | 0.001s                       |

---

## 🖥️ How to Run & Visualize
- Run `python minimal_k1_example.py` for a quick demo
- Use viewer controls to rotate, zoom, and pan
- Script pauses at end for classroom presentation

---

## 🛠️ Troubleshooting & Fixes
- Mesh path errors: All mesh references updated
- Buffer/loop errors: Loops robust to robot config
- All critical runtime bugs resolved

---

## 📚 Advanced Usage & Documentation
- For training, visualization, or interactive exploration, see:
  - `K1_QUICKSTART.md` (detailed examples)
  - `K1_CHEAT_SHEET.md` (copy-paste code)
  - `K1_CODE_PATH.md` (file structure)
  - `K1_FLOW_DIAGRAM.md` (architecture)
- For change log and technical details, see:
  - `K1_CHANGELOG.md`
  - `K1_FINAL_STATUS.md`
  - `K1_RUNTIME_FIX_SUMMARY.md`

---

## ✅ Status
- Booster K1 is fully integrated and ready for use in Isaac Gym!
- All code and assets are up to date with this commit.

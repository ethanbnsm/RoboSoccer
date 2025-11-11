#!/usr/bin/env python3
"""
Minimal example to pull up K1 in Isaac Gym
Run with: python minimal_k1_example.py
"""

import isaacgym
assert isaacgym  # Must be first!

import torch
from dribblebot.envs.base.legged_robot_config import Cfg
from dribblebot.envs.k1.k1_config import config_k1
from dribblebot.envs.k1.velocity_tracking import K1VelocityTrackingEasyEnv


def main():
    print("=" * 60)
    print("K1 in Isaac Gym - Minimal Example")
    print("=" * 60)
    
    # Step 1: Configure K1
    print("\n[1] Loading K1 configuration...")
    config_k1(Cfg)
    Cfg.robot.name = "k1"
    Cfg.env.num_envs = 1  # Single environment for testing
    print(f"    ✓ K1 robot name set")
    print(f"    ✓ Using {Cfg.env.num_envs} parallel environment(s)")
    
    # Step 2: Create environment
    print("\n[2] Creating K1 Isaac Gym environment...")
    env = K1VelocityTrackingEasyEnv(
        sim_device="cuda:0",
        headless=False,  # Set to True to run without rendering
        cfg=Cfg
    )
    print(f"    ✓ Environment created")
    print(f"    ✓ Number of actions: {env.num_actions}")
    print(f"    ✓ Observation size: {env.obs_buf.shape}")
    
    # Step 3: Reset environment
    print("\n[3] Resetting environment...")
    obs = env.reset()
    print(f"    ✓ Environment reset")
    print(f"    ✓ Initial observation shape: {obs.shape}")
    
    # Step 4: Run simulation
    print("\n[4] Running 50 simulation steps...")
    print("    (Use CTRL+C to exit)")
    
    try:
        for step in range(50):
            # Create random actions (joint position targets)
            actions = torch.randn(
                Cfg.env.num_envs, 
                env.num_actions, 
                device="cuda:0"
            )
            
            # Step simulation
            obs, rewards, dones, info = env.step(actions)
            
            if step % 10 == 0:
                print(f"    Step {step:3d} | Reward: {rewards[0].item():7.3f} | "
                      f"Obs norm: {obs[0].norm().item():.3f}")
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS! K1 is running in Isaac Gym!")
        print("=" * 60)
        print("\nSimulation complete. Press Enter to close the viewer and exit.")
        input()
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user")


if __name__ == "__main__":
    main()

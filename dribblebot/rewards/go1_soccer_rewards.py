import torch
import numpy as np
from dribblebot.utils.math_utils import quat_apply_yaw, wrap_to_pi, get_scale_shift
from isaacgym.torch_utils import *
from .soccer_rewards import SoccerRewards


class Go1SoccerRewards(SoccerRewards):
    """Go1-specific soccer dribbling rewards.
    
    Inherits all robot-agnostic rewards from SoccerRewards and implements
    Go1-specific dribbling rewards that reference Go1 body names.
    """

    def _reward_dribbling_robot_ball_vel(self):
        """Encourage robot velocity align vector from robot body to ball.
        
        Uses Go1-specific body name: FR_thigh_shoulder
        """
        FR_shoulder_idx = self.env.gym.find_actor_rigid_body_handle(
            self.env.envs[0], self.env.robot_actor_handles[0], "FR_thigh_shoulder"
        )
        FR_HIP_positions = quat_rotate_inverse(
            self.env.base_quat,
            self.env.rigid_body_state.view(self.env.num_envs, -1, 13)[:, FR_shoulder_idx, 0:3].view(
                self.env.num_envs, 3
            )
            - self.env.base_pos,
        )
        FR_HIP_velocities = quat_rotate_inverse(
            self.env.base_quat,
            self.env.rigid_body_state.view(self.env.num_envs, -1, 13)[:, FR_shoulder_idx, 7:10].view(
                self.env.num_envs, 3
            ),
        )

        delta_dribbling_robot_ball_vel = 1.0
        robot_ball_vec = self.env.object_local_pos[:, 0:2] - FR_HIP_positions[:, 0:2]
        d_robot_ball = robot_ball_vec / torch.norm(robot_ball_vec, dim=-1).unsqueeze(dim=-1)
        ball_robot_velocity_projection = torch.norm(
            self.env.commands[:, :2], dim=-1
        ) - torch.sum(d_robot_ball * FR_HIP_velocities[:, 0:2], dim=-1)
        velocity_concatenation = torch.cat(
            (torch.zeros(self.env.num_envs, 1, device=self.env.device), ball_robot_velocity_projection.unsqueeze(dim=-1)),
            dim=-1,
        )
        rew_dribbling_robot_ball_vel = torch.exp(
            -delta_dribbling_robot_ball_vel * torch.pow(torch.max(velocity_concatenation, dim=-1).values, 2)
        )
        return rew_dribbling_robot_ball_vel

    def _reward_dribbling_robot_ball_pos(self):
        """Encourage robot near ball.
        
        Uses Go1-specific body name: FR_thigh_shoulder
        """
        FR_shoulder_idx = self.env.gym.find_actor_rigid_body_handle(
            self.env.envs[0], self.env.robot_actor_handles[0], "FR_thigh_shoulder"
        )
        FR_HIP_positions = quat_rotate_inverse(
            self.env.base_quat,
            self.env.rigid_body_state.view(self.env.num_envs, -1, 13)[:, FR_shoulder_idx, 0:3].view(
                self.env.num_envs, 3
            )
            - self.env.base_pos,
        )

        delta_dribbling_robot_ball_pos = 4.0
        rew_dribbling_robot_ball_pos = torch.exp(
            -delta_dribbling_robot_ball_pos
            * torch.pow(torch.norm(self.env.object_local_pos - FR_HIP_positions, dim=-1), 2)
        )
        return rew_dribbling_robot_ball_pos

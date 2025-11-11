import torch
import numpy as np
from dribblebot.utils.math_utils import quat_apply_yaw, wrap_to_pi, get_scale_shift
from isaacgym.torch_utils import *
from .soccer_rewards import SoccerRewards


class K1SoccerRewards(SoccerRewards):
    """K1-specific soccer dribbling rewards.
    
    Inherits all robot-agnostic rewards from SoccerRewards and implements
    K1-specific dribbling rewards that reference K1 body names.
    """

    def _reward_dribbling_robot_ball_vel(self):
        """Encourage robot velocity align vector from robot body to ball.
        
        Uses K1-specific body name: Right_Hip_Yaw (K1 front-right hip reference point)
        """
        right_hip_idx = self.env.gym.find_actor_rigid_body_handle(
            self.env.envs[0], self.env.robot_actor_handles[0], "Right_Hip_Yaw"
        )
        hip_positions = quat_rotate_inverse(
            self.env.base_quat,
            self.env.rigid_body_state.view(self.env.num_envs, -1, 13)[:, right_hip_idx, 0:3].view(
                self.env.num_envs, 3
            )
            - self.env.base_pos,
        )
        hip_velocities = quat_rotate_inverse(
            self.env.base_quat,
            self.env.rigid_body_state.view(self.env.num_envs, -1, 13)[:, right_hip_idx, 7:10].view(
                self.env.num_envs, 3
            ),
        )

        delta_dribbling_robot_ball_vel = 1.0
        robot_ball_vec = self.env.object_local_pos[:, 0:2] - hip_positions[:, 0:2]
        d_robot_ball = robot_ball_vec / torch.norm(robot_ball_vec, dim=-1).unsqueeze(dim=-1)
        ball_robot_velocity_projection = torch.norm(
            self.env.commands[:, :2], dim=-1
        ) - torch.sum(d_robot_ball * hip_velocities[:, 0:2], dim=-1)
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
        
        Uses K1-specific body name: Right_Hip_Yaw (K1 front-right hip reference point)
        """
        right_hip_idx = self.env.gym.find_actor_rigid_body_handle(
            self.env.envs[0], self.env.robot_actor_handles[0], "Right_Hip_Yaw"
        )
        hip_positions = quat_rotate_inverse(
            self.env.base_quat,
            self.env.rigid_body_state.view(self.env.num_envs, -1, 13)[:, right_hip_idx, 0:3].view(
                self.env.num_envs, 3
            )
            - self.env.base_pos,
        )

        delta_dribbling_robot_ball_pos = 4.0
        rew_dribbling_robot_ball_pos = torch.exp(
            -delta_dribbling_robot_ball_pos
            * torch.pow(torch.norm(self.env.object_local_pos - hip_positions, dim=-1), 2)
        )
        return rew_dribbling_robot_ball_pos

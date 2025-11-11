from typing import Union

from params_proto import Meta

from dribblebot.envs.base.legged_robot_config import Cfg


def config_k1(Cnfg: Union[Cfg, Meta]):
    _ = Cnfg.init_state

    _.pos = [0.0, 0.0, 0.9]  # x,y,z [m]
    _.default_joint_angles = {
        # Head and neck
        "AAHead_yaw": 0.0,
        "Head_pitch": 0.0,
        
        # Left arm
        "ALeft_Shoulder_Pitch": 0.0,
        "Left_Shoulder_Roll": 0.0,
        "Left_Elbow_Pitch": 0.0,
        "Left_Elbow_Yaw": 0.0,
        
        # Right arm
        "ARight_Shoulder_Pitch": 0.0,
        "Right_Shoulder_Roll": 0.0,
        "Right_Elbow_Pitch": 0.0,
        "Right_Elbow_Yaw": 0.0,
        
        # Left leg
        "Left_Hip_Yaw": 0.0,
        "Left_Hip_Roll": 0.0,
        "Left_Hip_Pitch": -0.35,
        "Left_Knee_Pitch": 0.70,
        "Left_Ankle_Pitch": -0.35,
        "Left_Ankle_Roll": 0.0,

        # Right leg
        "Right_Hip_Yaw": 0.0,
        "Right_Hip_Roll": 0.0,
        "Right_Hip_Pitch": -0.35,
        "Right_Knee_Pitch": 0.70,
        "Right_Ankle_Pitch": -0.35,
        "Right_Ankle_Roll": 0.0
}


    _ = Cnfg.control
    _.control_type = 'P'
    _.stiffness = {'joint': 30.}
    _.damping = {'joint': 1.0}
    _.action_scale = 0.25
    _.hip_scale_reduction = 0.5
    # decimation: Number of control action updates @ sim DT per policy DT
    _.decimation = 4

    _ = Cnfg.asset
    _.file = '{MINI_GYM_ROOT_DIR}/resources/robots/k1/urdf/k1.urdf'
    _.foot_name = "foot_link"
    _.penalize_contacts_on = ["Shank"]
    _.terminate_after_contacts_on = ["Trunk"]
    _.self_collisions = 0  # 1 to disable, 0 to enable...bitwise filter
    _.flip_visual_attachments = False
    _.fix_base_link = False

    _ = Cnfg.rewards
    _.soft_dof_pos_limit = 0.9
    _.base_height_target = 0.9


    _ = Cnfg.reward_scales
    _.torques = -0.0001
    _.action_rate = -0.01
    _.dof_pos_limits = -10.0
    _.orientation = -5.
    _.base_height = -30.

    _ = Cnfg.terrain
    _.mesh_type = 'trimesh'
    _.measure_heights = False
    _.terrain_noise_magnitude = 0.0
    _.teleport_robots = True
    _.border_size = 50

    _.terrain_proportions = [0, 0, 0, 0, 0, 0, 0, 0, 1.0]
    _.curriculum = False

    _ = Cnfg.env
    _.num_observations = 65
    _.num_envs = 4000

    _ = Cnfg.commands
    _.num_commands = 10  # lin_vel_x, lin_vel_y, ang_vel_yaw, body_height, freq, phase, offset, bound, duration, footswing_height
    _.lin_vel_x = [-1.0, 1.0]
    _.lin_vel_y = [-1.0, 1.0]

    _ = Cnfg.commands
    _.heading_command = False
    _.resampling_time = 10.0
    _.command_curriculum = True
    _.num_commands = 10
    _.num_lin_vel_bins = 30
    _.num_ang_vel_bins = 30
    _.lin_vel_x = [-0.6, 0.6]
    _.lin_vel_y = [-0.6, 0.6]
    _.ang_vel_yaw = [-1, 1]
    _.body_height_cmd = [0.0, 0.0]
    _.gait_frequency_cmd_range = [2.0, 2.0]
    _.gait_phase_cmd_range = [0.0, 0.0]
    _.gait_offset_cmd_range = [0.0, 0.0]
    _.gait_bound_cmd_range = [0.0, 0.0]
    _.gait_duration_cmd_range = [0.5, 0.5]
    _.footswing_height_range = [0.06, 0.06]
    
    # Curriculum settings
    _.num_bins_vel_x = 30
    _.num_bins_vel_y = 30
    _.num_bins_vel_yaw = 30
    _.num_bins_body_height = 1
    _.num_bins_gait_frequency = 1
    _.num_bins_gait_phase = 1
    _.num_bins_gait_offset = 1
    _.num_bins_gait_bound = 1
    _.num_bins_gait_duration = 1
    _.num_bins_footswing_height = 1
    _.num_bins_body_pitch = 1
    _.num_bins_body_roll = 1
    _.num_bins_aux_reward_coef = 1
    _.num_bins_compliance = 1
    _.num_bins_stance_width = 1
    _.num_bins_stance_length = 1
    
    # For K1, we don't use gaits, so set these to minimal ranges
    _.limit_vel_x = [-0.6, 0.6]
    _.limit_vel_y = [-0.6, 0.6]
    _.limit_vel_yaw = [-1, 1]
    _.limit_body_height = [0.0, 0.0]
    _.limit_gait_phase = [0.0, 0.0]
    _.limit_gait_offset = [0.0, 0.0]
    _.limit_gait_bound = [0.0, 0.0]
    _.limit_gait_frequency = [2.0, 2.0]
    _.limit_gait_duration = [0.5, 0.5]
    _.limit_footswing_height = [0.06, 0.06]
    _.limit_body_pitch = [0.0, 0.0]
    _.limit_body_roll = [0.0, 0.0]
    _.limit_aux_reward_coef = [0.0, 0.0]
    _.limit_compliance = [0.0, 0.0]
    _.limit_stance_width = [0.0, 0.0]
    _.limit_stance_length = [0.0, 0.0]
    _.gaitwise_curricula = False
    _.exclusive_phase_offset = False
    _.balance_gait_distribution = False
    _.binary_phases = False

    _ = Cnfg.domain_rand
    _.randomize_base_mass = True
    _.added_mass_range = [-1, 3]
    _.push_robots = False
    _.max_push_vel_xy = 0.5
    _.randomize_friction = True
    _.friction_range = [0.05, 4.5]
    _.randomize_restitution = True
    _.restitution_range = [0.0, 1.0]
    _.restitution = 0.5  # default terrain restitution
    _.randomize_com_displacement = True
    _.com_displacement_range = [-0.1, 0.1]
    _.randomize_motor_strength = True
    _.motor_strength_range = [0.9, 1.1]
    _.randomize_Kp_factor = False
    _.Kp_factor_range = [0.8, 1.3]
    _.randomize_Kd_factor = False
    _.Kd_factor_range = [0.5, 1.5]
    _.rand_interval_s = 6

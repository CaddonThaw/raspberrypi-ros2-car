-- Copyright 2016 The Cartographer Authors
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER, -- map_builder.lua的配置信息
  trajectory_builder = TRAJECTORY_BUILDER, -- trajectory_builder.lua的配置信息
  map_frame = "map", -- 地图坐标系的名字
  tracking_frame = "base_link", -- 将所有传感器数据转换到这个坐标系，如果有IMU应设为IMU的坐标系，否则设为base_link
  published_frame = "odom", -- tf树的发布坐标系，通常发布 map -> odom 的变换
  odom_frame = "odom", -- 里程计坐标系的名字
  provide_odom_frame = false, -- 是否由Cartographer提供odom_frame，如果已有里程计发布odom -> base_link，则设为false
  publish_frame_projected_to_2d = true, -- 是否发布2D姿态（不包含俯仰角和横滚角）
  use_pose_extrapolator = true, -- 是否使用姿态推测器，用于平滑定位结果
  use_odometry = true, -- 是否订阅里程计话题 /odom
  use_nav_sat = false, -- 是否订阅GPS话题 /fix
  use_landmarks = false, -- 是否订阅路标话题 /landmarks
  num_laser_scans = 1, -- 订阅的激光雷达话题数量（/scan）
  num_multi_echo_laser_scans = 0, -- 订阅的多回波激光雷达话题数量（/echo_scan）
  num_subdivisions_per_laser_scan = 1, -- 将一帧激光雷达数据拆分成多少份处理，1表示不拆分
  num_point_clouds = 0, -- 订阅的3D点云话题数量（/points2）
  lookup_transform_timeout_sec = 0.2, -- 查找tf变换的超时时间
  submap_publish_period_sec = 0.3, -- 发布子地图的时间间隔
  pose_publish_period_sec = 5e-3, -- 发布姿态的时间间隔 (5ms)
  trajectory_publish_period_sec = 30e-3, -- 发布轨迹的时间间隔 (30ms)
  rangefinder_sampling_ratio = 1., -- 激光雷达数据的采样率，1.0表示全部在用
  odometry_sampling_ratio = 1., -- 里程计数据的采样率
  fixed_frame_pose_sampling_ratio = 1., -- 固定坐标系姿态的采样率
  imu_sampling_ratio = 1., -- IMU数据的采样率
  landmarks_sampling_ratio = 1., -- 路标数据的采样率
}

-- MAP_BUILDER.use_trajectory_builder_2d = true
-- TRAJECTORY_BUILDER_2D.num_accumulated_range_data = 10

MAP_BUILDER.use_trajectory_builder_2d = true -- 开启2D SLAM
TRAJECTORY_BUILDER_2D.min_range = 0.10 -- 雷达数据的最小距离，小于该值的点被忽略
TRAJECTORY_BUILDER_2D.max_range = 10 -- 雷达数据的最大距离，大于该值的点被忽略
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 3. -- 如果雷达数据丢失，假定障碍物在这个距离
TRAJECTORY_BUILDER_2D.use_imu_data = false -- 是否使用IMU数据（2D SLAM通常可以不用）
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true -- 是否开启实时相关扫描匹配（CSM），用于解决里程计不准的问题
TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians = math.rad(0.1) -- 运动过滤：角度变化超过该值才插入新数据
POSE_GRAPH.constraint_builder.min_score = 0.65 -- 闭环检测的最低分数阈值
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.7 -- 全局定位的最低分数阈值

return options   
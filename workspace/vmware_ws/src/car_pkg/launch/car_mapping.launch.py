import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
  # 定位到功能包的地址
  pkg_share = FindPackageShare(package='car_pkg').find('car_pkg')
  
  # == 运行小车模型Launch脚本 ==
  car_display = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([
          os.path.join(pkg_share, 'launch', 'car_display.launch.py')
      ])
  )
  
  # == 运行节点需要的配置 ==
  # 是否使用仿真时间
  use_sim_time = LaunchConfiguration('use_sim_time', default='false')
  # 地图的分辨率
  resolution = LaunchConfiguration('resolution', default='0.05')
  # 地图的发布周期
  publish_period_sec = LaunchConfiguration('publish_period_sec', default='1.0')
  # 配置文件夹路径
  configuration_directory = LaunchConfiguration('configuration_directory', 
                                              default=os.path.join(pkg_share, 'config'))
  # 配置文件
  configuration_basename = LaunchConfiguration('configuration_basename', 
                                            default='backpack_2d.lua')
  
  # == 声明三个节点，cartographer/occupancy_grid_node/rviz_node ==
  cartographer_node = Node(
      package='cartographer_ros',
      executable='cartographer_node',
      name='cartographer_node',
      output='screen',
      parameters=[{'use_sim_time': use_sim_time}],
      arguments=['-configuration_directory', configuration_directory,
                  '-configuration_basename', configuration_basename])

  occupancy_grid_node = Node(
      package='cartographer_ros',
      executable='cartographer_occupancy_grid_node',
      name='occupancy_grid_node',
      output='screen',
      parameters=[{'use_sim_time': use_sim_time}],
      arguments=['-resolution', resolution, '-publish_period_sec', publish_period_sec])

  rviz_node = Node(
      package='rviz2',
      executable='rviz2',
      name='rviz2',
      parameters=[{'use_sim_time': use_sim_time}],
      output='screen')

  # == 键盘控制节点，新终端窗口运行 ==
  key_control_node = ExecuteProcess(
      cmd=['gnome-terminal', '--', 'ros2', 'run', 'car_pkg', 'key_control_node'],
      output='screen',
      name='key_control_node'
  )

  # == 启动组合 ==
  ld = LaunchDescription()
  ld.add_action(car_display)
  ld.add_action(cartographer_node)
  ld.add_action(occupancy_grid_node)
  ld.add_action(rviz_node)
  ld.add_action(key_control_node)

  return ld
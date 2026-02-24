import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # == 获取包路径 ==
    pkg_share = FindPackageShare(package='car_pkg').find('car_pkg')
    nav2_bringup_dir = FindPackageShare(package='nav2_bringup').find('nav2_bringup')
    
    # == 配置路径 ==
    # 地图路径 
    map_yaml_path = os.path.join(pkg_share, 'maps', 'map1.yaml')
    # Nav2参数文件路径
    nav2_params_path = os.path.join(pkg_share, 'params', 'nav2_params.yaml')
    # RViz配置文件路径
    rviz_config_dir = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')

    # == 运行小车模型 ==
    car_display = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg_share, 'launch', 'car_display.launch.py')
        ])
    )

    # == 运行 Nav2 Bringup (核心导航功能) ==
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ]),
        launch_arguments={
            'map': map_yaml_path,
            'params_file': nav2_params_path,
            'use_sim_time': 'false', # 实车设置为false
            'autostart': 'true'      # 自动启动生命周期节点
        }.items()
    )

    # == 运行 RViz2 ==
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': False}],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(car_display)
    ld.add_action(nav2_bringup)
    ld.add_action(rviz_node)

    return ld
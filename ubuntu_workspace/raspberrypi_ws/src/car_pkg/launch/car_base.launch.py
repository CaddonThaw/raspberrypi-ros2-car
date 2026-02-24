from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    lidar_dir = get_package_share_directory('cspc_lidar')

    return LaunchDescription([
        # 启动雷达驱动节点
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(lidar_dir, 'launch', 'lidar_launch.py')),
        ),
        # 启动小车底盘节点
        Node(
            package='car_pkg', 
            executable='car_node',  
            name='car_node', 
            output='screen'  
        ),
    ])
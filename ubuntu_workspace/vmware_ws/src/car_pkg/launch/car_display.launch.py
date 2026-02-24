import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 设定需要启动的包名和URDF模型文件名
    package_name = 'car_pkg'
    urdf_name = "car.urdf"

    ld = LaunchDescription()
    
    # 查找指定包的共享目录路径，例如 /home/user/ros2_ws/install/car_pkg/share/car_pkg
    pkg_share = FindPackageShare(package=package_name).find(package_name) 
    
    # 构建URDF文件的完整路径
    urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')

    # 创建 robot_state_publisher 节点
    # 功能：读取URDF文件，并发布 /tf 和 /tf_static 变换树，以及 /robot_description 话题
    # 这是Rviz显示机器人模型的基础，将各个link的相对位置关系广播出去
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_model_path]
        )

    # 创建 joint_state_publisher 节点
    # 功能：负责发布非固定关节（如轮子转动）的状态信息到 /joint_states 话题
    # 因为没有使用 _gui 版本，它主要负责发布默认的关节状态（例如轮子角度为0）
    # 如果没有这个节点，Rviz中非固定关节的部件可能会位置显示错误
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        arguments=[urdf_model_path]
        )

    # 将节点添加到启动描述中
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)

    return ld
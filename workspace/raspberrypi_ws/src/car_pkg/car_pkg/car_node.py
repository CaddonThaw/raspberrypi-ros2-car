#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from tf_transformations import quaternion_from_euler
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
import serial   
import threading
import time
import math

class CarNode(Node):
    def __init__(self, name, port = '/dev/stm32_dev', baudrate = 115200):
        super().__init__(name)
        
        self.odometry_pub = self.create_publisher(Odometry, '/odom', 10)
        self.odometry_broadcaster = TransformBroadcaster(self)
        self.static_tf_broadcaster = StaticTransformBroadcaster(self)
        self.create_timer(0.1, self.publish_odom)
        self.key_control_sub = self.create_subscription(Twist, '/key_control', self.key_control_callback, 10)
        self.cmd_vel_sub = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)

        # map -> odom -> base_footprint -> base_link -> laser_link
        self.odomframe_id = 'odom'
        self.basefootframe_id = 'base_footprint'
        self.baseframe_id = 'base_link'
        self.laserframe_id = 'laser_link'
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.v_x = 0.0
        self.v_z = 0.0
        self.angle = 0.0
        
        self.gyroz = 0.0
        self.left_speed = 0.0
        self.right_speed = 0.0
        self.target_speed = 0.0
        self.target_angle = 0.0
        
        self.current_time = 0.0
        self.last_time = self.get_clock().now()
        
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=0.001)
            self.get_logger().info('串口已打开: {}'.format(port))
        except:
            self.get_logger().error('串口打开失败: {}'.format(port))
            self.serial_port = None
        
        self.publish_static_tf()
        
        self.car_thread = threading.Thread(target=self.car_loop)
        self.car_thread.start()   

    def publish_static_tf(self):
        basefoot_to_base = TransformStamped()
        basefoot_to_base.header.stamp = self.get_clock().now().to_msg()
        basefoot_to_base.header.frame_id = self.basefootframe_id
        basefoot_to_base.child_frame_id = self.baseframe_id
        basefoot_to_base.transform.translation.x = 0.0
        basefoot_to_base.transform.translation.y = 0.0
        basefoot_to_base.transform.translation.z = 0.043
        basefoot_to_base.transform.rotation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)
        
        base_to_laser = TransformStamped() 
        base_to_laser.header.stamp = self.get_clock().now().to_msg()
        base_to_laser.header.frame_id = self.baseframe_id 
        base_to_laser.child_frame_id = self.laserframe_id  
        base_to_laser.transform.translation.x = 0.057
        base_to_laser.transform.translation.y = 0.0  
        base_to_laser.transform.translation.z = 0.0745
        q = quaternion_from_euler(0, 0, 0)  
        base_to_laser.transform.rotation = Quaternion(
            x=q[0], y=q[1], z=q[2], w=q[3]
        )

        self.static_tf_broadcaster.sendTransform(basefoot_to_base)
        self.static_tf_broadcaster.sendTransform(base_to_laser)
        self.get_logger().info('已发布静态TF: base_footprint → base_link → laser_link') 
    
    def key_control_callback(self, msg):
        self.target_speed = msg.linear.x
        self.target_angle = msg.angular.z
        
    def cmd_vel_callback(self, msg):
        self.target_speed = msg.linear.x
        self.target_angle = -msg.angular.z 
        
        if self.target_speed > 0:
            if self.target_speed > 0.5: 
                self.target_speed = 0.5
            elif self.target_speed < 0.2:
                self.target_speed = 0.2
        elif self.target_speed < 0:
            if self.target_speed < -0.5:
                self.target_speed = -0.5
            elif  self.target_speed > -0.2:
                self.target_speed = -0.2
        else:
            self.target_speed = 0 
            
    def car_loop(self):
        while rclpy.ok():
            if self.serial_port:
                message = '(x={},z={})\r\n'.format(self.target_speed, self.target_angle)
                self.serial_port.write(message.encode('utf-8'))
                    
                if self.serial_port.in_waiting > 0:
                    raw_data = self.serial_port.readline().decode('utf-8').strip()
                    
                    if raw_data.startswith('(') and raw_data.endswith(')') and ',' in raw_data:
                        try:
                            content = raw_data[1:-1]  
                            gyroz_str, left_str, right_str = content.split(',')

                            self.gyroz = float(gyroz_str)
                            self.gyroz = -self.gyroz
                            self.left_speed = float(left_str)
                            self.right_speed = float(right_str)

                            # 调试用（正式使用时可以注释掉）
                            # self.get_logger().info(
                            #     f"串口数据 - gyroz: {self.gyroz}, left: {self.left_speed}, right: {self.right_speed}",
                            #     throttle_duration_sec=0.5  # 每0.5秒最多打印一次
                            # )
                            
                        except ValueError as e:
                            self.get_logger().error(f"整数转换错误: {raw_data} - {e}")
                        except Exception as e:
                            self.get_logger().error(f"数据处理异常: {raw_data} - {e}")
            
            time.sleep(0.005)

    def publish_odom(self):
        self.current_time = self.get_clock().now()
        dt = (self.current_time - self.last_time).nanoseconds * 1e-9
        d = (self.left_speed + self.right_speed) / 2

        if abs(self.gyroz) > 0.1:
            self.angle += self.gyroz * dt  
            self.angle = math.atan2(math.sin(self.angle), math.cos(self.angle))  # 限制在[-π, π]
        self.pos_x += d * math.cos(self.angle) 
        self.pos_y += d * math.sin(self.angle)
        self.v_x = d / dt if dt > 0 else 0
        self.v_z = self.gyroz if abs(self.gyroz) > 0.1 else 0
        
        self.last_time = self.current_time
        
        # 调试用（正式使用时可以注释掉）
        # self.get_logger().info(f"Odometry - X: {self.pos_x / 66.6 :.3f} m, Y: {self.pos_y / 66.6 :.3f} m, Angle: {self.angle:.3f} rad",throttle_duration_sec=0.5)   
        
        # 创建并发布里程计消息
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = self.odomframe_id
        odom.child_frame_id = self.basefootframe_id       
        
        quaternion = quaternion_from_euler(0, 0, self.angle)  
        odom.pose.pose.position.x = float(self.pos_x) / 66.6
        odom.pose.pose.position.y = float(self.pos_y) / 66.6
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = quaternion[0]
        odom.pose.pose.orientation.y = quaternion[1]
        odom.pose.pose.orientation.z = quaternion[2]
        odom.pose.pose.orientation.w = quaternion[3]
        
        odom.twist.twist.linear.x = float(self.v_x)
        odom.twist.twist.linear.y = 0.0
        odom.twist.twist.angular.z = float(self.v_z)
        
        self.odometry_pub.publish(odom) 
        
        transform = TransformStamped()
        transform.header.stamp = odom.header.stamp
        transform.header.frame_id = self.odomframe_id
        transform.child_frame_id = self.basefootframe_id
        transform.transform.translation.x = self.pos_x / 66.6
        transform.transform.translation.y = self.pos_y / 66.6
        transform.transform.rotation = Quaternion(
            x=quaternion[0],
            y=quaternion[1],
            z=quaternion[2],
            w=quaternion[3]
        ) 
        self.odometry_broadcaster.sendTransform(transform)   

def main(args=None):
    rclpy.init(args=args)           # 初始化rclpy
    node = CarNode("car_node")      # 新建一个节点
    try:
        rclpy.spin(node)            # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()        # 关闭rclpy
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios
import select

class KeyboardControl(Node):
    def __init__(self):
        super().__init__('keyboard_control')
        self.publisher = self.create_publisher(Twist, 'key_control', 10)
        self.twist_msg = Twist()
        
        # 控制参数配置
        self.linear_speed = 0.5   # 前进/后退速度 (m/s)
        self.angular_speed = 1.0  # 旋转速度 (rad/s)
        
        # 保存原始终端设置
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        
        # 当前状态跟踪
        self.current_state = "停止"
        print("\nWSAD键盘控制 (Ctrl+C退出)")
        print("W:前进 S:后退 A:左转 D:右转 空格:停止\n")

    def get_key(self):
        """获取按键输入"""
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            return sys.stdin.read(1)
        return None

    def run(self):
        """主循环"""
        try:
            tty.setraw(sys.stdin.fileno())
            
            while rclpy.ok():
                key = self.get_key()
                if not key:
                    continue
                
                # 重置速度
                self.twist_msg.linear.x = 0.0
                self.twist_msg.angular.z = 0.0
                
                # 处理按键
                new_state = self.current_state
                if key.lower() == 'w':
                    self.twist_msg.linear.x = self.linear_speed
                    new_state = "前进"
                elif key.lower() == 's':
                    self.twist_msg.linear.x = -self.linear_speed
                    new_state = "后退"
                elif key.lower() == 'a':
                    self.twist_msg.angular.z = self.angular_speed
                    new_state = "左转"
                elif key.lower() == 'd':
                    self.twist_msg.angular.z = -self.angular_speed
                    new_state = "右转"
                elif key == ' ':
                    new_state = "停止"
                elif key == '\x03':  # Ctrl+C
                    break
                
                # 只在状态变化时打印
                if new_state != self.current_state:
                    self.current_state = new_state
                    print(f"\r当前: {self.current_state}", end='', flush=True)
                
                self.publisher.publish(self.twist_msg)
                
        finally:
            # 恢复终端设置
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            self.twist_msg.linear.x = 0.0
            self.twist_msg.angular.z = 0.0
            self.publisher.publish(self.twist_msg)
            print("\n已停止")

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardControl()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
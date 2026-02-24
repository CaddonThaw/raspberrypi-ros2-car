# raspberrypi-ros2-car

基于树莓派4B的ROS2自动定位与导航小车

## 📖 项目简介

这是一个基于 **ROS2（机器人操作系统2）** 的自主导航智能小车项目，采用树莓派4B作为主控平台，结合STM32单片机进行底层硬件控制。小车能够实现激光雷达SLAM建图、自主定位、路径规划和自主导航等功能。

## 🛠️ 硬件配置

### 核心硬件
- **主控板**：树莓派4B（Ubuntu 24.04 + ROS2 Jazzy）
- **底层控制器**：STM32F103C8T6
- **激光雷达**：国科光芯 COIN-D6 单线激光雷达
- **电机驱动**：TB6612FNG双路直流电机驱动模块
- **传感器**：
  - MPU6050 六轴姿态传感器（陀螺仪+加速度计）
  - 编码器（轮速测量，2000脉冲/转）
- **显示屏**：0.96寸OLED显示屏
- **电源**：根据实际配置调整

### 机械参数
- 轮径：65mm
- 编码器分辨率：2000 脉冲/转

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    虚拟机（VMware）                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 键盘控制节点  │  │ Cartographer │  │    Nav2      │     │
│  │key_control   │  │    SLAM      │  │  自主导航     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                   │            │
│         └──────────────────┴───────────────────┘            │
│                            │ /key_control、/cmd_vel         │
└────────────────────────────┼───────────────────────────────┘
                             │ ROS2 网络通信
┌────────────────────────────┼───────────────────────────────┐
│                  树莓派4B（Ubuntu 24.04）                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  car_node    │  │  lidar_node  │  │   TF树发布   │     │
│  │  底盘控制    │  │  激光雷达    │  │   里程计     │     │
│  └──────┬───────┘  └──────────────┘  └──────────────┘     │
│         │ 串口通信（115200）                                │
└─────────┼─────────────────────────────────────────────────┘
          │
┌─────────┼─────────────────────────────────────────────────┐
│    STM32F103C8T6（底层控制固件）                            │
│  ┌──────┴───────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   串口通信    │  │   电机控制   │  │   传感器读取  │     │
│  │  指令解析    │  │   TB6612     │  │  编码器+IMU   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                   │            │
│         └──────────────────┴───────────────────┘            │
│              ┌─────────────┐                                │
│              │    OLED     │                                │
│              │  状态显示    │                                │
│              └─────────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

## 📁 项目结构

```
raspberrypi-ros2-car/
├── stm32_base/               # STM32底层控制代码
│   └── ros2_car/
│       ├── Core/             # HAL库核心代码
│       ├── Devices/          # 外设驱动库
│       │   ├── TB6612/       # 电机驱动
│       │   ├── Encoder/      # 编码器
│       │   ├── MPU6050/      # 六轴传感器（DMP）
│       │   └── OLED/         # OLED显示
│       └── Drivers/          # STM32 HAL驱动
│
├── ubuntu_workspace/
│   ├── raspberrypi_ws/       # 树莓派工作空间
│   │   └── src/
│   │       ├── car_pkg/      # 小车底盘功能包
│   │       │   ├── car_pkg/
│   │       │   │   └── car_node.py         # 底盘控制节点
│   │       │   └── launch/
│   │       │       └── car_base.launch.py  # 底盘+雷达启动
│   │       └── cspc_lidar_sdk_ros2/        # 激光雷达SDK
│   │
│   └── vmware_ws/            # 虚拟机工作空间
│       └── src/
│           └── car_pkg/      # 上层控制功能包
│               ├── car_pkg/
│               │   └── key_control_node.py  # 键盘控制节点
│               ├── launch/
│               │   ├── car_display.launch.py   # 小车模型显示
│               │   ├── car_mapping.launch.py   # SLAM建图
│               │   └── car_nav.launch.py       # 自主导航
│               ├── urdf/                       # 小车模型描述
│               ├── config/                     # Cartographer配置
│               ├── params/                     # Nav2参数
│               └── maps/                       # 保存的地图
│
└── README.md
```

## 🚀 功能特性

### 1. 底层硬件控制（STM32）
- ✅ TB6612双路电机PWM速度控制
- ✅ 编码器速度反馈（左右轮独立测速）
- ✅ MPU6050 DMP姿态解算（提供角速度Z轴）
- ✅ OLED实时显示传感器数据
- ✅ 串口通信协议（与树莓派交互）

### 2. 底盘运动控制（树莓派）
- ✅ 差速驱动运动学模型
- ✅ 里程计（Odometry）发布
- ✅ TF坐标变换发布（odom → base_footprint → base_link → laser_link）
- ✅ 速度指令处理（/cmd_vel、/key_control）
- ✅ 多线程串口通信

### 3. SLAM建图
- ✅ Cartographer 2D激光SLAM
- ✅ 实时地图构建
- ✅ 地图保存功能

### 4. 自主导航
- ✅ Nav2导航栈
- ✅ AMCL自适应蒙特卡洛定位
- ✅ 全局路径规划
- ✅ 局部路径规划与避障
- ✅ RViz2可视化界面

### 5. 手动控制
- ✅ 键盘控制（WSAD按键）
- ✅ 实时状态反馈

## 📡 通信协议

### 串口通信格式（树莓派 ↔ STM32）

**树莓派发送（控制指令）：**
```
(x=<线速度>,z=<角速度>)\r\n
```
- `x`：线速度（m/s），范围：-0.5 ~ 0.5
- `z`：角速度（rad/s），范围：-2.0 ~ 2.0

**STM32返回（传感器数据）：**
```
(<gyroz>,<left_speed>,<right_speed>)\r\n
```
- `gyroz`：Z轴角速度（rad/s）
- `left_speed`：左轮线速度（m/s）
- `right_speed`：右轮线速度（m/s）

**示例：**
```
发送：(x=0.3,z=0.5)\r\n
接收：(-0.48,0.31,0.29)\r\n
```

## 🔧 环境配置

### 1. 树莓派环境
```bash
# 操作系统：Ubuntu 24.04 LTS（ARM64）
# ROS版本：ROS2 Jazzy

# 安装ROS2 Jazzy（如未安装）
sudo apt update
sudo apt install ros-jazzy-desktop

# 安装依赖
sudo apt install ros-jazzy-nav2-bringup
sudo apt install ros-jazzy-cartographer-ros
sudo apt install python3-pip
pip3 install pyserial
pip3 install transforms3d
```

### 2. 虚拟机环境
```bash
# 操作系统：Ubuntu 24.04 LTS（x86_64）
# ROS版本：ROS2 Jazzy

# 安装相同的依赖
sudo apt install ros-jazzy-desktop
sudo apt install ros-jazzy-nav2-bringup
sudo apt install ros-jazzy-cartographer-ros
```

### 3. STM32开发环境
- **IDE**：STM32CubeIDE
- **芯片**：STM32F103C8T6
- **HAL库版本**：STM32F1 HAL Driver

## 📦 编译与部署

### 🔹 STM32固件编译
1. 使用 STM32CubeIDE 打开 `stm32_base/ros2_car` 项目
2. 配置串口设备名（可选）：编辑 `Devices/config.h`
3. 编译项目：`Project → Build All`
4. 烧录固件：连接ST-Link，点击 `Run → Debug`

### 🔹 树莓派工作空间
```bash
# 进入树莓派工作空间
cd ~/raspberrypi_ws

# 编译
colcon build

# 配置环境变量
source install/setup.bash

# 设置串口权限
sudo chmod 666 /dev/ttyUSB0  # 根据实际串口设备调整

# 配置激光雷达udev规则（首次需要）
cd src/cspc_lidar_sdk_ros2
sudo cp sc_mini.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 🔹 虚拟机工作空间
```bash
# 进入虚拟机工作空间
cd ~/vmware_ws

# 编译
colcon build

# 配置环境变量
source install/setup.bash
```

## 🎮 使用说明

### 第一步：启动底盘和雷达（树莓派）
```bash
source ~/raspberrypi_ws/install/setup.bash
ros2 launch car_pkg car_base.launch.py
```
此命令会启动：
- 小车底盘控制节点
- 激光雷达驱动节点

### 第二步：选择运行模式

#### 模式A：键盘手动控制（虚拟机）
```bash
source ~/vmware_ws/install/setup.bash
ros2 run car_pkg key_control_node

# 控制方式：
# W - 前进
# S - 后退  
# A - 左转
# D - 右转
# 空格 - 停止
```

#### 模式B：SLAM建图（虚拟机）
```bash
source ~/vmware_ws/install/setup.bash
ros2 launch car_pkg car_mapping.launch.py

# 使用键盘控制节点遥控小车移动，构建地图
# 建图完成后保存地图：
ros2 run nav2_map_server map_saver_cli -f ~/vmware_ws/src/car_pkg/maps/my_map
```

#### 模式C：自主导航（虚拟机）
```bash
source ~/vmware_ws/install/setup.bash
ros2 launch car_pkg car_nav.launch.py

# 在RViz2中：
# 1. 使用 "2D Pose Estimate" 设置初始位姿
# 2. 使用 "Nav2 Goal" 设置目标点
# 3. 小车将自主规划路径并导航
```

## 🐛 故障排除

### 1. 串口打开失败
```bash
# 检查串口设备
ls /dev/ttyUSB* 或 ls /dev/ttyACM*

# 添加用户到dialout组
sudo usermod -aG dialout $USER
# 重新登录生效

# 临时授权
sudo chmod 666 /dev/ttyUSB0
```

### 2. 激光雷达无数据
```bash
# 检查雷达设备
ls /dev/ttyUSB*

# 重新配置udev规则
cd ~/raspberrypi_ws/src/cspc_lidar_sdk_ros2
sudo cp sc_mini.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 3. TF坐标变换错误
```bash
# 检查TF树
ros2 run tf2_tools view_frames

# 查看TF实时状态
ros2 run tf2_ros tf2_echo odom base_link
```

### 4. 导航无法规划路径
- 确保已正确设置初始位姿（2D Pose Estimate）
- 检查地图文件路径是否正确
- 查看 `params/nav2_params.yaml` 配置是否合理
- 确认 `use_sim_time` 设置为 `false`

## 📊 性能参数

| 参数 | 数值 |
|------|------|
| 最大线速度 | 0.5 m/s |
| 最大角速度 | 2.0 rad/s |
| 里程计更新频率 | 10 Hz |
| 激光雷达扫描频率 | 根据设备规格 |
| 串口波特率 | 115200 |
| 控制周期 | 10ms（STM32） |

## 📚 技术栈

- **ROS2 Jazzy** - 机器人操作系统
- **Nav2** - 自主导航
- **Cartographer** - SLAM算法
- **STM32 HAL** - 底层驱动
- **Python3** - 上层节点开发
- **C/C++** - 底层固件开发

## 📝 开发计划

- [ ] 增加超声波避障
- [ ] 优化PID参数自整定
- [ ] 添加Web远程监控界面
- [ ] 支持多点巡航模式
- [ ] 增加语音交互功能

## 📄 许可证

本项目遵循 GPL-3.0 许可证，详情见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过 GitHub Issues 联系。

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**

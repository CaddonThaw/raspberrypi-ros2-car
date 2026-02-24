################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Devices/Encoder/Encoder.c 

OBJS += \
./Devices/Encoder/Encoder.o 

C_DEPS += \
./Devices/Encoder/Encoder.d 


# Each subdirectory must supply rules for building sources it contributes
Devices/Encoder/%.o Devices/Encoder/%.su Devices/Encoder/%.cyclo: ../Devices/Encoder/%.c Devices/Encoder/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m3 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F103xB -c -I../Core/Inc -I../Drivers/STM32F1xx_HAL_Driver/Inc/Legacy -I../Drivers/STM32F1xx_HAL_Driver/Inc -I../Drivers/CMSIS/Device/ST/STM32F1xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices" -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices/Encoder" -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices/MPU6050" -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices/OLED" -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices/TB6612" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Devices-2f-Encoder

clean-Devices-2f-Encoder:
	-$(RM) ./Devices/Encoder/Encoder.cyclo ./Devices/Encoder/Encoder.d ./Devices/Encoder/Encoder.o ./Devices/Encoder/Encoder.su

.PHONY: clean-Devices-2f-Encoder


################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Devices/OLED/OLED.c 

OBJS += \
./Devices/OLED/OLED.o 

C_DEPS += \
./Devices/OLED/OLED.d 


# Each subdirectory must supply rules for building sources it contributes
Devices/OLED/%.o Devices/OLED/%.su Devices/OLED/%.cyclo: ../Devices/OLED/%.c Devices/OLED/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m3 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F103xB -c -I../Core/Inc -I../Drivers/STM32F1xx_HAL_Driver/Inc/Legacy -I../Drivers/STM32F1xx_HAL_Driver/Inc -I../Drivers/CMSIS/Device/ST/STM32F1xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices" -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices/Encoder" -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices/MPU6050" -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices/OLED" -I"C:/Users/21035/Desktop/Workspace/github/CaddonThaw/raspberrypi-ros2-car/ros2_car/Devices/TB6612" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Devices-2f-OLED

clean-Devices-2f-OLED:
	-$(RM) ./Devices/OLED/OLED.cyclo ./Devices/OLED/OLED.d ./Devices/OLED/OLED.o ./Devices/OLED/OLED.su

.PHONY: clean-Devices-2f-OLED


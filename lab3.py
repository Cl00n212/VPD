import ev3dev2.motor as motor
import time

delta = 2

omega_star = 100

def Pid_Reg(k_p, k_i, k_d, file_name):

    min_t = 1
    motor_a = motor.LargeMotor(motor.OUTPUT_A)

    time_start = time.time()
    timeReal = time_start
    pos_start = motor_a.position
    motor_pose = pos_start
    file = open(file_name, "w")
    inregralf = 0
    
    while True:
        last_time = timeReal
        timeReal = time.time() - time_start

        last_pose = motor_pose
        motor_pose = motor_a.position - pos_start
        if abs(motor_pose - omega_star) < delta:
            min_t = min(min_t,motor_pose)
        else:
            min_t = 1
        df = ((omega_star - motor_pose) - (omega_star - last_pose)) / (timeReal - last_time)
        inregralf += ((omega_star - motor_pose) + (omega_star - last_pose)) / 2 * (timeReal - last_time) 
        

        file.write(str(timeReal) + " " + str(motor_pose) + "\n")
        volt = k_p * (omega_star - motor_pose) + k_i * inregralf + k_d * df
        if volt > 100:
            volt = 100
        elif volt < -100:
            volt = -100
        motor_a.run_direct(duty_cycle_sp = volt)

        if timeReal > 1:
            motor_a.run_direct(duty_cycle_sp = 0)
            break
        
    file.close()

def P_Reg(k_p, file_name):
    Pid_Reg(k_p, 0, 0, file_name)

def Rel_Reg(file_name):
    file = open(file_name, "w")

    motor_a = motor.LargeMotor(motor.OUTPUT_A)

    time_start = time.time()
    pos_start = motor_a.position

    while True:
        timeReal = time.time() - time_start
        motor_pose = motor_a.position - pos_start
        file.write(str(timeReal) + " " + str(motor_pose) + "\n")
        if (motor_pose > omega_star):
            volt = -100
        elif (motor_pose < omega_star):
            volt = 100
        else:
            volt = 0
        motor_a.run_direct(duty_cycle_sp = volt)

        if timeReal > 1:
            motor_a.run_direct(duty_cycle_sp = 0)
            break
    file.close()


#1.1 релейный регулятор

file_name = "data_Rel_Reg"
Rel_Reg(file_name)


#2.1 П - регулятор поиск k_p

for k_p in range(1,11,1):
    file_name = "data_PReg_big_" + str(k_p)
    P_Reg(k_p, file_name)

#2.4 ПИ - регулятор поиск k_i с завфиксированными k_p
    
k_p = 3

for k_i in range(1,11,1):
    file_name = "data_PReg_big_" + str(k_p) + "_" + str(k_i)
    Pid_Reg(k_p, k_i, 0, file_name)
#2.4 ПИД - регуляторм поиск k_d с завфиксированными k_p и k_i

k_p = 3
k_i = 5

k_d = 0.051
while k_d < 0.15:
    file_name = "data_PReg_big_" + str(k_p) + "_" + str(k_i) + "_" + str(k_d)[:5].replace(".","x")
    Pid_Reg(k_p, k_i, k_d, file_name)
    k_d += 0.01

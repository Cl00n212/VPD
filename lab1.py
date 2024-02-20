import ev3dev2.motor as motor
import time

motor_a = motor.LargeMotor(motor.OUTPUT_A)
for volt in range(100, -101, -20):
    time_start = time.time()
    pos_start = motor_a.position
    name = "data" + str(volt)

    file = open(name, "w")
    while True:
        timeReal = time.time() - time_start
        motor_a.run_direct(duty_cycle_sp = volt)
        motor_pose = motor_a.position - pos_start
        motor_vel = motor_a.speed
        file.write(str(timeReal) + " " + str(motor_pose) + " " + str(motor_vel) + "\n")
        if timeReal > 1:
            motor_a.run_direct(duty_cycle_sp = 0)
            break

    file.close()
    time.sleep(0.4)
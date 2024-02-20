import ev3dev2.motor as motor
import time

zadergka = 4
zamer = 3
motor_a = motor.LargeMotor(motor.OUTPUT_A)
for volt in range(15, 51, 5):
    time_start = time.time()
    pos_start = motor_a.position

    while True:
        timeReal = time.time() - time_start
        motor_a.run_direct(duty_cycle_sp = volt)
        if timeReal > zamer:
            motor_a.run_direct(duty_cycle_sp = 0)
            break
    time.sleep(zadergka)
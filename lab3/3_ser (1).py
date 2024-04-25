import ev3dev2.motor as motor
import time

dtime = 0.05
motor_a = motor.LargeMotor(motor.OUTPUT_A)
best = 100

def Rel_reg(file_name):
    global best
    time_start = time.time()
    time_now = time.time()
    pose_start = motor_a.position
    file = open(file_name, "w")
    while True:
        time_last = time_now
        time_now = time.time()
        
        if time_now - time_last < dtime: # дорабатываем прошлый volt до dtime
            time.sleep(dtime - time_now + time_last)
        else:
            motor_a.run_direct(duty_cycle_sp=0) #чтобы сильно не переработал с прошлым volt
            print("!!!!!!!")

        time_now = time.time()# пересчитываем так как мы увеличили промежуток работы сном
        now_pos = motor_a.position - pose_start
            
        file.write(str(time_now - time_start) + " " + str(now_pos) + "\n")
        if best - now_pos > 0:
            volt = 100
        elif best - now_pos < 0:
            volt = -100
        else:
            volt = 0
            
        motor_a.run_direct(duty_cycle_sp=volt)
        
        if time_now - time_start >5:
            motor_a.run_direct(duty_cycle_sp=0)
            file.close()
            break

def PID_reg(k_p, k_i, k_d, file_name):
    global best
    time_start = time.time()
    time_now = 0
    pose_start = motor_a.position
    now_pos = 0
    file = open(file_name, "w")
    integral = 0
    while True:
        time_last = time_now
        time_now = time.time()
        
        if time_now - time_last < dtime:# дорабатываем прошлый volt до dtime
            time.sleep(dtime - time_now + time_last)
        else:
            motor_a.run_direct(duty_cycle_sp=0) #чтобы сильно не переработал с прошлым volt
            print("!!!!!!!")

        time_now = time.time()# пересчитываем так как мы увеличили промежуток работы сном
        last_pos = now_pos
        e_last = best - now_pos
        now_pos = motor_a.position - pose_start
        e_now = best - now_pos

        file.write(str(time_now - time_start) + " " + str(now_pos) + "\n")
        
        integral += (e_now + e_last)/2 * dtime
        #print(e_now, e_last, e_now + e_last, integral)

        dif = (- e_last + e_now) / dtime
        volt = k_p * e_now + k_i * integral + k_d * dif
        if abs(volt) > 100 :
            volt = volt / abs(volt) * 100
        motor_a.run_direct(duty_cycle_sp=volt)
        if time_now - time_start > 5:# жесть как долго, либо уменьшать тут, либо количество операций фора(программа сумарно работает 150 секунд)
            motor_a.run_direct(duty_cycle_sp=0)
            file.close()
            break
#rel reg
#Rel_reg("rel_reg.txt")
''' #не акутально
#П регулятор            
for k_p in range(1, 11, 1):
    #file_name = f"PID{str(k_p)}".replace(".", "^") + ".txt"
    file_name = ("PID" + str(k_p)).replace(".", "^") + ".txt" 
    PID_reg(k_p, 0, 0, file_name)

#ПИ ругулятор
k_p = 1
for k_i in range(1, 11, 1):
    file_name = f"PID{str(k_p)}_{str(k_i)}".replace(".", "^") + ".txt"
    PID_reg(k_p, k_i, 0, file_name)
'''
#ПИД регулятор
k_p = 0.3
k_i = 0.3
k_d = 0
for per in range(5, 51, 5):
    per /= 10 
    if per % 1 == 0:
        per = int(per)
    k_d = per #!!!!!!!!!!!!!!!
    time.sleep(2)
    file_name = ("PID" + str(k_p) + "_" + str(k_i) + "_" + str(k_d)).replace(".", "^") + ".txt"
    PID_reg(k_p, k_i, k_d, file_name)

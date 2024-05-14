#!/usr/bin/env python3
import ev3dev2.motor as motor
import time
import math

r_kol = 0.021 #metr
B_rol = 0.165 #metr
theta = 0.0  #start_theta
error = 0.05 #error_for_point
Ks = 200 #ks_for_move_vpered
Kr = 350 #kr_for_move_vbok
delta_time = 0.05 #time_for_operation
mass_start_cord = [0.0, 0.0, theta] #start_cordinate
mass_start_proizv = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]] #start_proizv_cordinate

def get_motors(): 
    motor_left = motor.LargeMotor(motor.OUTPUT_A)
    motor_right = motor.LargeMotor(motor.OUTPUT_D)

    return (motor_left, motor_right)


def stop_motors(): 
    motors = get_motors()
    motors[0].run_direct(duty_cycle_sp = 0)
    motors[1].run_direct(duty_cycle_sp = 0)


def start_motors(Ul, Ur): 
    motors = get_motors()
    motors[0].run_direct(duty_cycle_sp = Ul)
    motors[1].run_direct(duty_cycle_sp = Ur)

def rast_do_point(ex, ey):
    return math.sqrt(ex*ex + ey*ey)

def get_U(mass_gelaem, mass_cord): 

    ex = (mass_gelaem[0] - mass_cord[0])
    ey = (mass_gelaem[1] - mass_cord[1])
    th = mass_cord[2]
    mod_p = rast_do_point(ex,ey)

    A_1 = (math.cos(th) * ey - math.sin(th) * ex) / mod_p
    CS = (math.cos(th) * ex + math.sin(th) * ey) / mod_p
    if CS < 0:
        A_1 = 1

    alfa = A_1
    '''
    alfa = math.atan2(ey, ex)# azimut
    if (abs(alfa) - math.pi * 3 / 4 > 0):
        alfa = -abs(alfa) + mass_cord[2]
    else:
        alfa = alfa - mass_cord[2]
    '''
    Us = Ks * mod_p
    Ur = Kr * alfa
    U_left = Us - Ur
    U_right = Us + Ur
    
    if (U_left > 100):
        U_left = 100
    elif (U_left < -100):
        U_left = -100

    if (U_right > 100):
        U_right = 100
    elif (U_right < -100):
        U_right = -100

    return (U_left, U_right)





def anpack_mass_proizv(mass_proizv): 
    return (mass_proizv[0], mass_proizv[1])


def update_mass_proizv(mass_proizv, new_mass_proizv):
    mass_proizv[0] = new_mass_proizv[0]
    mass_proizv[1] = new_mass_proizv[1]


def update_mass_cord(mass_cord, new_mass_cord):
    mass_cord[0] = new_mass_cord[0]
    mass_cord[1] = new_mass_cord[1]
    mass_cord[2] = new_mass_cord[2]


def new_proiz(mass_wlr, mass_proizv, mass_cord): 

    mass_proizv_cord_prev, mass_proizv_cord = anpack_mass_proizv(mass_proizv)

    w = (mass_wlr[1] - mass_wlr[0]) * r_kol/ B_rol
    v = (mass_wlr[1] + mass_wlr[0]) * r_kol / 2
    x_pi = v * math.cos(mass_cord[2])
    y_pi = v * math.sin(mass_cord[2])
    th_pi = w

    new_mass_proizv = [mass_proizv_cord, [x_pi, y_pi, th_pi]]

    update_mass_proizv(mass_proizv, new_mass_proizv)



def integrate(mass_cord, mass_proizv, h): 

    mass_proizv_cord_prev, mass_proizv_cord = anpack_mass_proizv(mass_proizv)

    new_mass_cord = [0.0, 0.0, 0.0]
    new_mass_cord[0] = mass_cord[0] + (mass_proizv_cord_prev[0] + mass_proizv_cord[0]) * h * 0.5
    new_mass_cord[1] = mass_cord[1] + (mass_proizv_cord_prev[1] + mass_proizv_cord[1]) * h * 0.5
    new_mass_cord[2] = mass_cord[2] + (mass_proizv_cord_prev[2] + mass_proizv_cord[2]) * h * 0.5

    update_mass_cord(mass_cord, new_mass_cord)


def save_cord(file_name, mass_cord): 
    file.write(str(mass_cord[0]) + " " + str(mass_cord[1]) + " " + str(mass_cord[2]) + "\n") 

def check_error_cord(mass_cord_1, mass_cord_2): 
    mod_p = rast_do_point(mass_cord_1[0] - mass_cord_2[0], mass_cord_1[1] - mass_cord_2[1])
    if (mod_p < error):
        return True
    else:
        return False


def F_U(mass_gelaem, mass_cord, mass_proizv, file_name): 

    motors = get_motors()

    time_last = time.time()

    pos_start = [motors[0].position, motors[1].position]
    
    while True:
        time_real = time.time()

        save_cord(file_name, mass_cord)

        if (check_error_cord(mass_cord, mass_gelaem)):
            break

        time_error = time_real - time.time()

        if time_error < delta_time: 
            time.sleep(delta_time - time_error)
        else:
            print('warning: time_error is out of time')
            
        time_real = time.time()
        h = time_real - time_last

        mass_wlr = [motors[0].speed*math.pi/180, motors[1].speed*math.pi/180]
        # mass_wlr = [Ul, Ur]
        
        new_proiz(mass_wlr, mass_proizv, mass_cord)

        integrate(mass_cord, mass_proizv, h)
        Ul, Ur = get_U(mass_gelaem, mass_cord)
        
        #save_cord(file_name, [Ul,Ur,0.0])
        #save_cord(file_name, mass_proizv[0])
        
        start_motors(Ul, Ur)
        
        time_last = time_real
    
    stop_motors()






dlin = 1    
a = [[1, 1],[ -1, 1],[-1, -1],[1, -1]]


mass_cord = [0.0, 0.0, theta]
mass_proizv = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

n = 4
for i in range(n):
    file_name = "data_" + str(i + 1) + ".txt"
    file = open(file_name, "w")

    #x0, y0 = map(int, input().split())
    x0 = a[i][0]
    y0 = a[i][1]
    
    F_U([x0, y0], mass_cord, mass_proizv, file_name)
    file.close()
    print(i + 1)
    time.sleep(2)

print("this is end!!!!!!!!")

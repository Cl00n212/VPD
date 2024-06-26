import ev3dev2.motor as motor
import time
import math

r_kol = 28 # радиус колёс
B_rol = 16.5 # растояние между центрами двух колёс
theta = 0.0 # изначальный угол относительно Ox
error = 0.05 # константы ...
Ks = 0.6 # константы для прямолинейного движения 
Kr = 0.6 # константы для криволинейного движения
delta_time = 0.05 # время между опирациями 
mass_start_cord = [0.0, 0.0, theta]
mass_start_proizv = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

rad_v_gradus = 57.3

def get_motors(): # возвращяет массив [левый_двигатель, правый_двигатель]
    motor_left = motor.LargeMotor(motor.OUTPUT_A)
    motor_right = motor.LargeMotor(motor.OUTPUT_B)

    return (motor_left, motor_right)

def azimut(mass_gelaem, mass_cord):
    return math.atan2(mass_gelaem[0] - mass_cord[0], mass_gelaem[1] - mass_cord[1]) * rad_v_gradus

def stop_motors(): # останавливает моторы
    motors = get_motors()
    motors[0].run_direct(duty_cycle_sp = 0)
    motors[1].run_direct(duty_cycle_sp = 0)


def start_motors(Ul, Ur): # запускает моторы с наряжением Ul и Ur
    motors = get_motors()
    motors[0].run_direct(duty_cycle_sp = Ul)
    motors[1].run_direct(duty_cycle_sp = Ur)


def get_U(mass_gelaem, mass_cord): # возвращает напряжение картежем (U_left, U_right)
    mod_p = ((mass_gelaem[0] - mass_cord[0]) ** 2 + (mass_gelaem[1] - mass_cord[1]) ** 2) ** (1 / 2)
    alfa = azimut(mass_gelaem, mass_cord)
    Us = Ks * mod_p
    Ur = Kr * alfa
    U_left = Us + Ur
    U_right = Us - Ur
    
    if (U_left > 100):
        U_left = 100
    elif (U_left < -100):
        U_left = -100

    if (U_right > 100):
        U_right = 100
    elif (U_right < -100):
        U_right = -100

    return (U_left, U_right)





def anpack_mass_proizv(mass_proizv): # возвращает mass производных картежем (mass_proizv_last, mass_proizv_real)
    return (mass_proizv[0], mass_proizv[1])


def update_mass_proizv(mass_proizv, new_mass_proizv): # обновляет значение первой переменной(mass_proizv) на занченние второй
    mass_proizv = new_mass_proizv


def update_mass_cord(mass_cord, new_mass_cord): # обновляет значение первой переменной(mass_cord) на занченние второй
    mass_cord = new_mass_cord


def new_proiz(mass_wlr, mass_proizv, mass_cord): #1

    mass_proizv_cord_prev, mass_proizv_cord = anpack_mass_proizv(mass_proizv)

    w = (mass_wlr[1] - mass_wlr[0]) * r_kol/ B_rol
    v = (mass_wlr[1] - mass_wlr[0]) * r_kol / 2
    x_pi = v * math.cos(mass_cord[2])
    y_pi = v * math.sin(mass_cord[2])
    th_pi = w

    new_mass_proizv = [mass_proizv_cord, [x_pi, y_pi, th_pi]]

    update_mass_proizv(mass_proizv, new_mass_proizv)



def integrate(mass_cord, mass_proizv, h): #2

    mass_proizv_cord_prev, mass_proizv_cord = anpack_mass_proizv(mass_proizv)

    new_mass_cord = [0.0, 0.0, 0.0]
    new_mass_cord[0] = mass_cord[0] + (mass_proizv_cord_prev[0] + mass_proizv_cord[0]) * h * 0.5
    new_mass_cord[1] = mass_cord[1] + (mass_proizv_cord_prev[1] + mass_proizv_cord[1]) * h * 0.5
    new_mass_cord[2] = mass_cord[2] + (mass_proizv_cord_prev[2] + mass_proizv_cord[2]) * h * 0.5

    update_mass_cord(mass_cord, new_mass_cord)


def save_cord(file_name, mass_cord): #сохраняет кординаты в формате "x1 y1 theta"
    file.write(str(mass_cord[0]) + " " + str(mass_cord[1]) + " " + str(mass_cord[2]) + "\n") 

def check_error_cord(mass_cord_1, mass_cord_2): # проверяет отличается ли значение кодинат на error
    if (abs(mass_cord_1[0] - mass_cord_2[0]) < error and abs(mass_cord_1[1] - mass_cord_2[1]) < error):
        return True
    else:
        return False


def F_U(mass_gelaem, mass_cord, mass_proizv, file_name): #3

    motors = get_motors()

    time_last = time.time()

    pos_start = [motors[0].position, motors[1].position]
    
    while True:
        time_real = time.time()

        #save_cord(file_name, mass_cord)

        if (check_error_cord(mass_cord, mass_gelaem)):
            break

        time_error = time_real - time.time()

        if time_error < delta_time: # выравнивает промежутки времении между операциями
            time.sleep(delta_time - time_error)
            
        time_real = time.time()
        h = time_real - time_last

        mass_wlr = [motors[0].speed, motors[1].speed]
        
        new_proiz(mass_wlr, mass_proizv, mass_cord)

        integrate(mass_cord, mass_proizv, h)
        Ul, Ur = get_U(mass_gelaem, mass_cord)
        
        #save_cord(file_name, [Ul,Ur,0.0]) #дебаг
        
        start_motors(Ul, Ur)
        
        time_last = time_real
    
    stop_motors()







a = [[10,0],[0,10],[-10,0],[0,-10]]

n = 4
for i in range(n):
    file_name = "data_" + str(i + 1) + ".txt"
    file = open(file_name, "w")

    #x0, y0 = map(int, input().split())
    x0 = a[i][0]
    y0 = a[i][1]

    mass_cord = mass_start_cord
    mass_proizv = mass_start_proizv
    
    F_U([x0, y0], mass_cord, mass_proizv, file_name)
    file.close()

    time.sleep(1)

print("Программа закончила работу")

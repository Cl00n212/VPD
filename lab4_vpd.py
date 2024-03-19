import math

r_kol = 1 # радиус колёс
B_rol = 5 # растояние между центрами двух колёс
theta = 0.0 # изначальный угол относительно Ox

mass_proizv_cord = [0.0, 0.0, 0.0]
mass_proizv_cord_prev = [0.0, 0.0, 0.0]
mass_cord = [0.0, 0.0, theta]

def stat_motor(Ul,Ur):
    

def new_proiz(mass_wlr, mass_proizv_cord_prev, mass_proizv_cord, mass_cord):
    w = (mass_wlr[1] - mass_wlr[0]) * r_kol/ B_rol
    v = (mass_wlr[1] - mass_wlr[0]) * r_kol / 2
    x_pi = v * math.cos(mass_cord[-1][2])
    y_pi = v * math.sin(mass_cord[-1][2])
    th_pi = w
    return (mass_proizv_cord, [x_pi, y_pi, th_pi])
    
def integrate(mass_cord,h, mass_proizv_cord_prev,mass_proizv_cord ):
    mass_cord[0]=mass_cord[0]+(mass_proizv_cord_prev[0]+mass_proizv_cord[0])*h*0,5
    mass_cord[1]=mass_cord[1]+(mass_proizv_cord_prev[1]+mass_proizv_cord[1])*h*0,5
    mass_cord[2]=mass_cord[2]+(mass_proizv_cord_prev[2]+mass_proizv_cord[2])*h*0,5
    return mass_cord

def F_U(mass_gelaem, mass_cord): #3
    motor_left = motor.LargeMotor(motor.OUTPUT_A)
    motor_right = motor.LargeMotor(motor.OUTPUT_B)

    time_last = time.time()

    pos_start = [motor_left.position, motor_right.position]
    
    while True:
        time_real = time.time()
        h = time_real - time_last
        
        mass_wlr = [motor_left.speed, motor_right.speed]
        
    
    mod_p = ((mass_gelaem[0] - mass_cord[0]) ** 2 + (mass_gelaem[1] - mass_cord[1]) ** 2) ** (1 / 2)
    alfa = mass_gelaem[2] - mass_cord[2]
    Us = Ks * mod_p
    Ur = Kr * alfa
    U_left = Us + Ur
    U_right = Us - Ur
    






'''
def F_psi_start(x0,y0,xf,yf):
    return atan2(yf - y0, xf - x0)

def input_psi():
    #asdasasdasdasd
    return [psi_l, psi _ r]

def F_delta_L(delta_psi_l, delta_psi_r):
    delta_L = (delta_psi_l * r + delta_psi_r * r) / 2
    return delta_L

def F_delta_omega(delta_psi_l, delta_psi_r):
    delta_omega = (delta_psi_r + delta_psi_l) * r / B
    return delta_omega

def Delta_cordinat(delta_psi_l, delta_psi_r, last_omega):
    delta_omega = F_delta_omega(delta_psi_l, delta_psi_r)
    real_omega = last_omega + delta_omega
    delna_x = math.cos(real_omega) * F_delta_L(delta_psi_l, delta_psi_r)
    delta_y = math.sin(real_omega) * F_delta_L(delta_psi_l, delta_psi_r)
    return [delna_x, delta_y, delta_omega]

def Get_real_cordinat(delta_psi_l, delta_psi_r, last_x, last_y, last_omega):
    mass_delta = Delta_cordinat(delta_psi_l, delta_psi_r, last_omega)
    real_x = last_x + mass_delta[0]
    real_y = last_u + mass_delta[0]
    real_omega = last_omega + mass_delta[0]
    return [real_x, real_y, real_omega]

def F_U(mass_gelaem, mass_real_cordinat): #3
    mod_p = ((mass_gelaem[0] - mass_real_cordinat[0]) ** 2 + (mass_gelaem[1] - mass_real_cordinat[1]) ** 2) ** (1 / 2)
    alfa = mass_gelaem[2] - mass_real_cordinat[2]
    Us = Ks * mod_p
    Ur = Kr * alfa
    return [Us + Ur, Us - Ur]

def fun():


fun()
'''

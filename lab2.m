clc
clear all
close all
U_procent = [15, 20, 25, 30, 35, 40, 45, 50];
%U_procent = num2str(U_procent)
m_p = 15.6 / 1000
r_p = 23/2/1000
J_ed = m_p*r_p^2/2
I = 48
J = I^2 *J_ed 
L = 0.0047

colors = lines(10)

files_plus = ["data15.txt", "data20.txt", "data25.txt", ...
    "data30.txt", "data35.txt", "data40.txt", "data45.txt", "data50.txt"];

files_minus = ["data-15.txt", "data-20.txt", "data-25.txt", ...
    "data-30.txt", "data-35.txt", "data-40.txt", "data-45.txt", "data-50.txt"];

ampers_plus = [0.16, 0.22, ...
    0.27, 0.31, 0.36, ...
    0.41, 0.46, 0.52];
ampers_minus = [-0.15, -0.21, ...
    -0.26, -0.29, -0.35, ...
    -0.40, -0.46, -0.52];
voltage_minus = [-1.8, -2.5, ...
    -3.2, -3.8, -4.5, ...
    -5.1, -5.6, -6.1];
voltage_plus = [1.8, 2.6, ...
    3.3, 3.9 , 4.6, ...
    5.1, 5.7, 6.1];


%График зависимости силы тока от напряжения '+'
fun = @(par, ampers_plus)par(1) * ampers_plus;
par0 = 0;
par = lsqcurvefit(fun, par0, ampers_plus,  voltage_plus);
R_plus = par(1);
voltage_plus_apr = ampers_plus * R_plus;
figure(1);
set(gcf, 'Position', [100, 100, 800, 600]);
plot(ampers_plus, voltage_plus, ampers_plus, voltage_plus_apr, "LineWidth", 2);
xlabel("I, А");
ylabel("U, В");
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points");
title("U(I) положительное напряжение");
legend("Измерения", "Апроксимация", Location="best");
saveas(gcf, 'U(i)_plus.png')

%График силы тока от апряжение '-'
fun = @(par, ampers_minus)par(1) * ampers_minus;
par0 = 0;
par = lsqcurvefit(fun, par0, ampers_minus, voltage_minus);
R_minus = par(1);
voltage_minus_apr = ampers_minus * R_minus;
figure(2);
set(gcf, 'Position', [100, 100, 800, 600]);
plot(ampers_minus, voltage_minus, ampers_minus, voltage_minus_apr, "LineWidth", 2);
xlabel("I, А");
ylabel("U, В");
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points");

title("U(I) отрицательное напряжение");
legend("Измерения", "Апроксимация", Location="best");
saveas(gcf, 'U(i)_minus.png')

%%
R = (R_minus + R_plus)/2
% R = 10


omega_plus_sr = [];

speed = {};
time = {};

for i=1:8
    data=readmatrix("files/" + files_plus(i));
    omega = data(:,3)*pi/180;
    delt_omega = omega(end-19:end);
    omega_plus_sr(i) = sum(delt_omega) / length(delt_omega);

    speed{i} = omega;
    time{i} = data(:, 1);
end

for i=1:8
    data=readmatrix("files/" + files_minus(i));
    omega = data(:,3)*pi/180;
    delt_omega = omega(end-19:end);
    omega_minus_sr(i) = sum(delt_omega) / length(delt_omega);

    speed{i + 8} = omega;
    time{i + 8} = data(:, 1);
end

% вычисление k_e
fun = @(par, omega_plus_sr)par(1) * omega_plus_sr;
par = lsqcurvefit(fun, par0, omega_plus_sr, voltage_plus);
k_e_plus = par(1)
figure(3)
set(gcf, 'Position', [100, 100, 800, 600]);
plot(omega_plus_sr, voltage_plus, omega_plus_sr, omega_plus_sr.*k_e_plus, "LineWidth", 2)
xlabel("Угловая скорость, рад/c")
ylabel("U, В")
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points");
title("U(w) положительное напряжение");
legend("Измерения", "Апроксимация", Location="best")
saveas(gcf, 'U(w)_plus.png')

fun = @(par, omega_minus_sr)par(1) * omega_minus_sr;
par = lsqcurvefit(fun, par0, omega_minus_sr, voltage_minus);
k_e_minus = par(1)
figure(4)
set(gcf, 'Position', [100, 100, 800, 600]);
plot(omega_minus_sr, voltage_minus, omega_minus_sr, omega_minus_sr.*k_e_minus, "LineWidth", 2)
xlabel("Угловая скорость, рад/c")
ylabel("U, В")
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points");
title("U(w) отрицательное напряжение");
legend("Измерения", "Апроксимация", Location="best");
saveas(gcf, 'U(w)_minus.png');

k_e = (k_e_minus + k_e_plus)/2
k_m = k_e

%%

% положительное напряжение, симуляция
figure(10)
set(gcf, 'Position', [100, 100, 1000, 600]);
hold on; grid on;
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points")
ylabel("Сила тока (I), А")
xlabel("t, с")
title("I(t) симуляция положительное напряжение")


figure(11); 
set(gcf, 'Position', [100, 100, 1200, 600]);
hold on; grid on;
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points")
ylabel("угловая скорость (w), рад/с")
xlabel("t, с")
title("w(t) измерение, симуляция \newlineположительное напряжение")


for i=8:-1:1
       U = voltage_plus(i)
       simulin_data = sim("lab2.slx")

       figure(10)
       plot(simulin_data.I.Time, simulin_data.I.Data, 'LineWidth', 2,...
           'DisplayName', U_procent(i) + "%", "Color", colors(i, :))


       figure(11)
       plot(simulin_data.w.Time, simulin_data.w.Data, 'LineWidth', 2,...
           'DisplayName', "cимуляция " + U_procent(i) + "%", 'LineStyle' ,'--', "Color", colors(i, :))
       plot(time{i}, speed{i}, 'LineWidth', 2, 'DisplayName', ...
           "измерения " + U_procent(i) + "%", "Color", colors(i, :))
end
figure(10) %I(t)
legend("Location", "eastoutside");
saveas(gcf, 'I(t)_plus2.png');


figure(11) %W(t)
legend("NumColumns", 2, "Location", "eastoutside");
saveas(gcf, 'W(t)_plus2.png');


%%
% отрицательное напряжение, симуляция
figure(12)
set(gcf, 'Position', [100, 100, 1000, 600]);
hold on; grid on;
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points")
ylabel("Сила тока (I), А")
xlabel("t, с")
title("I(t) симуляция отрицательное напряжение")


figure(13); 
set(gcf, 'Position', [100, 100, 1200, 600]);
hold on; grid on;
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points")
ylabel("угловая скорость (w), рад/с")
xlabel("t, с")
title("w(t) измерение, симуляция \newlineотрицательное напряжение")


%for i=8:-1:1
for i = 1:8
       U = -voltage_plus(i)
       simulin_data = sim("lab2.slx")

       figure(12)
       plot(simulin_data.I.Time, simulin_data.I.Data, 'LineWidth', 2,...
           'DisplayName', -U_procent(i) + "%", "Color", colors(i, :))


       figure(13)
       plot(simulin_data.w.Time, simulin_data.w.Data, 'LineWidth', 2,...
           'DisplayName', "cимуляция " + -U_procent(i) + "%", 'LineStyle' ,'--', "Color", colors(i, :))
       plot(time{i+8}, speed{i+8}, 'LineWidth', 2, 'DisplayName', ...
           "измерения " + -U_procent(i) + "%", "Color", colors(i, :))
end
figure(12) %I(t)
legend("Location", "eastoutside");
saveas(gcf, 'I(t)_minus2.png');


figure(13) %W(t)
legend("NumColumns", 2, "Location", "eastoutside");
saveas(gcf, 'W(t)_minus2.png');


clc
clear all
close all
load("motor_for_sim.mat")
p = 2;
i = 0;    
d = 0.17;

data_sim = sim("relein")

data = readmatrix(strrep(sprintf('plots_data/PID' + string(p) + "_" + string(i) + "_" + string(d)), '.', '^') + ".txt"); %!
time = data(:, 1);
angle = data(:,2)*pi/180;
plot(time, angle, LineWidth=2, DisplayName="p=" + p +" i=" + i  +  " d=" + d)
hold on
grid on
time = [0, 5];
lin = [100*pi/180, 100*pi/180];
plot(time, lin, "LineStyle","--")
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points");
xlabel("время, с")
ylabel("угол, рад")
title("симуляция PD")
plot(data_sim.tetta.Time, data_sim.tetta.Data, LineWidth=2, DisplayName="Симуляция")
legend()
save2PDF("plots_data/SIM_PD")
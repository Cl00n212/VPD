clc
close all
clear all
p_all = [0.5, 2, 2, 0.3]
i_all = [0, 0, 0.35, 0.1]
d_all = [0, 0.17, 0.17, 0]


figure(1)
set(gcf, 'Position', [100, 100, 1200, 500])
hold on;
grid on;
set(gca, 'GridAlpha', 0.7);
set(gca, 'LineWidth', 1.1);
fontsize(gcf, 20, "points");
xlabel("время, с")
ylabel("угол, рад")
title("Сравнение регуляторов")
delt = 51
for j = 1:4
    
    p = p_all(j)
    i = i_all(j)
    d = d_all(j)
    data = readmatrix(strrep(sprintf('plots_data/PID' + string(p) + "_" + ...
        string(i) + "_" + string(d)), '.', '^') + ".txt")
    if (p == 0.5)
        time = data((1:end - delt-35), 1);
        angle = data((1:end - delt-35),2)*pi/180;
    else
        time = data((1:end - delt), 1);
        angle = data((1:end - delt),2)*pi/180;
    end
    plot(time, angle, "LineWidth", 2, "DisplayName", "p=" + p + ", i=" + i + ", d=" + d)
end
plot([0, 2.5],[100*pi/180, 100*pi/180], "LineStyle","--", "DisplayName","Целевое значение", "LineWidth",2)
plot([0, 2.5],[100*pi/180 * 1.05, 100*pi/180 * 1.05], "LineStyle","-", "DisplayName","Верхняя граница", "LineWidth",1.5, "Color","Black")
plot([0, 2.5],[100*pi/180 * 0.95, 100*pi/180 * 0.95], "LineStyle","-", "DisplayName","Нижняя граница", "LineWidth",1.5, "Color","Black")

legend("Location","eastoutside")
filename = "plots_data/ALL_reg"; 
filename = strrep(filename, '.', '^');
save2PDF(filename)
close all; clc; clear;

n=[1:20, 50]; lw = 2;
% 50 laminations results:
% M19:
lossesTrM19_50 = 0.0096; peakBTrM19_50 = 0.7727; 
lossesTHM19_50 = 0.0316; peakBTHM19_50 = 0.4158;
% Hiperco: 
lossesTrHip_50 = 0.0075; peakBTrHip_50 = 0.6460;
lossesTHHip_50 = 0.0252; peakBTHHip_50 = 0.3453;
%% M-19

load('solDataStaticM19.mat')
for i=1:length(solutionData)
    ByStM19(i)=solutionData(i).ByAvg;
end

load('solDataTHM19.mat')
for i=1:length(solutionData)
    IronOhmicLossesTHM19(i)=solutionData(i).TotalOhmicLosses;
    ByTHM19(i)=solutionData(i).ByAvg*sqrt(2);
end

load('solDataTransientM19.mat')
for i=1:length(solutionData)
    IronOhmicLossesTrM19(i)=solutionData(i).TotalOhmicLosses;
    ByTrM19(i)=solutionData(i).Bypeak;
end


figure
plot(n,[IronOhmicLossesTHM19,lossesTHM19_50],n,[IronOhmicLossesTrM19,lossesTrM19_50],'Linewidth',lw)
set(gca, 'FontName', 'TimesNewRoman','TickLabelInterpreter', 'latex');  
xlabel('Number of laminations','Interpreter','latex');
ylabel('Iron ohmic losses (W)','Interpreter','latex')
h1 = legend('Time-harmonic','Transient');
set (h1,'FontName','TimesNewRoman','Interpreter', 'latex');
title('M-19','Interpreter','latex')
grid on
saveas(gcf,[pwd '\PlotResults\Plot1'],'svg')

figure
plot(n,[ByStM19,1],n,[ByTHM19,peakBTHM19_50],n,[ByTrM19,peakBTrM19_50],'Linewidth',lw)
set(gca, 'FontName', 'TimesNewRoman','TickLabelInterpreter', 'latex');  
xlabel('Number of laminations','Interpreter','latex');
ylabel('Peak $|B_y|$ (T)','Interpreter','latex')
h1 = legend('Static','Time-harmonic','Transient');
set (h1,'FontName','TimesNewRoman','Interpreter', 'latex');
title('M-19','Interpreter','latex')
grid on
saveas(gcf,[pwd '\PlotResults\Plot2'],'svg')

%% Hiperco

load('solDataStaticHiperco.mat')
for i=1:length(solutionData)
    ByStHiperco(i)=solutionData(i).ByAvg;
end

load('solDataTHHiperco.mat')
for i=1:length(solutionData)
    IronOhmicLossesTHHiperco(i)=solutionData(i).TotalOhmicLosses;
    ByTHHiperco(i)=solutionData(i).ByAvg*sqrt(2);
end

load('solDataTransientHiperco.mat')
for i=1:length(solutionData)
    IronOhmicLossesTrHiperco(i)=solutionData(i).TotalOhmicLosses;
    ByTrHiperco(i)=solutionData(i).Bypeak;
end


figure
plot(n,[IronOhmicLossesTHHiperco,lossesTHHip_50],n,[IronOhmicLossesTrHiperco,lossesTrHip_50],'Linewidth',lw)
set(gca, 'FontName', 'TimesNewRoman','TickLabelInterpreter', 'latex');  
xlabel('Number of laminations','Interpreter','latex');
ylabel('Iron ohmic losses (W)','Interpreter','latex')
h1 = legend('Time-harmonic','Transient');
set (h1,'FontName','TimesNewRoman','Interpreter', 'latex');
ylim([0 0.4])
title('Hiperco','Interpreter','latex')
grid on
saveas(gcf,[pwd '\PlotResults\Plot3'],'svg')

figure
plot(n,[ByStHiperco,1],n,[ByTHHiperco,peakBTHHip_50],n,[ByTrHiperco,peakBTrHip_50],'Linewidth',lw)
set(gca, 'FontName', 'TimesNewRoman','TickLabelInterpreter', 'latex');
xlabel('Number of laminations','Interpreter','latex');
ylabel('Peak $|B_y|$ (T)','Interpreter','latex')
h1 = legend('Static','Time-harmonic','Transient');
set (h1,'FontName','TimesNewRoman','Interpreter', 'latex');
title('Hiperco','Interpreter','latex')
grid on
saveas(gcf,[pwd '\PlotResults\Plot4'],'svg')

%% Both materials

figure
plot(n,[IronOhmicLossesTrM19,lossesTrM19_50],n,[IronOhmicLossesTrHiperco,lossesTrHip_50],'Linewidth',lw)
set(gca, 'FontName', 'TimesNewRoman','TickLabelInterpreter', 'latex');
xlabel('Number of laminations','Interpreter','latex');
ylabel('Iron ohmic losses (W)','Interpreter','latex')
h1 = legend('M-19, transient','Hiperco, transient');
set (h1,'FontName','TimesNewRoman','Interpreter', 'latex');
% ylim([0 0.4])
grid on
saveas(gcf,[pwd '\PlotResults\Plot5'],'svg')

figure
plot(n,[ByTrM19,peakBTrM19_50],n,[ByTrHiperco,peakBTrHip_50],'Linewidth',lw)
set(gca, 'FontName', 'TimesNewRoman','TickLabelInterpreter', 'latex');
xlabel('Number of laminations','Interpreter','latex');
ylabel('Peak $|B_y|$ (T)','Interpreter','latex')
h1 = legend('M-19, transient','Hiperco, transient');
set (h1,'FontName','TimesNewRoman','Interpreter', 'latex');
grid on
saveas(gcf,[pwd '\PlotResults\Plot6'],'svg')

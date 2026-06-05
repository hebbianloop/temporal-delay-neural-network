filename='~/Desktop/potential_log.txt';
data=import_potential(filename,1,inf);

scalefactor=max(data(:,2))- max(data(:,2))/3;% scale amplitude window
ylim=max(data(:,2))+ max(data(:,2))/10;
figure('color',[1 1 1],'position',[0 0 2560 1389],'Visible','on');
subplot(2,1,1)
plot(data(1:300,2),'LineWidth',6)
hold on
%plot(stimtimes.*scalefactor,'LineWidth',5,'Color','k')
hold on
 plot(data(1:1000,5),'LineWidth',5,'LineStyle',':')
 set(gca,'xlim',[0 300])
 set(gca,'ylim',[0 ylim])
%set(gca,'XTickLabel',num2str(get(gca,'XTick').'))
%set(gca,'YTickLabel',num2str(get(gca,'YTick').'))
set(gca,'fontsize',60,'FontName','Computer Modern')
ylabel('Potential (a.u)','fontsize',62,'interpreter','latex')
title(sprintf('First Stimulus Presentations',presinwin),'fontsize',62,'interpreter','latex')

hold off
subplot(2,1,2)
plot(data(end-300:end,2),'LineWidth',6)
hold on
%plot(stimtimes.*scalefactor,'LineWidth',5,'Color','k')
hold on
 plot(data(end-300:end,5),'LineWidth',5,'LineStyle',':')
 set(gca,'xlim',[0 300])
 set(gca,'ylim',[0 ylim])
%set(gca,'XTickLabel',num2str(get(gca,'XTick').'))
%set(gca,'YTickLabel',num2str(get(gca,'YTick').'))
set(gca,'fontsize',60,'FontName','Computer Modern')
ylabel('Potential (a.u)','fontsize',62,'interpreter','latex')
title(sprintf('Test Stimulus Presentations'),'fontsize',62,'interpreter','latex')
hold off

filename='~/Desktop/weights.txt';

% import weights data
 data = import_weights(filename);

% calculate beta mixture across inputs
[betamix, ~] = calc_Betamix(data);

savepicshere=fullfile(dir,sprintf('%s-%s-%idelay-%idists_weights',trainortest,delayfunction, ...
    delaywin, numdistributions));
delaywin=0.2;           % delay window in seconds
% beta graphics
graphics_Betamix(betamix,savepicshere,delaywin,SGdata{2},format);


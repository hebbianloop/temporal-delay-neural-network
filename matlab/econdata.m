clf;

subplot(3,2,2,'align');
plot(dates, [rCPI, rDEF],'linewidth',5);
recessionplot;
dateaxis('x');
title('Inflation and GDP Deflator','interpreter','latex');
h = legend('CPI','DEF','Location','Best');
h.FontSize = 30;
h.Box = 'off';
axis([dates(1) - 600, dates(end) + 600, 0, 1]);
axis 'auto y'
set(gca,'fontsize',30,'FontName','Computer Modern')

subplot(3,2,3,'align');
plot(dates, [rWAGES, rHOURS],'linewidth',5);
recessionplot;
dateaxis('x');
title('Wages and Hours','interpreter','latex');
h = legend('WAGES','HOURS','Location','Best');
h.FontSize = 30;
h.Box = 'off';
axis([dates(1) - 600, dates(end) + 600, 0, 1]);
axis 'auto y'
set(gca,'fontsize',30,'FontName','Computer Modern')

subplot(3,2,4,'align');
plot(dates, [rCONS, rGCE],'linewidth',5);
recessionplot;
dateaxis('x');
title('Consumption','interpreter','latex');
h = legend('CONS','GCE','Location','Best');
h.FontSize = 30;
h.Box = 'off';
axis([dates(1) - 600, dates(end) + 600, 0, 1]);
axis 'auto y'
set(gca,'fontsize',30,'FontName','Computer Modern')
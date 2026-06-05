x=horzcat(rCPI, rDEF, rWAGES, rCONS, rGCE, rFED, ...
    rG10, rTB3, rUNEMP);

figure;imagesc(smoothRows(x',30))
set(gcf,'color',[1 1 1])
set(gca,'xticklabel',{[]})
set(gca,'yticklabel',{[]})

clf

figure('color',[1 1 1])

subplot(3,1,3,'align');
plot(dates, rUNEMP,'linewidth',5);
recessionplot;
dateaxis('x');
title('Unemployment','interpreter','latex');
h = legend('UNEMP','Location','Best');
h.FontSize = 30;
h.Box = 'off';
axis([dates(1) - 600, dates(end) + 600, 0, 1]);
%axis 'auto y'
set(gca,'fontsize',55,'FontName','Computer Modern')
set(gca,'ylim',[0 0.15])

subplot(3,1,1,'align');
plot(dates, [rINV],'linewidth',5);
recessionplot;
dateaxis('x');
title('Investment','interpreter','latex');
h = legend('INV','Location','Best');
h.FontSize = 30;
h.Box = 'off';
axis([dates(1) - 600, dates(end) + 600, 0, 1]);
axis 'auto y'
set(gca,'fontsize',55,'FontName','Computer Modern')
set(gca,'xticklabel',{[]})

subplot(3,1,2,'align');
plot(dates, [rFED, rG10, rTB3],'linewidth',5);
recessionplot;
dateaxis('x');
title('Interest Rates','interpreter','latex');
h = legend('FED','G10','TB3','Location','Best');
h.FontSize = 30;
h.Box = 'off';
axis([dates(1) - 600, dates(end) + 600, 0, 1]);
axis 'auto y'
set(gca,'fontsize',55,'FontName','Computer Modern')
set(gca,'xticklabel',{[]})
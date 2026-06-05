function graphics_Mesq(mweights,savehere,delaywin,F,format)

delaywin=delaywin*1000; % convert to ms

t=linspace(0,delaywin,size(mweights,2));

figure('color',[1 1 1],'position',[0 0 2560 1389]);
% Generate a contour plot
subplot(1,2,1)
contourf(mweights,'xdata',t,'ydata',F,'LineWidth',5)
set(gca,'fontsize',60,'FontName','Computer Modern')
xlabel('Relative Time (ms)','fontsize',62,'interpreter','latex');
ylabel('Frequency (Hz)','fontsize',62,'interpreter','latex')
% Generate a 3D curve
% m1=meshgrid(t,F);
% m2=meshgrid(F,t);
subplot(1,2,2)
% fill3(m2,m1',betamix',betamix','facealpha',0.8,'facelighting','gouraud', ...
%     'LineWidth',5);
%mesh(betamix,'xdata',t,'ydata',F,'FaceAlpha',0.8,'facelighting','gouraud', ...
%    'LineWidth', 5);
surf(mweights,'xdata',t,'ydata',F, 'facelighting','gouraud', ...
    'LineWidth', 5, 'EdgeColor','none');
colormap parula
% h= plot3(m2, m1',betamix','LineWidth',5); %plotted so time is continuous curve
grid on
set(gca,'XMinorGrid','on','YMinorGrid','on','ZMinorGrid','on')
set(gca, 'YTickLabel',{}, 'ZTickLabel',{},'XTickLabel',{},'TickLength',[0 0])
view(130,30)

% print results to datafileectory
export_fig(['mesq-' savehere '-wmesh' '.' format], ['-' format])
%print(gcf, '-dpdf', 'simulations/simple-images/chevron-l_SNRNaN_500pres/weights.pdf'); 
function [train,test] = graphics_potential_trainvstest(train,test, ts_training, ts_testing, stimtimes_training, stimtimes_testing, stimduration_training, stimduration_testing, savehere,printformat)

% -------------------------------------------------------------------------
%%                              TRAINING
%
% Set Parameters for Training Plot
data=train;
ts=ts_training;
stimtimes=stimtimes_training;
stimduration=stimduration_training;
	% Duration of dataset in ms
	dataset_duration=ts.TimeInfo.End*1000;
	% Add one point for 0
	dataset_duration=dataset_duration+1;
	% Number of iterations in dataset
	numiterations=size(data,1)/dataset_duration;
	% Generate stimulus times for entire time course (include iterations)
	stimtimes=repmat(stimtimes_training,1,uint16(numiterations));
	% scale stimtimes (so y axis is not too large)
	scalefactor=max(data(:,2))- max(data(:,2))/3 ;
	% scale plotting window in time
	presinwin=10;
	tmax=(stimduration*presinwin)+(100*presinwin);
	% scale amplitude window
	ylim=max(data(:,2))+ max(data(:,2))/10;
% ---------------------------------------------------------------------------
% MAKE A 2x2 SUBPLOT WITH FIRST AND LAST SET OF PRESENTATIONS FOR TRAIN & TEST
% ---------------------------------------------------------------------------
% plot first N pres
%%%%%%%%%%%%%%%%%%%%%%%%
figure('color',[1 1 1],'position',[0 0 2560 1389],'visible','off'); subplot(2,2,1);

% plot noncontributing
%plot(data(size(data,1)/dataset_duration*numiterations:dataset_duration*numiterations,3),'LineWidth',6)
%hold on

% plot contributing
plot(data(size(data,1)/dataset_duration*numiterations:dataset_duration*numiterations,2),'LineWidth',6)
hold on

% plot stimulus times
%area(stimtimes.*scalefactor,'LineWidth',5,'Color','k','facealpha',.5)
plot(stimtimes.*scalefactor,'LineWidth',5,'Color','k')
hold on

% plot threshold
plot(data(size(data,1)/dataset_duration:dataset_duration*numiterations,5),'LineWidth',5,'LineStyle',':')

% set figure & axis properties
set(gca,'xlim',[0 tmax])
set(gca,'ylim',[0 ylim])
set(gca,'XTickLabel',num2str(get(gca,'XTick').'))
set(gca,'YTickLabel',{})
%set(gca,'YTickLabel',num2str(get(gca,'YTick').'))
set(gca,'fontsize',60,'FontName','Computer Modern')
ylabel('Potential (a.u)','fontsize',62,'interpreter','latex')
title(sprintf('\bFirst %d Stimulus Presentations',presinwin),'fontsize',62,'interpreter','latex')
hold off

%%%%%%%%%%%%%%%%%%%%%%%%
% plot last N pres
%%%%%%%%%%%%%%%%%%%%%%%%

subplot(2,2,2)

% plot contributing
plot(data(end-dataset_duration*numiterations+1:end,2),'LineWidth',6)
hold on

% plot stimulus times
plot(stimtimes.*scalefactor,'LineWidth',5,'Color','k')
hold on

% plot threshold
plot(data(end-dataset_duration*numiterations+1:end,5),'LineWidth',5,'LineStyle',':')

% set figure & axis properties
set(gca,'ylim',[0 ylim])
set(gca,'xlim',[(dataset_duration*numiterations)-tmax dataset_duration*numiterations])
set(gca,'XTick',round(linspace((dataset_duration*numiterations)-tmax, dataset_duration*numiterations, 4)))
set(gca,'YTickLabel',{})
%set(gca,'YTickLabel',num2str(get(gca,'YTick').'))
set(gca,'XTickLabel',num2str((get(gca,'XTick')).'))
set(gca,'fontsize',60,'FontName','Computer Modern')
title(sprintf('\bLast %d Stimulus Presentations',presinwin),'fontsize',62,'interpreter','latex')
xlabel('Time (ms)','fontsize',62,'interpreter','latex');
hold off

% -------------------------------------------------------------------------
%% 								TESTING
%% 
% Set Parameters for Testing Plot
data=test;
ts=ts_testing;
stimtimes=stimtimes_testing;
stimduration=stimduration_testing;
	% Duration of dataset in ms
	dataset_duration=ts.TimeInfo.End*1000;
	% Add one point for 0
	dataset_duration=dataset_duration+1;
	% Number of iterations in dataset
	numiterations=size(train,1)/dataset_duration;
	% Generate stimulus times for entire time course (include iterations)
	stimtimes=repmat(stimtimes_training,1,uint16(numiterations));
	% scale stimtimes (so y axis is not too large)
	scalefactor=max(train(:,2))- max(train(:,2))/3 ;
	% scale plotting window in time
	presinwin=10;
	tmax=(stimduration_training*presinwin)+(100*presinwin);
	% scale amplitude window
	ylim=max(train(:,2))+ max(train(:,2))/10;
% ---------------------------------------------------------------------------
% plot first N pres
%%%%%%%%%%%%%%%%%%%%%%%%
subplot(2,2,3)

% plot noncontributing
%plot(data(size(data,1)/dataset_duration*numiterations:dataset_duration*numiterations,3),'LineWidth',6)
%hold on

% plot contributing
plot(data(size(data,1)/dataset_duration:dataset_duration,2),'LineWidth',6)
hold on

% plot stimulus times
%area(stimtimes.*scalefactor,'LineWidth',5,'Color','k','facealpha',.5)
plot(stimtimes.*scalefactor,'LineWidth',5,'Color','k')
hold on

% plot threshold
plot(data(size(data,1)/dataset_duration:dataset_duration,5),'LineWidth',5,'LineStyle',':')

% set figure & axis properties
set(gca,'xlim',[0 tmax])
set(gca,'ylim',[0 ylim])
set(gca,'XTickLabel',num2str(get(gca,'XTick').'))
set(gca,'YTickLabel',{})
%set(gca,'YTickLabel',num2str(get(gca,'YTick').'))
set(gca,'fontsize',60,'FontName','Computer Modern')
ylabel('Potential (a.u)','fontsize',62,'interpreter','latex')
%title(sprintf('\bTe',presinwin),'fontsize',62,'interpreter','latex')
hold off

%%%%%%%%%%%%%%%%%%%%%%%%
% plot last N pres
%%%%%%%%%%%%%%%%%%%%%%%%
subplot(2,2,4)

%plot contributing
plot(data(end-dataset_duration+1:end,2),'LineWidth',6)
hold on

% plot stimulus times as boxcar
plot(stimtimes.*scalefactor,'LineWidth',5,'Color','k')
hold on

% plot threshold
plot(data(end-dataset_duration+1:end,5),'LineWidth',5,'LineStyle',':')


%set figure & axis properties
set(gca,'ylim',[0 ylim])
set(gca,'xlim',[(dataset_duration)-tmax dataset_duration])
set(gca,'XTick',round(linspace((dataset_duration)-tmax, dataset_duration, 4)))
set(gca,'YTickLabel',{})
%set(gca,'YTickLabel',num2str(get(gca,'YTick').'))
set(gca,'XTickLabel',num2str((get(gca,'XTick')).'))
set(gca,'fontsize',60,'FontName','Computer Modern')
%title(sprintf('\bLast %d Stimulus Presentations',presinwin),'fontsize',62,'interpreter','latex')
xlabel('Time (ms)','fontsize',62,'interpreter','latex');
hold off

%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% print results
export_fig([savehere '.' printformat], ['-' printformat])
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
close

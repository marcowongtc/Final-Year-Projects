clc; clear all; close all;

group = {'01-GC';'02-Swap'};
groupn = ["Natural G/C";"-1/+1-swap"];

for k = 1:2       
    data(:,:,k) = dlmread(strcat(group{k},'/mindisres.xvg'),'',24,1);
end

data = data * 10;

%% Preprocessing
cutoff = 5; % remove residue candidates with heavy-atom min distance > 5Å
idxorig = find(sum(data<cutoff,[1 3])); % no frequency filter

datamerge = [data(:,:,1);data(:,:,2)];

dataNorm = normalize(1./datamerge); % Normalization
[R,P] = corrcoef(dataNorm);
relatmat = triu(R,1);

%% Logistic regression
iptglob = [];

% train the model 10 times with randomly chosen features for statistics
for t = 1:10
    % randomly choose elements
    i = 1; idxrelat = [];
    while i <= size(relatmat,1)
        if ismember(i,idxrelat)
            i = i+1;
            continue;
        end
        tmp = [i,find(abs(relatmat(i,:))>0.9)];
        idxrelat = union(idxrelat, randsample(tmp,length(tmp)-1));
        i = i+1;
    end
    
    idx = setdiff(idxorig,idxrelat); 
    datamerge = [data(:,idx,1);data(:,idx,2)];
    
    X = normalize(1./datamerge);
    Y = [ones(size(data,1),1);zeros(size(data,1),1)];
    
    cvp = cvpartition(size(Y,1),'HoldOut',0.4);
    
    idxTrain = training(cvp); % Extract training set indices
    X = X'; lambda = logspace(-6,-0.5,length(idx));
    Mdl = fitclinear(X(:,idxTrain),Y(idxTrain),'ObservationsIn','columns', ...
        'Learner','logistic','Regularization','lasso','Solver','sparsa', ...
        'Lambda',lambda,'GradientTolerance',1e-8);
     
    idxTest = test(cvp); % Extract test set indices
    labels = predict(Mdl,X(:,idxTest),'ObservationsIn','columns');
    L = loss(Mdl,X(:,idxTest),Y(idxTest),'ObservationsIn','columns');
    
    importance = zeros(1,size(data,2));
    importance(idx) = abs(Mdl.Beta(:,1));
    importance = normalize(reshape(importance,[590 int64(size(data,2)/590)]))';
    iptorig = sum(importance,'omitnan');
    ipt = normalize(iptorig,'range');
    
    iptglob(t,:) = ipt;

end

ipt = mean(iptglob);

figure('Position', [500 500 800 300]); hold on; box off;

plot(35:329,ipt(:,1:295),'LineWidth',1.5);
set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
xlim([35 329]); ylim([-0.1 1.1]);
hold off;

figure('Position', [500 500 800 300]); hold on; box off;

plot(35:329,ipt(:,296:590),'LineWidth',1.5);
set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
xlim([35 329]); ylim([-0.1 1.1]);
hold off;

%% Random forest
iptglob = [];

% train the model 10 times with randomly chosen features for statistics
for t = 1:10
    % randomly choose elements
    i = 1; idxrelat = [];
    while i <= size(relatmat,1)
        if ismember(i,idxrelat)
            i = i+1;
            continue;
        end
        tmp = [i,find(abs(relatmat(i,:))>0.9)];
        idxrelat = union(idxrelat, randsample(tmp,length(tmp)-1));
        i = i+1;
    end

    idx = setdiff(idx,idxrelat); 
    n = size(data,1); datamerge = [data(:,idx,1);data(:,idx,2)];
    
    X = normalize(1./datamerge);
    Y = [ones(n,1);zeros(n,1)];
    
    cvp = cvpartition(size(Y,1),'HoldOut',0.4);
    
    idxTrain = training(cvp); % Extract training set indices
    Mdl = TreeBagger(500,X(idxTrain,:),Y(idxTrain),'OOBPrediction','On',...
        'Method','classification','OOBPredictorImportance','on', ...
        'MaxNumSplits',60,'NumPredictorsToSample',50);
%     view(Mdl.Trees{1},'Mode','graph')
%     
%     figure;
%     oobErrorBaggedEnsemble = oobError(Mdl);
%     plot(oobErrorBaggedEnsemble,'LineWidth',1.5);
%     xlabel 'Number of grown trees';
%     ylabel 'Out-of-bag classification error';
%     set(gca,'linewidth',2,'FontSize',16,'FontWeight','normal');
    
    importance = zeros(1,size(data,2));
    importance(idx) = Mdl.OOBPermutedPredictorDeltaError;
    importance = normalize(reshape(importance,[590 int64(size(data,2)/590)]))';
    iptorig = sum(importance,'omitnan');
    ipt = normalize(iptorig,'range');

    iptglob(t,:) = ipt;

end

ipt = mean(iptglob);

figure('Position', [500 500 800 300]); hold on; box off;

plot(35:329,ipt(:,1:295),'LineWidth',1.5);
set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
xlim([35 329]); ylim([-0.1 1.1]);
hold off;

figure('Position', [500 500 800 300]); hold on; box off;

plot(35:329,ipt(:,296:590),'LineWidth',1.5);
set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
xlim([35 329]); ylim([-0.1 1.1]);
hold off;


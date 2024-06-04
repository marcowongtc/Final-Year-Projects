%% Read data file
%%%%
clc; clear all; close all;

group = {'GC';'Swap'};
groupn = ["Natural G/C";"-1/+1-swap"];

for k = 1:2
    data(:,:,k) = dlmread(strcat('mindisres-', group{k}, '.xvg'),'',24,1);
end

data = data * 10; % nm to angstrom for gromacs

%% Param Tweaking
%%
% remove residue candidates with heavy-atom min distance > :: default: 5Å
distance_cutoff = 5; 

% number of iterations on training & shuffling :: default: 20
n_iteration = 20

% correlation filtering during shuffle :: default: 0.9
correlation_cutoff = 0.9

% cvpartition test:train ratio :: default: 0.4
partition_ratio = 0.4

model = 'lr'
% model = 'rf'

%% model specific params
% linear regression
regularization = 'lasso'    % :: default: lasso, check docs for available options
solver = 'sparsa'           % :: default: sparsa, check docs for available options
tolerance = 1e-8            % :: default: 1e-8
lambda_a = -6               % :: default: -6
lambda_b = -0.5             % :: default: -0.5

% random forest
n_trees = 500               % :: default: 500
max_splits = 60             % :: default: 60
n_predictor_samples = 50    % :: default: 50

%% File
% base file path for figure saving
base_path = 'C:/Users/Bono/Documents/MATLAB' % please change to your workspace

% can modify file name based on your params
fname = sprintf('%s/%s-model_%d-iter_%.1f-dist_%.1f-corr.png', base_path, model, n_iteration, distance_cutoff, correlation_cutoff);

%% Preprocessing
%%
idxorig = find(sum(data<distance_cutoff,[1 3]));

datamerge = [data(:,:,1);data(:,:,2)];

dataNorm = normalize(1./datamerge);
[R,P] = corrcoef(dataNorm); % expensive part
relatmat = triu(R,1);

%% Logistic regression
%%
if model == 'lr'
    iptglob = [];
    
    % train the model n_iteration times with randomly chosen features for statistics
    for t = 1:n_iteration
          % randomly choose elements
        i = 1; idxrelat = [];
        while i <= size(relatmat,1)
            if ismember(i,idxrelat)
                i = i+1;
                continue;
            end
            tmp = [i,find(abs(relatmat(i,:))>correlation_cutoff)];
            idxrelat = union(idxrelat, randsample(tmp,length(tmp)-1));
            i = i+1;
        end
        
        idx = setdiff(idxorig,idxrelat); 
        datamerge = [data(:,idx,1);data(:,idx,2)];
        
        X = normalize(1./datamerge);
        Y = [ones(size(data,1),1);zeros(size(data,1),1)];
        
        cvp = cvpartition(size(Y,1),'HoldOut',partition_ratio);
        
        idxTrain = training(cvp); % Extract training set indices
        X = X'; 
        lambda = logspace(lambda_a,lambda_b,length(idx));

        Mdl = fitclinear(X(:,idxTrain),Y(idxTrain),'ObservationsIn','columns', ...
            'Learner','logistic','Regularization',regularization,'Solver',solver, ...
            'Lambda',lambda,'GradientTolerance',tolerance);
         
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
end


%% Random forest
if model == 'rf'
    iptglob = [];
    
    % train the model 10 times with randomly chosen features for statistics
    % for t = 1:10
    for t = 1:2
        % randomly choose elements
        i = 1; idxrelat = [];
        while i <= size(relatmat,1)
            if ismember(i,idxrelat)
                i = i+1;
                continue;
            end
            tmp = [i,find(abs(relatmat(i,:)) > correlation_cutoff)];
            idxrelat = union(idxrelat, randsample(tmp,length(tmp)-1));
            i = i+1;
        end
        
        idx = setdiff(idxorig,idxrelat);
        n = size(data,1); datamerge = [data(:,idx,1);data(:,idx,2)];
        
        X = normalize(1./datamerge);
        Y = [ones(n,1);zeros(n,1)];
        
        cvp = cvpartition(size(Y,1),'HoldOut',partition_ratio);
        
        idxTrain = training(cvp); % Extract training set indices
        Mdl = TreeBagger(n_trees,X(idxTrain,:),Y(idxTrain),'OOBPrediction','On',...
            'Method','classification','OOBPredictorImportance','on', ...
            'MaxNumSplits', max_splits,'NumPredictorsToSample', n_predictor_samples);
        
        importance = zeros(1,size(data,2));
        importance(idx) = Mdl.OOBPermutedPredictorDeltaError;
        importance = normalize(reshape(importance,[590 int64(size(data,2)/590)]))';
        iptorig = sum(importance,'omitnan');
        ipt = normalize(iptorig,'range');
        
        iptglob(t,:) = ipt;
    end
end

ipt = mean(iptglob);

%% Draw figures from loaded data
figure('Position', [500 500 800 300]); hold on; box off;

plot(35:329,ipt(:,1:295),'LineWidth',1.2);
set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
xlim([35 329]); ylim([-0.1 1.1]);

ftitle = sprintf('%s %d-iter %.1f-dist %.1f-corr',model,  n_iteration, distance_cutoff, correlation_cutoff);
title(ftitle, FontSize = 16)
xlabel('residue', FontSize = 13)
ylabel('importance', FontSize = 13)

p = plot(35:329,ipt(:,296:590),'LineWidth',1.2);
hold off;

% setup peak comparison to known important residues
% known_importance = [54, 144, 221, 252, 285];  % To compare with our value
% text_values = num2str(text_positions.');
% max_values = max(ipt(:, 1:295), ipt(:, 296:590));  % Find maximum values along each chain
% text(known_importance, max_values(known_importance - 34) + .05, text_values, 'HorizontalAlignment', 'center');

lgd = legend('chain-1','chain-2')
lgd.FontSize = 12

saveas(gca, fname, 'png')
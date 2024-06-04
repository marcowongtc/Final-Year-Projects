%% Read data file
%%%%
clc; clear all; close all;

group = {'01-GC';'02-Swap'};
groupn = ["Natural G/C";"-1/+1-swap"];

for k = 1:2
    data(:,:,k) = dlmread(strcat(group{k},'/mindisres.xvg'),'',24,1);
end

data = data * 10; % nm to angstrom for gromacs

%% Param Tweaking
%%
% remove residue candidates with heavy-atom min distance > :: default: 5Å
distance_cutoff = 5; 

% number of iterations on training & shuffling :: default: 20
n_iteration = 20;

% correlation filtering during shuffle :: default: 0.9
correlation_cutoff_list = [0.55, 0.65, 0.75, 0.85, 0.95];

% cvpartition test:train ratio :: default: 0.4
partition_ratio = 0.4;

% model
model_list = ["lr", "rf"];

%% model specific params
% linear regression
regularization = 'lasso';    % :: default: lasso, check docs for available options
solver = 'sparsa';           % :: default: sparsa, check docs for available options
tolerance = 1e-8;            % :: default: 1e-8
lambda_a = -6;               % :: default: -6
lambda_b = -0.5;             % :: default: -0.5

% random forest
n_trees = 500;               % :: default: 500
max_splits = 60;             % :: default: 60
n_predictor_samples = 50;    % :: default: 50

%% File
% base file path for figure saving
base_path = 'W:/home/marco/projects/FYP/result/Standard/correlation/temp'; % please change to your workspace



%csv parameter
ID_list = 35:329;
ID_list = reshape(ID_list, [size(ID_list,2), 1]);
temp_idx_size = 0;



for model = model_list

    idxsize_list = [];

    for correlation_cutoff = correlation_cutoff_list

        % can modify file name based on your params
        fname1 = sprintf('%s/%s-model_%d-iter_%.1f-dist_%.2f-corr.png', base_path, model, n_iteration, distance_cutoff, correlation_cutoff);
        fname1_chain1 = sprintf('%s/%s-model_%d-iter_%.1f-dist_%.2f-corr_1-chain.png', base_path, model, n_iteration, distance_cutoff, correlation_cutoff);
        fname1_chain2 = sprintf('%s/%s-model_%d-iter_%.1f-dist_%.2f-corr_2-chain.png', base_path, model, n_iteration, distance_cutoff, correlation_cutoff);
        
        fname_csv_chain1 = sprintf('%s/%s-model_%d-iter_%.1f-dist_%.2f-corr_chain1.csv', base_path, model, n_iteration, distance_cutoff, correlation_cutoff);
        fname_csv_chain2 = sprintf('%s/%s-model_%d-iter_%.1f-dist_%.2f-corr_chain2.csv', base_path, model, n_iteration, distance_cutoff, correlation_cutoff);
        fname_csv_ipxsize = sprintf('%s/%s-model_%d-iter_%.2f-dist_idxsize_against_correlation.csv', base_path, model, n_iteration, distance_cutoff);



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
                
                %for idx_size comparison
                temp_idx_size = size(idx, 2);
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

                %for idx_size comparison
                temp_idx_size = size(idx, 2);
            end
        end

        ipt = mean(iptglob);



        %csv writing | chain 1 & chain 2 importance profile
        ipt_column = reshape(ipt, [size(ipt,2), 1]);
        disp(size(ID_list))
        disp(size(ipt_column(1:295)))


        ipt_chain1 = [ID_list, ipt_column(1:295)];
        ipt_chain2 = [ID_list, ipt_column(296:590)];
        csvwrite(fname_csv_chain1, ipt_chain1);
        csvwrite(fname_csv_chain2, ipt_chain2);
    
        idxsize_list = [idxsize_list, temp_idx_size];








        %% Draw figures from loaded data
        figure('Position', [500 500 800 300]); hold on; box off;

        plot(35:329,ipt(:,1:295),'LineWidth',1.2);
        set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
        xlim([35 329]); ylim([-0.1 1.1]);

        ftitle = sprintf('%s %d-iter %.1f-dist %.2f-corr',model,  n_iteration, distance_cutoff, correlation_cutoff);
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

        lgd = legend('chain-1','chain-2');
        lgd.FontSize = 12;

        saveas(gca, fname1, 'png');
        
        



        figure('Position', [500 500 800 300]); hold on; box off;

        plot(35:329,ipt(:,1:295),'LineWidth',1.5);
        set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
        xlim([35 329]); ylim([-0.1 1.1]);

        ftitle = sprintf('%s %d-iter %.1f-dist %.2f-corr 1-chain',model,  n_iteration, distance_cutoff, correlation_cutoff);
        title(ftitle, FontSize = 16)
        xlabel('residue', FontSize = 13)
        ylabel('importance', FontSize = 13)

        hold off;

        saveas(gca, fname1_chain1, 'png');




        figure('Position', [500 500 800 300]); hold on; box off;

        plot(35:329,ipt(:,296:590),'LineWidth',1.5);
        set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
        xlim([35 329]); ylim([-0.1 1.1]);

        ftitle = sprintf('%s %d-iter %.1f-dist %.2f-corr 2-chain',model,  n_iteration, distance_cutoff, correlation_cutoff);
        title(ftitle, FontSize = 16)
        xlabel('residue', FontSize = 13)
        ylabel('importance', FontSize = 13)

        hold off;

        saveas(gca, fname1_chain2, 'png');



    
    end

    %csv writing | idx size against correlation
    correlation_cutoff_csv_list = reshape(correlation_cutoff_list, [size(correlation_cutoff_list,2), 1]);
    idxsize_list = reshape(idxsize_list, [size(idxsize_list,2), 1]);
    idxsize_list = [correlation_cutoff_csv_list, idxsize_list];
    csvwrite(fname_csv_ipxsize, idxsize_list);






end
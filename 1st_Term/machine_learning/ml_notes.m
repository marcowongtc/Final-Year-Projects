clc; clear all; close all;

group = {'01-GC';'02-Swap'};
groupn = ["Natural G/C";"-1/+1-swap"];

% 
% data = 3d array with 2 layer - GC and Swap (2d array) | data extracted from mindires.xvg file starting from row=24, column=1 
% 

for k = 1:2
    %-----------------------------------------------------
    % dlmread(): read numeric data from a delimited text file
    % data = dlmread('filename.txt', delimiter, R, C);
    % R/C: row column indices to start to read
    % -----------------------------------------------------
    % strcat(): concantenate the strings together
    % output: 01-GC/mindires.xvg, 02-Swap/mindires.xvg
    % -----------------------------------------------------
    % data(:,:,k): Access the slice at index k of 3D array
    % : = access all, k: specific indeex in third dimension
    % disp(data) -> show all layer of data 
    % -----------------------------------------------------
    data(:,:,k) = dlmread(strcat(group{k},'/mindisres.xvg'),'',24,1);
end

% 
% all data times 10
% 
data = data * 10;


% *****************************************************
% %% = section marker for matlab
% % = comment

%% Preprocessing

% -----------------------------------------------------
% data<cutoff : return a array with 1 (true) where the condition is satisfied and 0 (false) when condition is not satisfied
% sum(_____, [1,3]) : sum up data along 1st and 3rd dimension, fix 2nd dimension each time like suming a slice with fix index of 2nd dimension
% eg: sum(ones(4,2,3), [1,3]) -> [12, 12]
% 

% -----------------------------------------------------
% find(): locate the indices of non-zero or non-false elements in an array, return indices in a column vector
% indices here is the index of flatten array (if 3d -> 1d, eg: 2*2 array [1,1]-> 4)
% 
% -----------------------------------------------------
% -----------------------------------------------------
% Purpose:
% cutoff 
% min distance > 5Å | = 0
% min distance <= 5Å | = 1
% 
% sum
% fix type of residue-nucleobisis (2nd dimension)
% sum = number of datapoint (difference: different time + different protein GC/Swap) of same residue-nucleobisis min distance <= 5Å
% 
% find
% locate which residue-nucleobisis has min distance <= 5Å (condition)
% index return = column number in mindisres.xvg | represent residue-nucleobisis
% here we don't care the frequency of condition | one time / many time = yes 
% 
% -----------------------------------------------------
% -----------------------------------------------------
cutoff = 5; % remove residue candidates with heavy-atom min distance > 5Å
idxorig = find(sum(data<cutoff,[1 3])); % no frequency filter



% -----------------------------------------------------
%  [data ; data] -> merge two page of data to one page | insert into subsequent row
%  page here means slice of 1st and 2nd dimension consisted 
% -----------------------------------------------------
datamerge = [data(:,:,1);data(:,:,2)];


% -----------------------------------------------------
% normalize() -> change all data to max = 1 | range from 0 to 1
% -----------------------------------------------------
% [R,P] = corrcof(A) 
%  measure correlation of variable
% 
%  A: each column = a seperate variable | in fixed column, each row = observation change in a order
%  eg: [4*3] -> 3 seperate varible, each containing 4 data points
%  Aim: compare the correlation / linearity between variables 
% -> ↑↑/↓↓ = positive correlated linearly | if all data lies on a line = 1
% -> ↑↓/↓↑ = negative correlated linearly | if all data lies on a line = -1
% -> ↑-/↓- = uncorrelated | = 0
% -> if it is deviated from linear relation | inbetween 
% 
% R: matrix of correlation coefficient 
% -> index [m,n] = corr coef between mth + nth column variable 
% -> ** symmentric matrix | eg: [2,3] = [3,2] **
% -> [n,n] must be 1 (same variable data comparison)
% 
% P: matrix of p value | Measure of probability that an observed difference occured just by random chance
% -> ** symmentric matrix | eg: [2,3] = [3,2] **
% -----------------------------------------------------
% triu(R,1)
% extract the upper triangular part of matrix | lower trigular part = 0, 1 - also make diagnal term to zero
% here we know correlation matrix = symmentric + diagnol: no meaning (compare itself) 
% => only keep upper triangular part
% -----------------------------------------------------
dataNorm = normalize(1./datamerge); % Normalization
[R,P] = corrcoef(dataNorm);

% relate matrix
relatmat = triu(R,1);




% *****************************************************
%% Logistic regression
iptglob = [];

% train the model 10 times with randomly chosen features for statistics


for t = 1:10
    % randomly choose elements
    i = 1; idxrelat = [];

    % -----------------------------------------------------
    % size(A,1): size in 1st dimension (row)
    % 
    % ismember(i, idxrelat): 
    % output true/flase | checks if the element i is present in the array idxrelat
    % 
    % union(A,B): 
    % output a new array | contains all element of A, B without any duplicated element
    % -> [1,2,3] [2,3,4] -> [1,2,3,4]
    % 
    % randsample(A, n): 
    % output a new array | randomly select n elements from array A without replacement
    % -> [1,6,8,9] | randsample(A,3) -> [9,1,6]
    % 
    % setdiff(A,B): 
    % output new array | set difference of two array i.e. elements that does not apperead in both array
    % identify unique value that are not present in another array
    % -> [1,2,3,4,5] [3,4,5] -> [1,2]
    % 
    % ones(m,n) / zeros(m,n): 
    % output array of 1 / 0 with dimension m*n
    % 
    % -----------------------------------------------------


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

    % -----------------------------------------------------
    % cvpartition(n, 'HoldOut', 0.4)
    % output = cross-validation partition object (cvp object)
    % -> n : total number of observation in dataset
    % -> HoldOut : divide the data into two set | training set + test set
    % -> 0.4 : proportion of data allocated to test set 
    % 
    % -----------------------------------------------------   


    cvp = cvpartition(size(Y,1),'HoldOut',0.4);

    % -----------------------------------------------------   
    % training(cvp)
    % extract training set indices in cvp object
    % 
    % test(cvp)
    % extract test set indices in cvp object
    % ----------------------------------------------------
    
    % ----------------------------------------------------
    % logspace(a,b,n)
    % output: array | generates n points between 10^a and 10^b
    % 
    % 
    % ----------------------------------------------------
    % fitclinear(X, Y)
    % **** train linear classification model by fitclinear
    % -> X: Training Set (2d) 
    % -> Y: Label (1d) 
    % column as different R<->N ID
    % 
    % 
    % X(:,[1,3,4]) - subset of X with original column of 1,3,4 index included | 2D
    % Y([1,3,4]) - subset of Y with origianl index 1,3,4 included | 1D
    % 
    % 
    % 
    % 'ObservationsIn', 'columns' 
    % -> specifies that the observations are arranged in columns.
    % 
    % 'Learner', 'logistic' 
    % -> Learning Algorithm: Logistic regression 
    % 
    % 'Regularization', 'lasso' 
    % -> Redularization: L1 regularization (lasso)
    % 
    % 'Solver', 'sparsa' 
    % -> Optimiztion: SPARSA algorithm | solver
    % 
    % 'Lambda', lambda 
    % -> Regularization parameter values: lambda
    % 
    % 'GradientTolerance', 1e-8 
    % -> Tolerance for the termination criterion based on the gradient magnitude
    % 
    % ----------------------------------------------------



    % training set
    idxTrain = training(cvp); % Extract training set indices
    X = X'; % transpose X
    lambda = logspace(-6,-0.5,length(idx));
    Mdl = fitclinear(X(:,idxTrain),Y(idxTrain),'ObservationsIn','columns', ...
        'Learner','logistic','Regularization','lasso','Solver','sparsa', ...
        'Lambda',lambda,'GradientTolerance',1e-8);
    


    % ---------------------------------------------------- 
    % predict(Mdl, A)
    % predict the label for test set using trained model 
    % -> Mdl : Trained model
    % -> A : test set 
    % 
    % 
    % loss(Mdl, A, LA)
    % calculate classification error of trained model
    % -> Mdl : Trained model
    % -> A : test set 
    % -> LA : true label of test set
    % 
    % ----------------------------------------------------    
        

    % test set
    idxTest = test(cvp); % Extract test set indices
    labels = predict(Mdl,X(:,idxTest),'ObservationsIn','columns');
    L = loss(Mdl,X(:,idxTest),Y(idxTest),'ObservationsIn','columns');



    % ---------------------------------------------------- 
    % Mdl.Beta
    % coefficient matrix of model
    % nth row: coefficient value of nth feacture
    % 
    % abs(Mdl.Beta)
    % absolute value | importance / contribution of feature to model's prediction
    % 
    % ---------------------------------------------------- 
    % reshape
    % row no. : 590 - feature number 
    % 
    % sum(importance,'omitnan')
    % sum up all importance across each row (one feature) | omitting NaN
    % 
    % normalize(iptorig,'range')
    % range = ensure normalized to range [0,1]
    % if x range = normalize by making the vector magnitude as 1 
    % ----------------------------------------------------   


    importance = zeros(1,size(data,2));
    importance(idx) = abs(Mdl.Beta(:,1));
    importance = normalize(reshape(importance,[590 int64(size(data,2)/590)]))';
    iptorig = sum(importance,'omitnan');
    ipt = normalize(iptorig,'range');
    
    iptglob(t,:) = ipt;

end

%end training and testing, also has the imporatance array with its time


ipt = mean(iptglob);

% ---------------------------------------------------- 
% figure()
% create a new figure window 
% 
% 'Position', [left bottom width height]
% left: horizontal position | from upper left corner of figure window
% bottom: vertical position | from upper left corner of figure window
% width/height: width and height of the figure
% 
% hold on
% hold state | subsequent plot commands will add ot exisitng plot instead of replacing
%
% box off
% reomove bounding box outline the plot area | no visible line forming a box around the plot 
% 
% ---------------------------------------------------- 


%1st plot for ipt [1:259] | 294 feature
figure('Position', [500 500 800 300]); hold on; box off;

% ---------------------------------------------------- 
% plot(x axis, y axis)
% -> x axis: 35:329 with a step size of 1
% -> y axis: ipt(:,1:295) | ipt 1*590 row vector, each column entities 
% 
% LineWidth',1.5
% set thickness of line in the plot
% ---------------------------------------------------- 
% set(gca,)
% set propeties of current axes (gca)
% 
% 'linewidth',2
% set thickness of axes line
% 
% FontSize',18,'FontWeight','normal'
% set axes labels font
% 
% ---------------------------------------------------- 
% xlim([x0 xmax]) ylim([y0 ymax])
% set range of x and y
% 
% hold off
% release hold on | subsequent plot commands will create a new plot
% 
% ---------------------------------------------------- 


plot(35:329,ipt(:,1:295),'LineWidth',1.5);
set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
xlim([35 329]); ylim([-0.1 1.1]);
hold off;


%2nd plot for ipt [296:590] | 294 feature
figure('Position', [500 500 800 300]); hold on; box off;


plot(35:329,ipt(:,296:590),'LineWidth',1.5);
set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
xlim([35 329]); ylim([-0.1 1.1]);
hold off;






% *****************************************************
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

    idx = setdiff(idxorig,idxrelat); %changed!!!
    n = size(data,1); datamerge = [data(:,idx,1);data(:,idx,2)];
    
    X = normalize(1./datamerge);
    Y = [ones(n,1);zeros(n,1)];
    
    cvp = cvpartition(size(Y,1),'HoldOut',0.4);
    
    idxTrain = training(cvp); % Extract training set indices

    %difference here!!!!
    % ----------------------------------------------------
    % TreeBagger(n, X, Y)
    % **** train ensemble model | random forest
    % -> n: number of tree in the ensemble
    % -> X: Training Set (2d) 
    % -> Y: Label (1d) 
    % 
    % 
    % 
    % 
    % 'OOBPrediction','On' 
    % -> enables the calculation of out-of-bag (OOB) predictions
    % -> OOB predictions: estimates of the model's performance on unseen data, using only the samples that were not included in the bootstrap sample for each tree.
    % 
    % 'Method','classification' 
    % -> specifies that the ensemble model is being trained for classification
    % -> response variable Y contains discrete class labels.
    %
    % 'OOBPredictorImportance','on' 
    % -> calculates the importance of predictors based on their ability to improve the accuracy of the model's OOB predictions
    % -> The importance values indicate the relative contribution of each predictor variable in making accurate predictions.
    %
    % 'MaxNumSplits',60 
    % -> Maximum number of splits allowed in each decision tree | controls the depth or complexity of the trees in the ensemble.
    %
    % 'NumPredictorsToSample',50 
    % -> Number of predictor variables to consider at each split point | controls the randomness in feature selection during tree construction.
    % 
    % 
    % 
    % 
    % Overall, 
    % the code trains a random forest ensemble model with 500 decision trees using the specified training data and response variable. 
    % The model provide: 
    % 1. OOB predictions
    % 2. predictor importance,
    % 3. a maximum tree depth of 60 with 50 predictors considered at each split point
    % 
    % ----------------------------------------------------


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
    importance(idx) = Mdl.OOBPermutedPredictorDeltaError; %difference here!!!!
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

%% Draw figures from loaded data

%figure('Position', [500 500 800 300]); hold on; box off;

%plot(35:329,ipt(:,1:295),'LineWidth',1.5);
%set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
%xlim([35 329]); ylim([-0.1 1.1]);
%hold off;

%figure('Position', [500 500 800 300]); hold on; box off;

%plot(35:329,ipt(:,296:590),'LineWidth',1.5);
%set(gca,'linewidth',2,'FontSize',18,'FontWeight','normal');
%xlim([35 329]); ylim([-0.1 1.1]);
%hold off;

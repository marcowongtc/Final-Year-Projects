data = rand(3,4,5);
%k = 3;

%slice = data(:,:,k)

%disp(slice)
%disp(data)

%indices = find(data < 0.5)
%disp(sum(data<0.5,[1,3]))
%disp(data <0.5)
%disp(indices)

%disp(sum(ones(4,2,3), [1,3]))


%data = [1 4 2; 2 5 3; 3 8 4]
%disp(data)
%disp(corrcoef(data))

%A = [1,2,3]
%B= [5, A]

A = [1,2,3]
%B = zeros(5,2)

%L = logspace(-6, -5, 20)

%Y = [0,1,2,3,4,5,6,7,8,9]
%ExtractedY = Y([1,4,6,7])

data = [1 4 2; 2 5 3; 3 8 4]
S = sum(data)
M = mean(data)
R = reshape(data, [9 1])
Ra = randsample(R, 5)
T = data(:,2)

Y = [0,1,2,3,4,5,6,7,8,9]
Y([1,4,6,7]) = [10 10 10 10]



%importance(idx) = abs(Mdl.Beta(:,1));
%importance = normalize(reshape(importance,[590 int64(size(data,2)/590)]))';

I = zeros(1,20)
iix = [1 5 7 9]
B = [1 2 3 4; 1 2 3 4; 1 2 3 4; 1 2 3 4]

I(iix) = abs(B(:,1))
I = reshape(I, [4 5])
I = normalize(I)


shape = size(A)

array = 35:329;
size(array, 2)

ID_list = 35:329;
ID_list = reshape(ID_list, [size(ID_list,2), 1]);
disp(ID_list)

A = [1 2; 3 4]
B = [4 5 6; 7 8 9]
D = [A,B]


A = [1,2,3,4]
B = A(1:2)

C = A > 2
D = find(C)

E = setdiff(A,B)
F = union ([],B)
function J = computeCostMulti(X, y, theta)
%COMPUTECOSTMULTI Compute cost for linear regression with multiple variables
%   J = COMPUTECOSTMULTI(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta
%               You should set J to the cost.

% Vectorization figured out for computeCost.m
% X (47,3)
% y (47,1)
% theta (3, 1)
% h(x) = θ'x for each x
% H = X * theta;                         % (47,1)
% Diff = H - y;                          % (47,1)
% SquareDiff = Diff .^ 2;                % (47,1)
% J = sum(SquareDiff) / (2 * rows(X))    % 1
% J = sum((X*theta - y).^2) / (2 * rows(X)) % The above in one line.

% Vectorization suggested by the assignment. Mine doesn't compute X * theta - y
% twice, but this one does look nicer.
J = (X * theta - y)' * (X * theta - y) / (2 * rows(X));

% =========================================================================

end

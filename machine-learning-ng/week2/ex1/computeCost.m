function J = computeCost(X, y, theta)
%COMPUTECOST Compute cost for linear regression
%   J = COMPUTECOST(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta
%               You should set J to the cost.

% X (97,2)
% y (97, 1)
% theta (2, 1)
% h(x) = θ'x for each x
H = X * theta;                         % (97,1)
Diff = H - y;                          % (97,1)
SquareDiff = Diff .^ 2;                % (97,1)
J = sum(SquareDiff) / (2 * rows(X));   % 1

% =========================================================================

end

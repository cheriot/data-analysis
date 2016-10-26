function [theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters)
%GRADIENTDESCENTMULTI Performs gradient descent to learn theta
%   theta = GRADIENTDESCENTMULTI(x, y, theta, alpha, num_iters) updates theta by
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

for iter = 1:num_iters

    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter vector
    %               theta. 
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCostMulti) and gradient here.
    %

    % X          (47,3)
    % y          (47,1)
    % theta       (3,1)
    % alpha         .01
    % num_inters    400

    % Method 1 works, but ain't pretty.
    % h(x) = θ'x for each x
    % theta(j) = theta(j) - (alpha/rows(X)) * sum((h(x) - y) * xj for m xj's)
    % H = X * theta;       % (47,1)
    % Diff = H - y;        % (47,1)
    % Portion = Diff .* X; % (47,3)
    % Delta = (alpha/rows(X)) * sum(Portion)'; % (3,1)
    % theta = theta - Delta
    theta = theta - (X' * (X * theta - y)) * (alpha/rows(X));

    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCostMulti(X, y, theta);

end

end

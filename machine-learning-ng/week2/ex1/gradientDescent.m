function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
%GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESENT(X, y, theta, alpha, num_iters) updates theta by 
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
    %       of the cost function (computeCost) and gradient here.
    %

    % X          (97,2)
    % y          (97,1)
    % theta       (2,1)
    % alpha         .01
    % num_inters   1500

    % h(x) = θ'x for each x
    % theta(j) = theta(j) - (alpha/rows(X)) * sum((h(x) - y) * xj for m xj's)
    H = X * theta;       % (97,1)
    Diff = H - y;        % (97,1)
    Portion = Diff .* X; % (97,2)
    Delta = (alpha/rows(X)) * sum(Portion)';
    theta = theta - Delta;

    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCost(X, y, theta);

end

end

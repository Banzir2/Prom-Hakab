close all;

balloons = [[642106.7687921221, 3498466.1847251933];
     [671012.5189409455, 3570217.4580244776];
     %[678575.14592777, 3445230.86053654];
     %[692696.6167061602, 3645350.4665942537];
     %[748868.3735791973, 3688186.9144293247];
     [740496.8721962199, 3609535.74057031];
     [737615.7261567067, 3530423.099617622];
     [734605.1525099277, 3450825.1000316045];
     [717312.4251174777, 3373837.197992947];
     [698466.3620219924, 3297285.0489743496];
     [652742.5273499738, 3356990.6751238727];
     [627754.7425738295, 3430796.169016114]];

fun = @(x) score_config(reshape(x * 1e6, size(balloons)), points);
options = optimoptions('fmincon', 'DiffMinChange', 500 / 1e6);
problem.options = options;
problem.solver = 'fmincon';
problem.objective = fun;
problem.x0 = balloons(:) / 1e6;
out = fmincon(problem);
figure; axis equal; hold on;
scatter(points(:,1), points(:,2));

out = reshape(out, size(balloons)) * 1e6;

theta = linspace(0, 2*pi, 100);  % Circle resolution

% Plot each point and its surrounding circle
for i = 1:size(out, 1)
    x = out(i, 1);
    y = out(i, 2);
    
    % Circle coordinates
    xc = radius * cos(theta) + x;
    yc = radius * sin(theta) + y;
    
    % Plot the point and the circle
    plot(x, y, 'k.', 'MarkerSize', 10);     % Plot point
    plot(xc, yc, 'r-');                     % Plot circle
end
scatter(out(:, 1), out(:, 2));
scatter(borders(:, 1), borders(:, 2));
score_config(out, points)

out = utm2ll(out(:,1), out(:,2), 36, 'wgs84');
T = array2table(out);
T.Properties.VariableNames(1:2) = {'lat', 'lon'};
writetable(T, "configurations/balloons" + size(out, 1) + ".csv");
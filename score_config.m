function [out] = score_config(balloons, points)
    rc = size(balloons);
    rc2 = size(points);
    total = zeros(rc2(1), 1);
    for i = 1:rc(1)
        diffx = points(:, 1) - balloons(i, 1);
        diffy = points(:, 2) - balloons(i, 2);
        dist = sqrt(diffx.^2 + diffy.^2);
        binary_dists = zeros(rc2(1), 1);
        binary_dists(dist < 56500) = 1;
        total = total + binary_dists;
    end
    scatter(balloons(:,1), balloons(:,2));
    out = -sum(sum(sqrt(sqrt(total))));
end


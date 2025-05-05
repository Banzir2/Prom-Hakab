close all; clear;

radius = 56500;
borders = readmatrix('borders.csv');

maxX = 823181.7714890691;
maxY = 3901511.0344994236;
minX = 565998.3597003543;
minY = 3064491.748778477;

X = linspace(minX, maxX, (maxX - minX) / 500).';
Y = linspace(minY, maxY, (maxY - minY) / 500).';
[X, Y] = meshgrid(X, Y);
thicc_border = zeros(size(X));

inpolygonmatrix = inpolygon(X, Y, borders(:,1), borders(:,2));
for b=borders.'
    R = sqrt((X - b(1)).^2 + (Y - b(2)).^2);
    thicc_border(R < 40000 & (inpolygonmatrix == 1)) = 1;
    thicc_border(R < 40000 & (~(inpolygonmatrix == 1))) = 1;
end

sizes = size(thicc_border);

idx = find(thicc_border==1);
points(:,1) = X(idx);
points(:,2) = Y(idx);
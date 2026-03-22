%{
@Author: Bhupesh BISHNOI, Florian BUGARIN, Corinne LORENZO
@Project: CNRS MesEnView Computational Imaging Pipeline
@Laboratory: Institute for Research in Geroscience and Rejuvenation (RESTORE) | CNRS UMR5070 | INSERM UMR1301 |
@Laboratory: Clément Ader Institute | Federal University Toulouse Midi-Pyrénées | UMR CNRS 5312 |
@Year: 2024-2025
@License: GNU Lesser General Public License v3.0 (LGPL-3.0)
%}

function output = average_shrink(input, shrink_size)
[rows,cols] = size(input);
if mod(rows,shrink_size) || mod(cols,shrink_size)
    input = padarray(input,...
        [shrink_size-mod(rows,shrink_size),...
        shrink_size-mod(cols,shrink_size)],'post');
end
[rows,cols] = size(input);
kernel = ones(shrink_size);
kernel = kernel./sum(kernel(:));
output = conv2(input,kernel);
output = output(shrink_size:shrink_size:rows,shrink_size:shrink_size:cols);
end


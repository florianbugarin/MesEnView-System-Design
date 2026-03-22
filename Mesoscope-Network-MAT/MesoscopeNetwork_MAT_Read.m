%{
@Author: Bhupesh BISHNOI, Florian BUGARIN, Corinne LORENZO
@Project: CNRS MesEnView Computational Imaging Pipeline
@Laboratory: Institute for Research in Geroscience and Rejuvenation (RESTORE) | CNRS UMR5070 | INSERM UMR1301 |
@Laboratory: Clément Ader Institute | Federal University Toulouse Midi-Pyrénées | UMR CNRS 5312 |
@Year: 2024-2025
@License: GNU Lesser General Public License v3.0 (LGPL-3.0)
%}

function y = read_tif_to_mat(filename, verbose)
nz = size(imfinfo(filename),1);
for i = 1:nz
   y(:,:,i) = imread(filename,i); 
   if verbose
       disp([num2str(i),'/',num2str(nz)]);
   end
end
end

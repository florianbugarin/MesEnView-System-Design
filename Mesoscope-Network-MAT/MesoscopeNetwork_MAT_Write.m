%{
@Author: Bhupesh BISHNOI, Florian BUGARIN, Corinne LORENZO
@Project: CNRS MesEnView Computational Imaging Pipeline
@Laboratory: Institute for Research in Geroscience and Rejuvenation (RESTORE) | CNRS UMR5070 | INSERM UMR1301 |
@Laboratory: Clément Ader Institute | Federal University Toulouse Midi-Pyrénées | UMR CNRS 5312 |
@Year: 2024-2025
@License: GNU Lesser General Public License v3.0 (LGPL-3.0)
%}

function write_mat_to_tif(mat,filename)
imwrite(mat(:,:,1),filename,'compression','none');
[~,~,nz] = size(mat);
for i = 2:nz
   imwrite(mat(:,:,i),filename,'compression','none','writemode','append'); 
end

end
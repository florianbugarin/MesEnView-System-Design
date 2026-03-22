%{
@Author: Bhupesh BISHNOI, Florian BUGARIN, Corinne LORENZO
@Project: CNRS MesEnView Computational Imaging Pipeline
@Laboratory: Institute for Research in Geroscience and Rejuvenation (RESTORE) | CNRS UMR5070 | INSERM UMR1301 |
@Laboratory: Clément Ader Institute | Federal University Toulouse Midi-Pyrénées | UMR CNRS 5312 |
@Year: 2024-2025
@License: GNU Lesser General Public License v3.0 (LGPL-3.0)
%}

VEC = @(x) x(:);
clip = @(x, vmin, vmax) max(min(x, vmax), vmin);
F2D = @(x) fftshift(fft2(ifftshift(x)));
Ft2D = @(x) fftshift(ifft2(ifftshift(x)));
pad2d = @(x) padarray(x,0.5*size(x));
crop2d = @(x) x(1+size(x,1)/4:size(x,1)/4*3,1+size(x,2)/4:size(x,2)/4*3);
conv2d = @(obj,psf) crop2d(real(Ft2D(F2D(pad2d(obj)).*F2D(pad2d(psf)))));
unit_norm = @(x) x./norm(x(:));
auto_corr = @(x) crop2d(Ft2D(F2D(pad2d(unit_norm(x))).*conj(F2D(pad2d(unit_norm(x))))));
x_corr = @(x,y) crop2d(Ft2D(F2D(pad2d(unit_norm(x))).*conj(F2D(pad2d(unit_norm(y))))));
linear_normalize = @(x) (x - min(x(:)))./(max(x(:))-min(x(:)));
load('downsampled_3d_psfs.mat');
psfs = psfs_ds(:,:,81:320); 
clear psfs_ds
psfs_tmp = zeros(324,432,16);
for i = 0:15
    tmp = psfs(:,:,i*15+1:i*15+15);
    tmp = sum(tmp,3);
    tmp = average_shrink(tmp,3);
    psfs_tmp(:,:,i+1) = tmp;
end
psfs = psfs_tmp;
clear psfs_tmp
[rows,cols,depth] = size(psfs);
psfs_recon = psfs;
psfs_recon(psfs_recon<=1.5e-4) = 0;
for i = 1:depth
    tmp = psfs(:,:,i);
    tmp = tmp ./ sum(tmp(:));
    psfs(:,:,i) = tmp;
    tmp = psfs_recon(:,:,i);
    tmp = tmp ./ sum(tmp(:));
    psfs_recon(:,:,i) = tmp;
end
num_particles = 200; 
sphere(sqrt(sx.^2+sy.^2+sz.^2)<=current_radius) = 1;
sphere2 = zeros(7,7,3);
for i = 1:3
    sphere2(:,:,i) = average_shrink(sphere(:,:,i),5);
end
sphere = sphere2;
sphere = sum(sphere,3);
clear sphere2
gt_volume = zeros(rows,cols,depth);
gt_locations = zeros(num_particles,4);
std_lum = 0.3;
for i = 1:num_particles
    rr = randi([7,rows-7]);
    cc = randi([7,cols-7]);
    while true 
        rr = randi([7,rows-7]);
        cc = randi([7,cols-7]);
        if sqrt(xx(rr,cc).^2 + yy(rr,cc).^2) <= 100
            break
        end
    end
    zz = randi([2, depth-2]);
    gt_locations(i,1) = rr;
    gt_locations(i,2) = cc;
    gt_locations(i,3) = zz;
    tmp_lum = 1 + std_lum*randn(1);
    tmp_lum = clip(tmp_lum, 0,1.5);
    gt_locations(i,4) = tmp_lum;
    gt_volume(rr-3:rr+3,cc-3:cc+3,zz)=gt_volume(rr-3:rr+3,cc-3:cc+3,zz)+tmp_lum.*sphere;
end
y = y_part1;
y = y./max(y(:));
y = poissrnd(y.*1000)/1000;
noise_std = 0.02;
y = y + noise_std*randn(size(y));
y = clip(y,0,1);
psfs_recon = single(psfs_recon);
y = single(y);
y_bgsub = single(bg_removal(y,4));
para = [];
para.mu1 = 1;
para.mu2 = 1;
para.mu3 = 1;
para.mu4 = 1;
para.clip_min = 0;
para.clip_max = 100;
para.color = jet(256);
para.tau_l1 = 0.03;
para.tau_tv = 0.01;
para.rtol = 1.5;
para.mu_ratio = 1.1;
para.display_flag = 1;
para.termination_ratio = 0.01;
para.plateau_tolerence = 4;
para.maxiter = 128;
para.img_save_period = 80;
para.img_save_path = '';
xhat(xhat<=0)=0;
xhat = uint8(255*linear_normalize(xhat));
write_mat_to_tif(xhat, 'xhat_cropped.tif');
write_mat_to_tif(uint8(255*linear_normalize(gt_volume)), 'gt_vol.tif');
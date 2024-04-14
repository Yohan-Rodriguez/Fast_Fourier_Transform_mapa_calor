% Cargar la imagen del mapa de calor del partido de fútbol
imagen = imread('descarga (3).png');

% Convertir a escala de grises si es necesario
imagen_gris = rgb2gray(imagen);


% -------------------------------------------------------------------------
% FFT 

% Aplicar la Transformada Rápida de Fourier (FFT)
fft_imagen = fft2(imagen_gris);

% Definir el tamaño de la imagen y las coordenadas del centro
[filas, columnas] = size(imagen_gris);
centro_filas = ceil(filas / 2);
centro_columnas = ceil(columnas / 2);


% -------------------------------------------------------------------------
% FILTRO

% Crear un filtro gaussiano en el dominio de la frecuencia
[X, Y] = meshgrid(1:columnas, 1:filas);

sigma = 60 ; % Ajusta según sea necesario
filtro_gaussiano = exp(-((X - centro_columnas).^2 + (Y - centro_filas).^2) / (2*sigma^2));

% Normalizar el filtro gaussiano
filtro_gaussiano = filtro_gaussiano / sum(filtro_gaussiano(:));

% Aplicar el filtro gaussiano a la FFT de la imagen
fft_filtrada = fft_imagen .* filtro_gaussiano;


% -------------------------------------------------------------------------
% IFFT

% Transformada inversa de Fourier (IFT) para obtener la imagen filtrada
imagen_filtrada = ifft2(fft_filtrada);

% Normalizar los valores de la imagen al rango [0, 1]
imagen_normalizada = mat2gray(abs(imagen_filtrada));

% -------------------------------------------------------------------------
% GRAPHS

% Visualizar los resultados
figure;

% Agregar título a la figura general    
sgtitle(['Sigma: ', num2str(sigma)]);

% Imagen original en escala de grises
subplot(2, 2, 1);
imshow(imagen);
% imshow(imagen_gris);
title('Imagen original (B/W)');

% FFT de la imagen original
subplot(2, 2, 2);
imshow(log(abs(fftshift(fft_imagen))), []);
title('FFT de la imagen');

% Filtro gaussiano en el dominio de la frecuencia
subplot(2, 2, 3);
imshow(filtro_gaussiano, []);
title('Filtro gaussiano');

% Imagen resultante después de aplicar la IFT
subplot(2, 2, 4);
imshow(imagen_normalizada);
title('Transformada Inversa');



% Umbral para distinguir blanco y negro
umbral = 0.5;

% Convertir los valores de la imagen filtrada a blanco o negro según el umbral
imagen_binaria = imagen_normalizada > umbral;

% Mostrar los valores binarios resultantes
% disp('Píxeles blancos (1) y negros (0):');
% disp(imagen_binaria);


% Guardar la matriz en un archivo CSV
csvwrite('imagen_binaria (3).csv', imagen_binaria);

% Obtener la ruta del directorio actual
directorio_actual = pwd;

% Directorio donde se encuentran las imágenes
directorio_imagenes = fullfile(directorio_actual);

% Patrón de nombres de archivo
patron = 'jornada_\d+_.*_.*_[AH].png';

% Obtener lista de nombres de archivo
archivos = dir(fullfile(directorio_imagenes, '*.png'));

for i_foto=1:1
    name_img = archivos(i_foto).name;

    % Cargar la imagen del mapa de calor del partido de fútbol
    imagen = imread(name_img);
    
    % Convertir a escala de grises
    imagen_gris = rgb2gray(imagen);
    
    
    % ---------------------------------------------------------------------
    % FFT 
    
    % Aplicar la FFT
    fft_imagen = fft2(imagen_gris);
    
    % Obtener el tamaño de la imagen y las coordenadas del centro
    [filas, columnas] = size(imagen_gris);
    centro_filas = ceil(filas / 2);
    centro_columnas = ceil(columnas / 2);
    
    
    % ---------------------------------------------------------------------
    % FILTRO
    
    % Filtro gaussiano en el dominio de la frecuencia
    % Matriz
    [X, Y] = meshgrid(1:columnas, 1:filas);
    
    % Ancho de la campana
    sigma = 60; 

    filtro_gaussiano = exp(-((X - centro_columnas).^2 + (Y - centro_filas).^2) / (2*sigma^2));
    
    % Normalizar el filtro gaussiano
    filtro_gaussiano_norm = filtro_gaussiano / sum(filtro_gaussiano(:));
    
    % Aplicar el filtro gaussiano a la FFT == Convolución
    fft_filtrada = fft_imagen .* filtro_gaussiano_norm;
    
    
    % -------------------------------------------------------------------------
    % IFFT
    
    % Transformada inversa de Fourier para obtener la imagen filtrada
    imagen_filtrada = ifft2(fft_filtrada);
    
    % Normalizar los valores de la imagen al rango [0, 1]
    imagen_normalizada = mat2gray(abs(imagen_filtrada));
    
    % % -------------------------------------------------------------------------
    % % GRÁFICAS
    % 
    % figure;
    % 
    % % Título del canvas
    % sgtitle(name_img_parcial)
    % % sgtitle(['Sigma: ', num2str(sigma)]);
    % 
    % % Imagen original
    % subplot(2, 2, 1);
    % imshow(imagen_gris);
    % % imshow(imagen_gris);
    % title('Imagen original (B/W)');
    % 
    % % FFT de la imagen original
    % subplot(2, 2, 2);
    % imshow(log(abs(fftshift(fft_imagen))), []);
    % title('FFT de la imagen');
    % 
    % % Filtro gaussiano en el dominio de la frecuencia
    % subplot(2, 2, 3);    
    % % imshow(filtro_gaussiano, []);
    % imshow(filtro_gaussiano);
    % title('Filtro Gaussiano');
    % 
    % % Imagen resultante después de aplicar la IFT
    % subplot(2, 2, 4);
    % imshow(imagen_normalizada);
    % title('Transformada Inversa');    
    
    
    % -------------------------------------------------------------------------
    % ARCHIVOS BINARIOS DEArchivo Binario de la transformada inversa de Fourier

    % Umbral para distinguir blanco y negro
    umbral = 0.5;
    
    % Convertir los valores de la imagen filtrada a blanco o negro según el umbral
    imagen_binaria = imagen_normalizada > umbral;
    
    % Guardar la matriz en un archivo CSV
    img_bin_csv = sprintf('bin_%s.csv', name_img[:-3]);
    csvwrite(img_bin_csv , imagen_binaria);

end
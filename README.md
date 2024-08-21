# Proyecto de Descarga y Conversión de Videos de YouTube

Este proyecto permite buscar videos en YouTube utilizando palabras clave, descargar los videos encontrados y convertirlos a formato MP3.

## Requisitos

- Python 3.12
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [pydub](https://github.com/jiaaro/pydub)
- [ffmpeg](https://ffmpeg.org/)

## Instalación

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea un entorno virtual:
    ```sh
    python3 -m venv venv
    ```

3. Activa el entorno virtual:
    - En Linux/MacOS:
        ```sh
        source venv/bin/activate
        ```
    - En Windows:
        ```sh
        .\venv\Scripts\activate
        ```

4. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

5. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
    ```env
    API_KEY=<TU_API_KEY_DE_YOUTUBE>
    ```

## Uso

Ejecuta el script principal:
```sh
python main.py
```


## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

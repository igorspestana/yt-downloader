import yt_dlp
import os

def download_specific_video():
    """Download do vídeo específico mencionado pelo usuário"""
    url = "https://www.youtube.com/watch?v=6E5jpNC1iR0"
    
    # Configurar diretório de destino
    download_dir = os.path.expanduser("~/Downloads")
    if not os.path.exists(download_dir):
        download_dir = os.getcwd()
    
    print(f"Baixando vídeo: {url}")
    print(f"Diretório de destino: {download_dir}")
    
    # Configurações do yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]',  # Melhor qualidade em MP4
        'noplaylist': True,
        'ignoreerrors': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Obter informações do vídeo
            print("Obtendo informações do vídeo...")
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Vídeo')
            duration = info.get('duration', 0)
            
            print(f"Título: {title}")
            print(f"Duração: {duration} segundos")
            print("Iniciando download...")
            
            # Baixar o vídeo
            ydl.download([url])
            
            print("Download concluído com sucesso!")
            print(f"Arquivo salvo em: {download_dir}")
            
    except Exception as e:
        print(f"Erro durante o download: {str(e)}")

if __name__ == "__main__":
    download_specific_video() 
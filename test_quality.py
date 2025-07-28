import yt_dlp
import os

def test_video_qualities():
    """Testa e mostra as qualidades disponíveis do vídeo"""
    url = "https://www.youtube.com/watch?v=6E5jpNC1iR0"
    
    print(f"Analisando vídeo: {url}")
    print("=" * 50)
    
    # Configurações básicas
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Obter informações do vídeo
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Vídeo')
            duration = info.get('duration', 0)
            
            print(f"Título: {title}")
            print(f"Duração: {duration} segundos ({duration//60}min {duration%60}s)")
            print()
            
            # Mostrar todos os formatos disponíveis
            formats = info.get('formats', [])
            if formats:
                print("Formatos disponíveis:")
                print("-" * 50)
                
                # Filtrar formatos com vídeo
                video_formats = []
                for fmt in formats:
                    if fmt.get('height') and fmt.get('ext'):
                        video_formats.append(fmt)
                
                # Ordenar por altura (qualidade)
                video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
                
                for i, fmt in enumerate(video_formats[:10]):  # Mostrar os 10 melhores
                    height = fmt.get('height', 'N/A')
                    ext = fmt.get('ext', 'N/A')
                    filesize = fmt.get('filesize', 'N/A')
                    format_id = fmt.get('format_id', 'N/A')
                    
                    if filesize != 'N/A':
                        filesize_mb = filesize / 1024 / 1024
                        filesize_str = f"{filesize_mb:.1f} MB"
                    else:
                        filesize_str = "N/A"
                    
                    print(f"{i+1:2d}. {height:4d}p | {ext:4s} | {filesize_str:8s} | ID: {format_id}")
                
                print()
                
                # Testar download com diferentes qualidades
                test_qualities = ["720p", "480p", "360p"]
                
                for quality in test_qualities:
                    print(f"Testando formato para {quality}:")
                    
                    if quality == "720p":
                        format_spec = "best[height<=720][ext=mp4]"
                    elif quality == "480p":
                        format_spec = "best[height<=480][ext=mp4]"
                    elif quality == "360p":
                        format_spec = "best[height<=360][ext=mp4]"
                    
                    print(f"  Formato: {format_spec}")
                    
                    # Simular seleção de formato
                    test_opts = ydl_opts.copy()
                    test_opts['format'] = format_spec
                    
                    try:
                        with yt_dlp.YoutubeDL(test_opts) as test_ydl:
                            test_info = test_ydl.extract_info(url, download=False)
                            selected_format = test_info.get('format_id', 'N/A')
                            selected_height = test_info.get('height', 'N/A')
                            selected_ext = test_info.get('ext', 'N/A')
                            
                            print(f"  Selecionado: {selected_height}p ({selected_ext}) - ID: {selected_format}")
                    except Exception as e:
                        print(f"  Erro: {str(e)}")
                    
                    print()
                
    except Exception as e:
        print(f"Erro ao analisar vídeo: {str(e)}")

if __name__ == "__main__":
    test_video_qualities() 
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import threading
from urllib.parse import urlparse
import customtkinter as ctk

class YouTubeDownloader:
    def __init__(self):
        # Configurar tema do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Criar janela principal
        self.root = ctk.CTk()
        self.root.title("YouTube Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variáveis
        self.download_path = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="best")
        self.format_var = tk.StringVar(value="mp4")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto para download")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="YouTube Downloader", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame para URL
        url_frame = ctk.CTkFrame(main_frame)
        url_frame.pack(fill="x", padx=10, pady=10)
        
        url_label = ctk.CTkLabel(url_frame, text="URL do YouTube:")
        url_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        url_entry = ctk.CTkEntry(url_frame, textvariable=self.url_var, 
                                placeholder_text="Cole a URL do vídeo aqui...",
                                height=35)
        url_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Frame para configurações
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", padx=10, pady=10)
        
        # Qualidade
        quality_label = ctk.CTkLabel(config_frame, text="Qualidade:")
        quality_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        quality_combo = ctk.CTkComboBox(config_frame, values=["best", "worst", "720p", "480p", "360p"],
                                       variable=self.quality_var)
        quality_combo.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Formato
        format_label = ctk.CTkLabel(config_frame, text="Formato:")
        format_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        format_combo = ctk.CTkComboBox(config_frame, values=["mp4", "webm", "mkv"],
                                      variable=self.format_var)
        format_combo.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Diretório de destino
        path_frame = ctk.CTkFrame(main_frame)
        path_frame.pack(fill="x", padx=10, pady=10)
        
        path_label = ctk.CTkLabel(path_frame, text="Diretório de destino:")
        path_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        path_entry = ctk.CTkEntry(path_frame, textvariable=self.download_path, height=35)
        path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=(0, 10))
        
        browse_btn = ctk.CTkButton(path_frame, text="Procurar", command=self.browse_directory,
                                  width=80, height=35)
        browse_btn.pack(side="right", padx=(5, 10), pady=(0, 10))
        
        # Barra de progresso
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", padx=10, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=10)
        self.progress_bar.set(0)
        
        # Status
        status_label = ctk.CTkLabel(progress_frame, textvariable=self.status_var)
        status_label.pack(pady=(0, 10))
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.download_btn = ctk.CTkButton(button_frame, text="Baixar Vídeo", 
                                         command=self.start_download,
                                         height=40)
        self.download_btn.pack(side="left", padx=(10, 5), pady=10)
        
        self.cancel_btn = ctk.CTkButton(button_frame, text="Cancelar", 
                                       command=self.cancel_download,
                                       height=40, fg_color="red")
        self.cancel_btn.pack(side="right", padx=(5, 10), pady=10)
        self.cancel_btn.configure(state="disabled")
        
        # Área de log
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        log_label = ctk.CTkLabel(log_frame, text="Log de Download:")
        log_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(log_frame, height=100)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Variáveis de controle
        self.downloading = False
        self.cancel_flag = False
        
    def browse_directory(self):
        """Abre diálogo para selecionar diretório de destino"""
        directory = filedialog.askdirectory(initialdir=self.download_path.get())
        if directory:
            self.download_path.set(directory)
            
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()
        
    def progress_hook(self, d):
        """Hook para atualizar progresso"""
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    progress = downloaded / total
                    self.progress_var.set(progress)
                    self.progress_bar.set(progress)
                    
                    # Calcular velocidade
                    speed = d.get('speed', 0)
                    if speed:
                        speed_mb = speed / 1024 / 1024
                        self.status_var.set(f"Baixando... {speed_mb:.1f} MB/s")
                    else:
                        self.status_var.set("Baixando...")
                        
            except Exception as e:
                pass
                
        elif d['status'] == 'finished':
            self.status_var.set("Download concluído! Processando...")
            
    def start_download(self):
        """Inicia o download em uma thread separada"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL do YouTube")
            return
            
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Erro", "URL inválida do YouTube")
            return
            
        if not os.path.exists(self.download_path.get()):
            messagebox.showerror("Erro", "Diretório de destino não existe")
            return
            
        self.downloading = True
        self.cancel_flag = False
        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.status_var.set("Iniciando download...")
        self.log_text.delete("1.0", "end")
        
        # Iniciar download em thread separada
        download_thread = threading.Thread(target=self.download_video, args=(url,))
        download_thread.daemon = True
        download_thread.start()
        
    def download_video(self, url):
        """Executa o download do vídeo"""
        try:
            # Determinar formato baseado na qualidade selecionada
            quality = self.quality_var.get()
            format_type = self.format_var.get()
            
            # Configurar formato específico para cada qualidade
            if quality == "best":
                format_spec = f'bestvideo+bestaudio/best[ext={format_type}]'
            elif quality == "worst":
                format_spec = f'worst[ext={format_type}]'
            elif quality == "720p":
                format_spec = f'bestvideo[height<=720][ext={format_type}]+bestaudio[ext=m4a]/best[height<=720][ext={format_type}]'
            elif quality == "480p":
                format_spec = f'bestvideo[height<=480][ext={format_type}]+bestaudio[ext=m4a]/best[height<=480][ext={format_type}]'
            elif quality == "360p":
                format_spec = f'bestvideo[height<=360][ext={format_type}]+bestaudio[ext=m4a]/best[height<=360][ext={format_type}]'
            else:
                format_spec = f'best[ext={format_type}]'
            
            # Configurações do yt-dlp
            ydl_opts = {
                'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'format': format_spec,
                'noplaylist': True,
                'ignoreerrors': False,
            }
            
            self.log_message(f"Iniciando download de: {url}")
            self.log_message(f"Qualidade: {self.quality_var.get()}")
            self.log_message(f"Formato: {self.format_var.get()}")
            self.log_message(f"Destino: {self.download_path.get()}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Obter informações do vídeo
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Vídeo')
                duration = info.get('duration', 0)
                
                self.log_message(f"Título: {title}")
                self.log_message(f"Duração: {duration} segundos")
                
                # Mostrar formatos disponíveis
                formats = info.get('formats', [])
                if formats:
                    self.log_message("Formatos disponíveis:")
                    for fmt in formats[:5]:  # Mostrar apenas os primeiros 5 formatos
                        height = fmt.get('height', 'N/A')
                        ext = fmt.get('ext', 'N/A')
                        filesize = fmt.get('filesize', 'N/A')
                        if filesize != 'N/A':
                            filesize_mb = filesize / 1024 / 1024
                            filesize_str = f"{filesize_mb:.1f} MB"
                        else:
                            filesize_str = "N/A"
                        self.log_message(f"  - {height}p ({ext}) - {filesize_str}")
                
                # Verificar se foi cancelado
                if self.cancel_flag:
                    return
                    
                # Iniciar download
                self.log_message(f"Baixando com formato: {format_spec}")
                ydl.download([url])
                
            if not self.cancel_flag:
                self.log_message("Download concluído com sucesso!")
                self.status_var.set("Download concluído!")
                messagebox.showinfo("Sucesso", f"Vídeo baixado com sucesso!\nTítulo: {title}")
                
        except Exception as e:
            error_msg = f"Erro durante o download: {str(e)}"
            self.log_message(error_msg)
            self.status_var.set("Erro no download")
            messagebox.showerror("Erro", error_msg)
            
        finally:
            self.downloading = False
            self.download_btn.configure(state="normal")
            self.cancel_btn.configure(state="disabled")
            self.progress_bar.set(0)
            
    def cancel_download(self):
        """Cancela o download em andamento"""
        if self.downloading:
            self.cancel_flag = True
            self.status_var.set("Cancelando...")
            self.log_message("Download cancelado pelo usuário")
            
    def is_valid_youtube_url(self, url):
        """Verifica se a URL é válida do YouTube"""
        try:
            parsed = urlparse(url)
            return (parsed.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be'] and
                    ('watch?v=' in url or 'youtu.be/' in url))
        except:
            return False
            
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

def main():
    """Função principal"""
    app = YouTubeDownloader()
    app.run()

if __name__ == "__main__":
    main() 
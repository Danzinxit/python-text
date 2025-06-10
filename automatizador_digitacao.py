import pyautogui
import time
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading

class AutomatizadorDigitacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatizador de Digitação")
        self.root.geometry("600x400")
        
        # Variável para controlar a digitação
        self.digitando = False
        
        # Configuração do estilo
        style = ttk.Style()
        style.configure("TButton", padding=5)
        style.configure("TLabel", padding=5)
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Área de texto
        ttk.Label(main_frame, text="Digite ou cole o texto aqui:").grid(row=0, column=0, sticky=tk.W)
        self.texto_area = scrolledtext.ScrolledText(main_frame, width=50, height=10)
        self.texto_area.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Opções de velocidade
        ttk.Label(main_frame, text="Velocidade de digitação:").grid(row=2, column=0, sticky=tk.W)
        self.velocidade = ttk.Combobox(main_frame, values=[
            "Muito Lento (0.5s)",
            "Lento (0.3s)",
            "Normal (0.1s)",
            "Rápido (0.05s)",
            "Muito Rápido (0.02s)"
        ])
        self.velocidade.set("Normal (0.1s)")
        self.velocidade.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Frame para os botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Botão de iniciar
        self.botao_iniciar = ttk.Button(botoes_frame, text="Iniciar Digitação", command=self.iniciar_digitacao)
        self.botao_iniciar.grid(row=0, column=0, padx=5)
        
        # Botão de parar
        self.botao_parar = ttk.Button(botoes_frame, text="Parar Digitação", command=self.parar_digitacao, state='disabled')
        self.botao_parar.grid(row=0, column=1, padx=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=2)
        
    def obter_intervalo(self):
        velocidade = self.velocidade.get()
        if "Muito Lento" in velocidade:
            return 0.5
        elif "Lento" in velocidade:
            return 0.3
        elif "Normal" in velocidade:
            return 0.1
        elif "Rápido" in velocidade:
            return 0.05
        else:
            return 0.02
    
    def parar_digitacao(self):
        self.digitando = False
        self.status_label.config(text="Digitação interrompida!")
        self.botao_iniciar.config(state='normal')
        self.botao_parar.config(state='disabled')
    
    def iniciar_digitacao(self):
        texto = self.texto_area.get("1.0", tk.END).strip()
        if not texto:
            self.status_label.config(text="Por favor, digite algum texto!")
            return
        
        # Inicia a digitação em uma thread separada
        self.digitando = True
        threading.Thread(target=self._processo_digitacao, args=(texto,), daemon=True).start()
    
    def _processo_digitacao(self, texto):
        intervalo = self.obter_intervalo()
        self.botao_iniciar.config(state='disabled')
        self.botao_parar.config(state='normal')
        self.status_label.config(text="Preparando para digitar...")
        self.root.update()
        
        # Contagem regressiva
        for i in range(5, 0, -1):
            if not self.digitando:
                return
            self.status_label.config(text=f"Iniciando em {i} segundos...")
            self.root.update()
            time.sleep(1)
        
        if not self.digitando:
            return
            
        self.status_label.config(text="Digitando...")
        self.root.update()
        
        for caractere in texto:
            if not self.digitando:
                return
            pyautogui.write(caractere)
            time.sleep(intervalo)
        
        if self.digitando:  # Só atualiza se não foi interrompido
            self.status_label.config(text="Digitação concluída!")
            self.botao_iniciar.config(state='normal')
            self.botao_parar.config(state='disabled')
            self.digitando = False

def main():
    root = tk.Tk()
    app = AutomatizadorDigitacao(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
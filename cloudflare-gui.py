#!/usr/bin/env python

import os
import subprocess
from time import sleep
import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from tkinter.font import Font

class StylishCloudflaredTunnelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloudflared Tunnel GUI")
        self.root.resizable(False, False)
        
        self.bg_color = "#2d2d2d"
        self.card_color = "#3d3d3d"
        self.text_color = "#ffffff"
        self.accent_color = "#5e72e4"
        self.success_color = "#2dce89"
        self.danger_color = "#f5365c"
        
        self.root.configure(bg=self.bg_color)
        
        self.title_font = Font(family="Helvetica", size=16, weight="bold")
        self.label_font = Font(family="Helvetica", size=10)
        self.button_font = Font(family="Helvetica", size=10, weight="bold")
        self.url_font = Font(family="Roboto Mono", size=10)
        
        window_width = 550
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.tunnel_url = tk.StringVar(value="No active tunnel")
        self.host = tk.StringVar(value="localhost")
        self.port = tk.StringVar(value="8080")
        self.process = None
        
        self.create_widgets()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        main_container = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        title_frame = tk.Frame(main_container, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, 
                text="CLOUDFLARED TUNNEL", 
                font=self.title_font, 
                bg=self.bg_color, 
                fg=self.text_color).pack(side=tk.LEFT)
        
        settings_card = tk.Frame(main_container, 
                               bg=self.card_color, 
                               padx=20, 
                               pady=20,
                               highlightbackground="#4d4d4d",
                               highlightthickness=1)
        settings_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(settings_card, 
                text="Local Host", 
                font=self.label_font, 
                bg=self.card_color, 
                fg=self.text_color).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        host_entry = ttk.Entry(settings_card, 
                             textvariable=self.host, 
                             font=self.label_font)
        host_entry.grid(row=1, column=0, sticky=tk.EW, pady=(0, 15))
        
        tk.Label(settings_card, 
                text="Port", 
                font=self.label_font, 
                bg=self.card_color, 
                fg=self.text_color).grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        port_entry = ttk.Entry(settings_card, 
                             textvariable=self.port, 
                             font=self.label_font)
        port_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 15))
        
        settings_card.columnconfigure(0, weight=1)
        settings_card.columnconfigure(1, weight=1)
        
        url_card = tk.Frame(main_container, 
                           bg=self.card_color, 
                           padx=15, 
                           pady=15,
                           highlightbackground="#4d4d4d",
                           highlightthickness=1)
        url_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(url_card, 
                text="Tunnel URL", 
                font=self.label_font, 
                bg=self.card_color, 
                fg=self.text_color).pack(anchor=tk.W)
        
        url_display = tk.Frame(url_card, bg="#4d4d4d", bd=0)
        url_display.pack(fill=tk.X, pady=(5, 0))
        
        tk.Label(url_display, 
                textvariable=self.tunnel_url, 
                font=self.url_font, 
                bg="#4d4d4d", 
                fg=self.success_color,
                anchor=tk.W,
                padx=10,
                pady=8).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.copy_btn = tk.Button(url_display,
                                text="📋",
                                command=self.copy_url,
                                bg=self.card_color,
                                fg=self.text_color,
                                activebackground=self.card_color,
                                activeforeground=self.text_color,
                                bd=0,
                                relief=tk.FLAT,
                                font=("Arial", 10),
                                state=tk.DISABLED)
        self.copy_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        btn_frame = tk.Frame(main_container, bg=self.bg_color)
        btn_frame.pack(fill=tk.X)
        
        self.start_btn = tk.Button(btn_frame,
                                 text="START TUNNEL",
                                 command=self.start_tunnel,
                                 bg=self.accent_color,
                                 fg="white",
                                 activebackground=self.accent_color,
                                 activeforeground="white",
                                 bd=0,
                                 relief=tk.FLAT,
                                 font=self.button_font,
                                 padx=20,
                                 pady=8)
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        self.stop_btn = tk.Button(btn_frame,
                                text="STOP TUNNEL",
                                command=self.stop_tunnel,
                                bg=self.danger_color,
                                fg="white",
                                activebackground=self.danger_color,
                                activeforeground="white",
                                bd=0,
                                relief=tk.FLAT,
                                font=self.button_font,
                                padx=20,
                                pady=8)
        self.stop_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(10, 0))

        footer = tk.Label(main_container,
                        text="made with ❤️ by keyaru-code",
                        font=("Helvetica", 8),
                        bg=self.bg_color,
                        fg="#777777")
        footer.pack(side=tk.BOTTOM, pady=(10, 0))

    def start_tunnel(self):
        if self.process and self.process.poll() is None:
            messagebox.showwarning("Warning", "Tunnel is already running")
            return
        
        host = self.host.get()
        port = self.port.get()
        
        if not host or not port:
            messagebox.showerror("Error", "Please enter both host and port")
            return
        
        try:
            cmd = f"cloudflared tunnel --url {host}:{port} --logfile cloudflared-log.txt > /dev/null 2>&1 &"
            self.process = subprocess.Popen(cmd, shell=True)
            
            self.tunnel_url.set("Starting tunnel...")
            self.start_btn.config(state=tk.DISABLED)
            self.copy_btn.config(state=tk.DISABLED)
            self.root.update()
            
            self.root.after(1000, self.check_for_url)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start tunnel: {str(e)}")

    def check_for_url(self):
        try:
            if os.path.exists("cloudflared-log.txt"):
                with open("cloudflared-log.txt", "r") as f:
                    log_content = f.read()
                
                import re
                match = re.search(r'https://[-0-9a-z]*\.trycloudflare\.com', log_content)
                if match:
                    url = match.group(0)
                    self.tunnel_url.set(url)
                    self.copy_btn.config(state=tk.NORMAL)
                    
                    os.remove("cloudflared-log.txt")
                    return
                
            self.root.after(1000, self.check_for_url)
            
        except Exception as e:
            self.tunnel_url.set("Error getting URL")
            messagebox.showerror("Error", f"Failed to get tunnel URL: {str(e)}")

    def stop_tunnel(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if "cloudflared" in proc.info['name']:
                try:
                    proc.kill()
                except:
                    pass
        
        if os.path.exists("cloudflared-log.txt"):
            try:
                os.remove("cloudflared-log.txt")
            except:
                pass
        
        self.tunnel_url.set("No active tunnel")
        self.start_btn.config(state=tk.NORMAL)
        self.copy_btn.config(state=tk.DISABLED)
        
        if self.process:
            self.process.terminate()
            self.process = None

    def copy_url(self):
        url = self.tunnel_url.get()
        if url and url != "No active tunnel" and not url.startswith("Error"):
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            self.copy_btn.config(text="✓")
            self.root.after(2000, lambda: self.copy_btn.config(text="📋"))

    def on_close(self):
        self.stop_tunnel()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StylishCloudflaredTunnelApp(root)
    
    try:
        root.iconbitmap(default='cloudflare.ico')
    except:
        pass
    
    root.mainloop()

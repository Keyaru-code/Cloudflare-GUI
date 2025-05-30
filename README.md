# Cloudflare Tunnel GUI

A stylish graphical interface for creating and managing Cloudflare tunnels using `cloudflared`.

![Screenshot](screenshot.jpg)

## Features

- Simple one-click tunnel creation  
- Clean, modern dark theme interface  
- Copy tunnel URL to clipboard with one click  
- Automatic cleanup of log files  
- Cross-platform support (Windows/Linux/macOS)  

## Requirements

- Python 3.6+
- `cloudflared` installed and in system PATH  

## Installation (GitHub Only)

### Method 1: Install directly from GitHub
```bash
pip install git+https://github.com/Keyaru-code/Cloudflare-GUI.git
```

### Method 2: Manual installation
```bash
git clone https://github.com/Keyaru-code/Cloudflare-GUI.git
cd Cloudflare-GUI
pip install .
```

## Usage

Run the application:  
```bash
cloudflare-gui
```

### How to Use:
1. Enter your local host (default: `localhost`)  
2. Enter port number (default: `8080`)  
3. Click **START TUNNEL**  
4. Wait for the URL to appear  
5. Click the 📋 button to copy the tunnel URL  
6. Click **STOP TUNNEL** when finished  

## Troubleshooting

Common issues:  
🔹 *"Command not found"* → Verify `cloudflared` is in your PATH  
🔹 *Connection errors* → Check if local service is running on specified port  
🔹 *Permission denied* → Try running with `sudo` (Linux/macOS)  

## Development

To run from source:
```bash
git clone https://github.com/Keyaru-code/Cloudflare-GUI.git
cd Cloudflare-GUI
pip install -r requirements.txt
python -m cloudflare_tunnel_gui.app
```

## License

MIT License  

## Credits

Made with ❤️ by:  
- [Keyaru-code](https://github.com/Keyaru-code)  
- [Alienkrishn](https://github.com/Alienkrishn)  

---

💡 *Note: This application automatically cleans up log files when closed.*

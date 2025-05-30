from setuptools import setup, find_packages

setup(
    name="cloudflare-tunnel-gui",
    version="1.0.0",
    author="Keyaru-code",
    author_email="alienkrishn@gmail.com",
    description="GUI for Cloudflare Tunnels",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Keyaru-code/Cloudflare-GUI",
    packages=find_packages(),
    package_data={
        "cloudflare_tunnel_gui": ["assets/*"],
    },
    install_requires=[
        "psutil>=5.8.0",
        "requests>=2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "cloudflare-gui=cloudflare_tunnel_gui.app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

# Install mamba (a faster conda)
curl -fsSL https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C $HOME
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Initialize mamba
micromamba shell init -s bash -p ~/micromamba
source ~/.bashrc

# Verify installation
micromamba --version


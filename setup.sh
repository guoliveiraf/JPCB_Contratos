#!/bin/bash

# Atualiza a lista de pacotes
sudo apt-get update

# Instala os pacotes listados em packages.txt
sudo xargs -a packages.txt apt-get install -y
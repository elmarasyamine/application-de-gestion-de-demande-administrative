#!/bin/bash
# ============================================
# Script de deploiement - Gestion de Demandes
# Serveur: 46.101.215.185
# ============================================

set -e

echo "========================================="
echo "  Deploiement - Gestion de Demandes"
echo "  Serveur: 46.101.215.185 (4GB RAM)"
echo "========================================="

# 0. Ajouter du swap (important pour Rasa + Docker)
echo "[0/7] Configuration du swap..."
if [ ! -f /swapfile ]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "Swap 2GB cree"
else
    echo "Swap deja configure"
fi

# 1. Mise a jour systeme
echo "[1/7] Mise a jour du systeme..."
apt update && apt upgrade -y

# 2. Installer Docker
echo "[2/7] Installation de Docker..."
if ! command -v docker &> /dev/null; then
    apt install -y docker.io docker-compose-v2
    systemctl enable docker --now
    echo "Docker installe avec succes"
else
    echo "Docker deja installe"
fi

# 3. Installer Nginx
echo "[3/7] Installation de Nginx..."
if ! command -v nginx &> /dev/null; then
    apt install -y nginx
    systemctl enable nginx --now
    echo "Nginx installe avec succes"
else
    echo "Nginx deja installe"
fi

# 4. Configurer le firewall
echo "[4/7] Configuration du firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
echo "Firewall configure"

# 5. Configurer Nginx reverse proxy
echo "[5/7] Configuration de Nginx..."
cp nginx-server.conf /etc/nginx/sites-available/gestion-demande
ln -sf /etc/nginx/sites-available/gestion-demande /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
echo "Nginx configure avec succes"

# 6. Construire et lancer les conteneurs Docker
echo "[6/7] Construction et lancement des conteneurs..."
docker compose up --build -d
echo "Conteneurs lances avec succes"

# 7. Verification
echo "[7/7] Verification des services..."
echo "Attente du demarrage complet (60s pour Rasa)..."
sleep 60
echo ""
echo "--- Conteneurs Docker ---"
docker compose ps
echo ""
echo "--- Test API Backend ---"
curl -s http://127.0.0.1:8093/api/ || echo "(Backend en cours de demarrage)"
echo ""
echo "--- Test Frontend ---"
curl -s -o /dev/null -w "Frontend: HTTP %{http_code}" http://127.0.0.1:3000
echo ""

echo ""
echo "========================================="
echo "  Deploiement termine !"
echo "========================================="
echo ""
echo "  Application: http://46.101.215.185"
echo "  API Backend: http://46.101.215.185/api"
echo ""
echo "  Pour voir les logs:"
echo "    docker compose logs -f"
echo ""
echo "  Pour voir les logs Rasa:"
echo "    docker compose logs -f rasa"
echo ""
echo "  Pour arreter:"
echo "    docker compose down"
echo "========================================="

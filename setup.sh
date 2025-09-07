#!/bin/bash

# Quantumia AI Kurulum Scripti
# Bu script gerekli bağımlılıkları kontrol eder ve kurar

echo "🔮 Quantumia AI Kurulum Scripti"
echo "================================"

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Hata mesajı fonksiyonu
error_exit() {
    echo -e "${RED}Hata: $1${NC}" >&2
    exit 1
}

# Başarı mesajı fonksiyonu
success_msg() {
    echo -e "${GREEN}$1${NC}"
}

# Bilgi mesajı fonksiyonu
info_msg() {
    echo -e "${BLUE}$1${NC}"
}

# Uyarı mesajı fonksiyonu
warning_msg() {
    echo -e "${YELLOW}$1${NC}"
}

# Özel mesaj fonksiyonu
special_msg() {
    echo -e "${MAGENTA}$1${NC}"
}

# Detaylı işletim sistemi tespiti
detect_os() {
    info_msg "İşletim sistemi tespit ediliyor..."
    
    # Temel OS türü
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
    elif [[ "$OSTYPE" == "cygwin" ]]; then
        OS="Cygwin"
    elif [[ "$OSTYPE" == "msys" ]]; then
        OS="Windows"
    elif [[ "$OSTYPE" == "win32" ]]; then
        OS="Windows"
    else
        error_exit "Desteklenmeyen işletim sistemi: $OSTYPE"
    fi
    
    # Linux dağıtımı tespiti
    if [ "$OS" = "Linux" ]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO=$ID
            DISTRO_VERSION=$VERSION_ID
        elif [ -f /etc/redhat-release ]; then
            DISTRO="rhel"
        elif [ -f /etc/arch-release ]; then
            DISTRO="arch"
        elif [ -f /etc/debian_version ]; then
            DISTRO="debian"
        else
            DISTRO="unknown"
        fi
    fi
    
    info_msg "İşletim Sistemi: $OS"
    if [ "$OS" = "Linux" ]; then
        info_msg "Dağıtım: $DISTRO"
        info_msg "Versiyon: $DISTRO_VERSION"
    fi
}

# Python kontrolü
check_python() {
    info_msg "Python kontrol ediliyor..."
    if command -v python3 &> /dev/null; then
        PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        success_msg "Python $PYTHON_VER bulundu"
        
        # Python versiyon kontrolü (3.8+)
        PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
        PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
        
        if [ $PYTHON_MAJOR -eq 3 ] && [ $PYTHON_MINOR -ge 8 ]; then
            success_msg "Python versiyonu uygun (3.8+)"
        else
            error_exit "Python 3.8 veya üstü gerekiyor. Mevcut versiyon: $PYTHON_VER"
        fi
    else
        error_exit "Python3 bulunamadı. Lütfen önce Python 3.8 veya üstünü kurun."
    fi
}

# Pip kontrolü
check_pip() {
    info_msg "Pip kontrol ediliyor..."
    if command -v pip3 &> /dev/null; then
        success_msg "Pip3 bulundu"
    else
        warning_msg "Pip3 bulunamadı, kuruluyor..."
        
        if [ "$OS" = "Linux" ]; then
            case $DISTRO in
                "ubuntu"|"debian"|"kali"|"linuxmint")
                    sudo apt update && sudo apt install -y python3-pip
                    ;;
                "fedora")
                    sudo dnf install -y python3-pip
                    ;;
                "centos"|"rhel")
                    sudo yum install -y epel-release
                    sudo yum install -y python3-pip
                    ;;
                "arch"|"manjaro")
                    sudo pacman -Sy --noconfirm python-pip
                    ;;
                "opensuse"|"suse")
                    sudo zypper install -y python3-pip
                    ;;
                *)
                    error_exit "Otomatik pip3 kurulumu bu dağıtımda desteklenmiyor. Lütfen manuel olarak pip3 kurun."
                    ;;
            esac
        elif [ "$OS" = "macOS" ]; then
            # macOS için pip kurulumu
            if command -v brew &> /dev/null; then
                brew install python3
            else
                error_exit "Homebrew bulunamadı. Lütfen pip3'ü manuel olarak kurun."
            fi
        else
            error_exit "Pip3 kurulumu için lütfen manuel olarak pip3 kurun."
        fi
        
        # Pip kurulumunu doğrula
        if command -v pip3 &> /dev/null; then
            success_msg "Pip3 başarıyla kuruldu"
        else
            error_exit "Pip3 kurulumu başarısız oldu"
        fi
    fi
}

# Sanal ortam kontrolü ve kurulumu
setup_venv() {
    info_msg "Sanal ortam kontrol ediliyor..."
    if python3 -c "import venv" &> /dev/null; then
        success_msg "venv modülü mevcut"
    else
        warning_msg "venv modülü bulunamadı, kuruluyor..."
        
        if [ "$OS" = "Linux" ]; then
            case $DISTRO in
                "ubuntu"|"debian"|"kali"|"linuxmint")
                    sudo apt install -y python3-venv
                    ;;
                "fedora")
                    sudo dnf install -y python3-virtualenv
                    ;;
                "centos"|"rhel")
                    sudo yum install -y python3-virtualenv
                    ;;
                "arch"|"manjaro")
                    sudo pacman -Sy --noconfirm python-virtualenv
                    ;;
                "opensuse"|"suse")
                    sudo zypper install -y python3-virtualenv
                    ;;
                *)
                    error_exit "Otomatik venv kurulumu bu dağıtımda desteklenmiyor. Lütfen manuel olarak python3-venv kurun."
                    ;;
            esac
        elif [ "$OS" = "macOS" ]; then
            # macOS için venv kurulumu
            if command -v brew &> /dev/null; then
                brew install python3
            else
                error_exit "Homebrew bulunamadı. Lütfen venv'i manuel olarak kurun."
            fi
        fi
    fi
    
    # Sanal ortam oluştur
    info_msg "Sanal ortam oluşturuluyor..."
    python3 -m venv quantumia-env
    if [ $? -eq 0 ]; then
        success_msg "Sanal ortam başarıyla oluşturuldu: quantumia-env"
    else
        error_exit "Sanal ortam oluşturulamadı"
    fi
}

# Gerekli paketleri kur
install_requirements() {
    info_msg "Gerekli paketler kuruluyor..."
    
    # Sanal ortamı etkinleştir
    source quantumia-env/bin/activate
    
    # requirements.txt kontrol et
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        if [ $? -eq 0 ]; then
            success_msg "Gerekli paketler başarıyla kuruldu"
        else
            error_exit "Paket kurulumu başarısız oldu"
        fi
    else
        warning_msg "requirements.txt bulunamadı, temel paketler kuruluyor..."
        
        # Temel paketleri kur
        pip3 install requests wikipedia psutil pyjokes scikit-learn numpy
        
        # Kurulumu doğrula
        if python3 -c "import requests, wikipedia, psutil, pyjokes, sklearn, numpy" &> /dev/null; then
            success_msg "Temel paketler başarıyla kuruldu"
            
            # requirements.txt oluştur
            pip3 freeze > requirements.txt
            success_msg "requirements.txt oluşturuldu"
        else
            error_exit "Temel paket kurulumu başarısız oldu"
        fi
    fi
}

# Bellek dosyasını oluştur
create_memory_file() {
    info_msg "AI bellek dosyası oluşturuluyor..."
    
    if [ ! -f "ai_memory.json" ]; then
        cat > ai_memory.json << EOF
{
    "conversations": [],
    "preferences": {},
    "user_data": {}
}
EOF
        success_msg "AI bellek dosyası oluşturuldu: ai_memory.json"
    else
        info_msg "AI bellek dosyası zaten mevcut"
    fi
}

# Kurulumu tamamla
complete_setup() {
    echo ""
    special_msg "🎉 Quantumia AI kurulumu tamamlandı!"
    echo ""
    info_msg "Çalıştırmak için:"
    echo -e "${CYAN}  source quantumia-env/bin/activate${NC}"
    echo -e "${CYAN}  python3 quantumia.py${NC}"
    echo ""
    info_msg "Durdurmak için:"
    echo -e "${CYAN}  deactivate${NC}"
    echo ""
}

# Ana kurulum fonksiyonu
main() {
    echo -e "${MAGENTA}"
    echo "   ██████                                     █████                                ███"
    echo "  ███░░░░███                                  ░░███                                ░░░"
    echo " ███    ░░███ █████ ████  ██████   ████████   ███████   █████ ████ █████████████   ████   ██████"
    echo "░███     ░███ ░░███ ░███  ░░░░░███ ░░███░░███ ░░░███░   ░░███ ░███ ░░███░░███░░███ ░░███  ░░░░░███"
    echo "░███   ██░███  ░███ ░███   ███████  ░███ ░███   ░███     ░███ ░███  ░███ ░███ ░███  ░███   ███████"
    echo "░░███ ░░████   ░███ ░███  ███░░███  ░███ ░███   ░███ ███ ░███ ░███  ░███ ░███ ░███  ░███  ███░░███"
    echo " ░░░██████░██  ░░████████░░████████ ████ █████  ░░█████  ░░████████ █████░███ █████ █████░░████████"
    echo "   ░░░░░░ ░░    ░░░░░░░░  ░░░░░░░░ ░░░░ ░░░░░    ░░░░░    ░░░░░░░░ ░░░░░ ░░░ ░░░░░ ░░░░░  ░░░░░░░░"
    echo -e "${NC}"
    
    detect_os
    check_python
    check_pip
    setup_venv
    install_requirements
    create_memory_file
    complete_setup
}

# Scripti çalıştır
main "$@"

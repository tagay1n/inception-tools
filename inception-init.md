# Just a reminder on how to deploy the [INCEpTION](https://inception-project.github.io/) server

1. Run VM
2. Open TCP port 80 for sources 0.0.0.0/0
3. After connection to the machine execute commands
```shell
sudo apt -y update
# install java, git
sudo apt -y install openjdk-17-jdk git
# create workdir
sudo mkdir -p /opt/inception/editors
# write into setting file
sudo bash -c 'cat > /opt/inception/settings.properties <<EOF
remote-api.enabled=true
EOF'

sudo wget -P /opt/inception https://github.com/inception-project/inception/releases/download/inception-38.1/inception-app-webapp-38.1-standalone.jar

# turn on proxying 80 -> 8080
sudo bash -c 'cat > /etc/nftables.conf <<EOF
#!/usr/sbin/nft -f

flush ruleset

table ip nat {
    chain prerouting {
        type nat hook prerouting priority 0;
        tcp dport 80 redirect to 8080
    }
    chain output {
        type nat hook output priority 0;
        tcp dport 80 redirect to 8080
    }
}
EOF'
sudo systemctl enable nftables
sudo systemctl start nftables

# configure daemon to control app lifecycle
sudo bash -c 'cat > /etc/systemd/system/inception.service <<EOF
[Unit]
Description=Inception java app
After=network.target

[Service]
User=inception
WorkingDirectory=/opt/inception
ExecStart=/usr/bin/java -Dinception.home=/opt/inception -XX:MaxRAMPercentage=80.0 -jar inception-app-webapp-38.1-standalone.jar
SuccessExitStatus=143
Restart=always
RestartSec=60
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF'

# Install editors
git clone https://github.com/inception-project/inception-annotatorjs-editor-plugin.git /opt/inception/editors/inception-annotatorjs-editor-plugin
git clone https://github.com/inception-project/inception-recogito-editor-plugin.git /opt/inception/editors/inception-recogito-editor-plugin
git clone https://github.com/inception-project/inception-apache-annotator-editor-plugin.git /opt/inception/editors/inception-apache-annotator-editor-plugin
git clone https://github.com/inception-project/inception-doccano-sequence-editor-plugin.git /opt/inception/editors/inception-doccano-sequence-editor-plugin
git clone https://github.com/inception-project/inception-intertext-editor-plugin.git /opt/inception/editors/inception-intertext-editor-plugin

sudo useradd -r -s /bin/false inception
sudo chown -R inception:inception /opt/inception

sudo systemctl stop inception
sudo systemctl daemon-reload
sudo systemctl start inception
sudo systemctl enable inception
```
4. Login as admin in the INCEpTION web app by public IP on port 80
5. Create new user with roles `ROLE_USER`, `ROLE_REMOTE`, `ROLE_ADMIN` 
6. Done
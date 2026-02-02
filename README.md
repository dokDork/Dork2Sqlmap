# Dork2Sqlmap



[![License](https://img.shields.io/badge/license-MIT-_red.svg)](https://opensource.org/licenses/MIT)  
<img src="https://github.com/dokDork/red-team-penetration-test-script/raw/main/images/siteSniper.png" width="250" height="250">  
  
## Description
**Dork2Sqlmap** is a lightweight tool that lets users select SQL injection–related Google Dorks and automatically generates ready-to-use sqlmap commands for authorized security testing and bug bounty workflows.
The tool proceeds step by step:
- It asks which type of Google Dork for SQL injection you want to use.
- It asks which Google Dork to use.
- It asks for the context argument of the websites on which to activate Google Dorks (e.g., "gods and heroes," food, "online games").
- It opens as many browsers as necessary to activate Google Dork searches.
- Once the website with the relevant Google Dork has been found, the URL must be passed to the tool, which will prepare tmux shells with the sqlmap instruction to test that SQL injection. A gobuster command will also be created in the tmux shell to search the target site for any hidden files.
  
## Example Usage
 ```
python3 dork2sqlmap.py
 ``` 
<img src="https://github.com/dokDork/Dork2sqlmap/raw/main/images/01.png">


Once selected the PHASE, scripts will be generated using tmux as terminal.
At this point you can select a specific SUB-PHASE using tmux commands:  
**(CTRL + b) w**  
<img src="https://github.com/dokDork/red-team-penetration-test-script/raw/main/images/03.png">

once the SUB-PHASE has been selected you will be able to view the commands that have been pre-compiled to analyse the SUB-PHASE. At this point it is possible to selecet and execute a specific command just pressing ENTER:
<img src="https://github.com/dokDork/red-team-penetration-test-script/raw/main/images/04.png">

When you need to change penetration test PHASE and return to main manu, you need to close the tmux session. To implement this action you need to use the tmux shortcut:  
**(CTRL + b) :kill-session**  
or, if you configure tmux as reported in the Installation section, you can use the shortcut:
**(CTRL + b) (CTRL + n)**  

<img src="https://github.com/dokDork/red-team-penetration-test-script/raw/main/images/05.png">

  
## Command-line parameters
```
./siteSniper.sh <interface> <target url>
```

| Parameter | Description                          | Example       |
|-----------|--------------------------------------|---------------|
| `interface`      | network interface through which the target is reached | `eth0`, `wlan0`, `tun0`, ... |
| `target url`      | Target URL you need to test          | `http://www.example.com`          |

  
## How to install it on Kali Linux (or Debian distribution)
It's very simple  
```
cd /opt
sudo git clone https://github.com/dokDork/SiteSniper.git
cd SiteSniper 
chmod 755 siteSniper.sh 
./siteSniper.sh 
```
Optional: You can insert a shortcut to move faster through the tool.
```
echo "bind-key C-n run-shell \"tmux kill-session -t #{session_name}\"" >> ~/.tmux.conf
```


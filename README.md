# Dork2Sqlmap



[![License](https://img.shields.io/badge/license-MIT-_red.svg)](https://opensource.org/licenses/MIT)  
<img src="https://github.com/dokDork/red-team-penetration-test-script/raw/main/images/dork2sqlmap.png" width="250" height="250">  
  
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
<img src="https://github.com/dokDork/Dork2Sqlmap/blob/main/images/01.jpg">

As mentioned, after selecting the URLs of the websites you want to analyze with sqlmap, tmux windows will be created.
- Use 'Ctrl+b' then 'n' to navigate between windows
- Use 'Ctrl+b' then 'd' to detach from session

<img src="https://github.com/dokDork/Dork2Sqlmap/blob/main/images/02.jpg">

 
  
## How to install it on Kali Linux (or Debian distribution)
It's very simple  
```
pip3 install requests beautifulsoup4 --break-system-packages
cd /opt
sudo git clone https://github.com/dokDork/Dork2Sqlmap.git
cd Dork2Sqlmap 
chmod 755 dork2sqlmap.py 
python3 dork2sqlmap.py
```


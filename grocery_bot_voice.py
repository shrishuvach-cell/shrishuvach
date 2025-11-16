import json
import datetime
import speech_recognition as sr
import pyttsx3
from typing import Dict, List, Optional

class GroceryTracker:
    def __init__(self, data_file="groceries.json"):
        self.data_file = data_file
        self.load_data()
    
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.inventory = json.load(f)
        except FileNotFoundError:
            self.inventory = {}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.inventory, f, indent=2)
    
    def add_item(self, item: str, quantity: int, category: str = "uncategorized", 
                 expiry_date: str = None):
        if item.lower() in self.inventory:
            self.inventory[item.lower()]["quantity"] += quantity
        else:
            self.inventory[item.lower()] = {
                "quantity": quantity,
                "category": category.lower(),
                "added_date": datetime.datetime.now().isoformat(),
                "expiry_date": expiry_date
            }
        self.save_data()
        return f"Added {quantity} {item}(s) to your inventory."
    
    def remove_item(self, item: str, quantity: int = None):
        item_key = item.lower()
        if item_key not in self.inventory:
            return f"{item} not found in inventory."
        
        if quantity is None or quantity >= self.inventory[item_key]["quantity"]:
            del self.inventory[item_key]
            message = f"Removed all {item}(s) from inventory."
        else:
            self.inventory[item_key]["quantity"] -= quantity
            message = f"Removed {quantity} {item}(s). {self.inventory[item_key]['quantity']} remaining."
        
        self.save_data()
        return message
    
    def check_inventory(self):
        if not self.inventory:
            return "Your inventory is empty."
        
        categorized = {}
        for item, details in self.inventory.items():
            category = details.get("category", "uncategorized")
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(f"{item} ({details['quantity']})")
        
        result = "Current Inventory:\n"
        for category, items in categorized.items():
            result += f"\n{category.title()}:\n"
            for item in items:
                result += f"  - {item}\n"
        
        return result
    
    def check_expiring_soon(self, days: int = 7):
        expiring = []
        today = datetime.date.today()
        threshold = today + datetime.timedelta(days=days)
        
        for item, details in self.inventory.items():
            if details.get("expiry_date"):
                expiry = datetime.datetime.fromisoformat(details["expiry_date"]).date()
                if today <= expiry <= threshold:
                    expiring.append(f"{item} expires on {expiry.strftime('%Y-%m-%d')}")
        
        if not expiring:
            return f"No items expiring within the next {days} days."
        
        result = f"Items expiring within {days} days:\n"
        for item in expiring:
            result += f"- {item}\n"
        return result

class GroceryChatbot:
    def __init__(self):
        self.tracker = GroceryTracker()
        self.categories = ["produce", "dairy", "meat", "pantry", "frozen", "beverages"]
        self.voice_enabled = False
        
        # Initialize speech recognition and text-to-speech
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume level
            self.setup_microphone()
            self.voice_available = True
        except Exception as e:
            print(f"Voice functionality not available: {e}")
            self.voice_available = False
            self.tts_engine = None
    
    def setup_microphone(self):
        """Adjust for ambient noise"""
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Microphone is ready!")
    
    def speak(self, text: str):
        """Convert text to speech"""
        print(f"Bot: {text}")  # Always print to console
        
        # Only use TTS if voice is enabled and available
	
        if self.voice_enabled and self.voice_available and self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
    
    def listen(self) -> Optional[str]:
        """Listen for voice input"""
        if not (self.voice_enabled and self.voice_available):
            return None
            
        try:
            print("Listening...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"You (voice): {text}")
            return text
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return None
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error in listening: {e}")
            return None
    
    def parse_add_command(self, message: str):
        parts = message.lower().replace("add ", "").split()
        
        quantity = 1
        if parts and parts[0].isdigit():
            quantity = int(parts[0])
            item_parts = parts[1:]
        else:
            item_parts = parts
        
        expiry_date = None
        item_string = " ".join(item_parts)
        if "expires" in item_string:
            item_string, expiry_str = item_string.split("expires")
            try:
                datetime.datetime.strptime(expiry_str.strip(), "%Y-%m-%d")
                expiry_date = expiry_str.strip()
            except ValueError:
                pass
        
        item_name = item_string.strip()
        category = self._guess_category(item_name)
        
        return self.tracker.add_item(item_name, quantity, category, expiry_date)
    
    def parse_remove_command(self, message: str):
        parts = message.lower().replace("remove ", "").split()
        
        quantity = None
        if parts and parts[0].isdigit():
            quantity = int(parts[0])
            item_name = " ".join(parts[1:])
        else:
            item_name = " ".join(parts)
        
        return self.tracker.remove_item(item_name, quantity)
    
    def _guess_category(self, item: str):
        item_lower = item.lower()
        if any(word in item_lower for word in ["apple", "banana", "orange", "lettuce", "tomato", "broccoli", "carrot", "spinach"]):
            return "produce"
        elif any(word in item_lower for word in ["milk", "cheese", "yogurt", "butter", "cream"]):
            return "dairy"
        elif any(word in item_lower for word in ["chicken", "fish",  "egg"]):
            return "meat"
        elif any(word in item_lower for word in ["bread", "rice", "pasta", "cereal", "flour", "sugar"]):
            return "pantry"
        elif any(word in item_lower for word in ["ice cream", "frozen", "peas"]):
            return "frozen"
        elif any(word in item_lower for word in ["water", "juice", "soda", "coffee", "tea", "beer", "wine"]):
            return "beverages"
        else:
            return "uncategorized"
    
    def process_message(self, message: str):
        message_lower = message.lower()
        
        if "add" in message_lower:
            return self.parse_add_command(message)
        elif "remove" in message_lower or "delete" in message_lower:
            return self.parse_remove_command(message)
        elif "inventory" in message_lower or "list" in message_lower:
            return self.tracker.check_inventory()
        elif "expir" in message_lower:
            return self.tracker.check_expiring_soon()
        elif "help" in message_lower:
            return self.get_help()
        elif "voice on" in message_lower:
            if self.voice_available:
                self.voice_enabled = True
                return "Voice commands enabled."
            else:
                return "Voice functionality is not available on this system."
        elif "voice off" in message_lower:
            self.voice_enabled = False
            return "Voice commands disabled."
        else:
            return "I didn't understand that command. Type 'help' for assistance."

    def get_help(self):
        return """
Available commands:
- Add [quantity] [item] [expires YYYY-MM-DD] - Add items to inventory
- Remove [quantity] [item] - Remove items from inventory
- List inventory - Show all items
- Check expiring - Show items expiring soon
- Voice on/off - Enable/disable voice commands
- Help - Show this help message
- Quit/Exit - Exit the program

Examples:
- Add 3 apples
- Add 1 milk expires 2025-12-25
- Remove 2 apples
- List inventory
- Voice on
"""

def main():

    engine = pyttsx3.init()
    engine.say("Hello, Welcome to the Grocery Tracking Bot.")


    bot = GroceryChatbot()


    bot.voice_enabled = True  # Enable voice manually
    
    print("Grocery Tracking Chatbot")
    print("Type 'help' for commands or 'quit' to exit")
    if bot.voice_available:
        print("Type 'voice on' to enable voice commands")
    else:
        print("Voice functionality is not available on this system")
    print()
    
    while True:
        # Check if voice is enabled and available
        if bot.voice_enabled and bot.voice_available:
            # Listen for voice command
            user_input = bot.listen()
            if user_input is None:
                continue
        else:
            # Text input
            try:
                user_input = input("You: ")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit']:
            bot.speak("Goodbye!")
            break
        
        # Process the message
        response = bot.process_message(user_input)
        bot.speak(response)
        engine.say(response)

if __name__ == "__main__":
    main()

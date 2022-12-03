from src import Client
from rich import console

import os
import discord
import importlib

class Main:
    def __init__(self, intents: discord.Intents):
        self.console = console.Console()
        self.load_events()
        self.client = Client(intents=intents)

    def load_events(self):
        events = []

        # Using os, walk the events directory
        for root, dirs, files in os.walk("events"):
            # Loop through files
            for file in files:
                # If the file is a python file
                if file.endswith(".py"):
                    # Remove the .py from the file name
                    name = file[:-3]

                    # Get the module path
                    path = f"events.{name}"

                    # Add the module path to the events list
                    events.append({"name": name, "path": path})

        if len(events) == 0:
            print("No events found.")
            return

        for event in events:
            module = importlib.import_module(event["path"])
            module = importlib.reload(module)

            # Get the runner from the module
            runner = getattr(module, f'on_{event["name"]}')

            # Add the runner to the client
            setattr(Client, f'on_{event["name"]}', runner)

            # Print it was bound
            self.console.log(f"Event: [bold yellow]{event['name']}[/bold yellow] was successfully bound.")


    def run(self):
        # Get token from ENV
        token = os.getenv("DISCORD_TOKEN")

        # Run the bot
        self.client.run(token)


if __name__ == "__main__":
    main = Main(
        intents = discord.Intents.all()
    )
    main.run()
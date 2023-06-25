from src.bots.linkedin_bots import LinkedinScrapperBot

if __name__ == "__main__":
    bot = LinkedinScrapperBot("data science", "US", wait_time=3)
    bot.start()
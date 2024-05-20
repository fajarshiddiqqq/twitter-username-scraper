import subprocess
import os
import json


class TwitterScraper:
    def __init__(self, tweet_id=None):
        os.makedirs("credentials", exist_ok=True)
        os.makedirs("results", exist_ok=True)
        self.tweet_id = tweet_id

    def scrape_tweet(self):
        if not self.check_accounts():
            print("\033[93m" + "Please configure your Twitter account:" + "\033[0m")
            twitter_username = input(
                "\033[96m" + "Enter your Twitter username: " + "\033[0m"
            )
            twitter_password = input(
                "\033[96m" + "Enter your Twitter password: " + "\033[0m"
            )
            gmail = input("\033[96m" + "Enter your Gmail address: " + "\033[0m")
            gmail_password = input(
                "\033[96m" + "Enter your Gmail password: " + "\033[0m"
            )

            if os.path.exists("credentials/accounts.txt"):
                os.remove("credentials/accounts.txt")

            with open("credentials/accounts.txt", "a") as f:
                f.write(
                    f"{twitter_username}:{twitter_password}:{gmail}:{gmail_password}\n"
                )

            accounts = subprocess.run(
                ["twscrape", "--db", "credentials/accounts.db", "accounts"],
                capture_output=True,
            )
            output = accounts.stdout.decode("utf-8").strip().split("\n")

            if len(output) == 1:
                add_account_subpricess = subprocess.run(
                    [
                        "twscrape",
                        "--db",
                        "credentials/accounts.db",
                        "add_accounts",
                        "credentials/accounts.txt",
                        "username:password:email:email_password",
                    ]
                )
                accounts = subprocess.run(
                    ["twscrape", "--db", "credentials/accounts.db", "accounts"],
                    capture_output=True,
                )
                output = accounts.stdout.decode("utf-8").strip().split("\n")
                if len(output) == 1:
                    print("\033[91m" + "Failed to add accounts" + "\033[0m")
                    return

            header = output[0].split()
            data_rows = [line.split() for line in output[1:]]

            for row in data_rows:
                if row[header.index("username")] == twitter_username:
                    if row[header.index("logged_in")] == "0":
                        login_subprocess = subprocess.run(
                            [
                                "twscrape",
                                "--db",
                                "credentials/accounts.db",
                                "login_accounts",
                            ]
                        )
                        break
                    else:
                        break

        if self.tweet_id is None:
            tweet_url = input("\033[96m" + "Enter the tweet URL: " + "\033[0m")
            if self.check_url(tweet_url) == False:
                return

        print("\033[92m" + "Scraping data..." + "\033[0m")
        self.collect_likes()
        self.collect_retweets()
        self.collect_replies()
        print("\033[92m" + "Scraping completed successfully!" + "\033[0m")

    def check_accounts(self):
        if not os.path.exists("credentials/accounts.txt") or not os.path.exists(
            "credentials/accounts.db"
        ):
            return False

        with open("credentials/accounts.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if len(line.split(":")) != 4:
                    return False

        return True

    def check_url(self, tweet_url):
        if tweet_url.split(".com/")[0].split("//")[1] not in ["twitter", "x"]:
            print("\033[91m" + "Not a Twitter URL" + "\033[0m")
            return False

        tweet_url = tweet_url.split(".com/")[1].split("/")
        if len(tweet_url) != 3 or tweet_url[1] != "status":
            print("\033[91m" + "Invalid tweet URL" + "\033[0m")
            return False

        self.tweet_id = tweet_url[2]

        return True

    def collect_likes(self):
        favoriters = subprocess.run(
            [
                "twscrape",
                "--db",
                "credentials/accounts.db",
                "favoriters",
                self.tweet_id,
            ],
            capture_output=True,
            text=True,
        )
        if favoriters.stdout is not None:
            favoriters_list = favoriters.stdout.split("\n")
            favoriters_list = favoriters_list[:-1]
            parsed_favoriters = [json.loads(entry) for entry in favoriters_list]
        else:
            print("No output captured from the subprocess.")

        with open(f"results/{self.tweet_id} - Likes.txt", "w") as f:
            for favoriter in parsed_favoriters:
                f.write(favoriter["username"] + "\n")

    def collect_retweets(self):
        retweeters = subprocess.run(
            [
                "twscrape",
                "--db",
                "credentials/accounts.db",
                "retweeters",
                self.tweet_id,
            ],
            capture_output=True,
            text=True,
        )
        if retweeters.stdout is not None:
            retweeters_list = retweeters.stdout.split("\n")
            retweeters_list = retweeters_list[:-1]
            parsed_retweeters = [json.loads(entry) for entry in retweeters_list]
        else:
            print("No output captured from the subprocess.")

        with open(f"results/{self.tweet_id} - Retweets.txt", "w") as f:
            for retweeter in parsed_retweeters:
                f.write(retweeter["username"] + "\n")

    def collect_replies(self):
        replies = subprocess.run(
            [
                "twscrape",
                "--db",
                "credentials/accounts.db",
                "tweet_replies",
                self.tweet_id,
            ],
            capture_output=True,
            text=True,
        )
        if replies.stdout is not None:
            replies_list = replies.stdout.split("\n")
            replies_list = replies_list[:-1]
            parsed_replies = [json.loads(entry) for entry in replies_list]
        else:
            print("No output captured from the subprocess.")
        with open(f"results/{self.tweet_id} - Comments.txt", "w") as f:
            for reply in parsed_replies:
                f.write(reply["user"]["username"] + "\n")


if __name__ == "__main__":
    tw = TwitterScraper()
    tw.scrape_tweet()

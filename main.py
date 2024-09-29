import cmd
import os
import shlex
import http.client
import json


class GitHubUserTracker(cmd.Cmd):
    # Settings the command prompt and intro message for the user
    prompt = "GHUserTracker> "
    intro = "Welcome to GitHub User Tracker! Type help to list commands."

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()

    def do_github_activity(self, username):

        if len(shlex.split(username)) != 1:  # Checks if only a single name is being dropped, and
            print("Please enter a valid GitHub username.")
            return
        username = shlex.split(username)[0]
        print(username)

        url = f"https://api.github.com/users/{username}/events"

        conn = http.client.HTTPSConnection("api.github.com")

        headers = {
            "User-Agent": "GitHub User Tracker" # Needed so GitHub let us in
        }

        conn.request("GET", url, headers=headers)

        response = conn.getresponse()
        if response.status == 200:  # if it is successful
            data = json.loads(response.read())
            print("Output:")
            for event in data[:5]:
                self.eventHandler(event)
        else:
            print(f"Error - response code: {response.status}")

    def eventHandler(self, event):
        match event["type"]:
            case "PushEvent":
                print(f"Pushed {event['payload']['size']} commit(s) to {event['repo']['name']}")
            case "CreateEvent":
                print(f"Created {event['payload']['ref_type']} {event['payload']['ref']}")
            case "IssuesEvent":
                print(f"Created issue {event['payload']['issue']['number']}")
            case "PullRequestEvent":
                print(f"Created pull request {event['payload']['pull_request']['number']} for repo {event['repo']['name']}")
            case "WatchEvent":
                print(f"Starred {event['repo']['name']}")
            case _:
                print("Currently not implemented event type")


if __name__ == '__main__':
    GitHubUserTracker().cmdloop()

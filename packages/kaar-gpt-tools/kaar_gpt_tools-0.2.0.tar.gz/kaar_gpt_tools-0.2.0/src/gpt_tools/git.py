import argparse
import logging
import os
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass

from gpt.openai import AssistantMessage, ChatCompletion, ChatCompletionRequest, ChatMessage, SystemMessage, UserMessage

LOGGER = logging.getLogger(__name__)
XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
DEFAULT_CHAT_MODEL = "gpt-3.5-turbo"
SAMPLE_PATH = pathlib.Path(f"{XDG_DATA_HOME}/git-gpt/samples")
SAMPLE_PATH.mkdir(parents=True, exist_ok=True)


def load_samples(file_pattern: str) -> list[str]:
    files = sorted(SAMPLE_PATH.glob(file_pattern))
    LOGGER.debug("Loading samples from %s", files)
    return [file.read_text() for file in files]


def load_commit_samples() -> list[ChatMessage]:
    user_messages = [UserMessage(text) for text in load_samples("*.diff")]
    LOGGER.debug("Loaded %d user messages", len(user_messages))
    assistant_messages = [AssistantMessage(text) for text in load_samples("*.commit")]
    LOGGER.debug("Loaded %d assistant messages", len(assistant_messages))
    return [message for pair in zip(user_messages, assistant_messages) for message in pair]


@dataclass
class Commit:
    commit_hash: str
    author: str
    date: str
    message: str
    diff: str


def parse_commit(commit_text: str) -> Commit:
    commit_and_diff = re.split("\n(?=diff --git)", commit_text)
    commit_text = commit_and_diff[0]
    lines = commit_text.strip().split("\n")
    # Merge commits dont have a diff
    diff = commit_and_diff[1] if len(commit_and_diff) > 1 else ""
    return Commit(
        commit_hash=lines[0].split(" ")[1],
        author=lines[1].replace("Author: ", ""),
        date=lines[2].replace("Date:   ", ""),
        message="\n".join([line.strip() for line in lines[4:]]),
        diff=diff,
    )


def parse_git_log(log_data) -> list[Commit]:
    commits = re.split("\n(?=commit)", log_data)
    return [parse_commit(commit_text=commit) for commit in commits]


def latest_commits(n: int) -> list[Commit]:
    """
    Returns the latest n commits as a list of Commit objects.
    Args:
        n: The number of commits to return.
    Returns:
        A list of Commit objects.
    """
    log_data = subprocess.check_output(["git", "log", "-p", "-{}".format(n)]).decode("utf-8").strip()
    commits = re.split("\n(?=commit)", log_data)
    return [parse_commit(commit_text=commit) for commit in commits]


def load_git_commit_samples() -> list[ChatMessage]:
    # TODO: The sixe of the diff and the message should be limited and configurable.
    # For example if we add the option --short
    # It should only contain examples with oneline messages
    #
    # If option --long/--detailed is added it should only contain
    # examples with multiline messages
    messages = []
    for commit in latest_commits(5):
        messages.append(UserMessage(commit.diff))
        messages.append(AssistantMessage(commit.message))

    return messages


def request_commit_message(input_diff) -> str:
    COMMIT_INSTRUCTION = """
You are going to receive a git diff and you are going to provide a git commit with the format: {Subject}\n\n{Message}.
Subject is a short description of the change.
For subject use imperative mood.
Subject line is not allowed to be longer than 50 characters.
Message is a more detailed description of the code change.
Message is not needed for trivial changes.
Be direct, try to eliminate filler words and phrases in these sentences.
Shorter is always better.
"""
    instruction = SystemMessage(COMMIT_INSTRUCTION)
    samples = load_git_commit_samples()
    LOGGER.debug("Loaded %d samples", len(samples))
    if len(samples) == 0:
        LOGGER.error("No samples found")
        sys.exit(1)

    input_message = UserMessage(input_diff.read())

    chat_completion = ChatCompletion.create(
        ChatCompletionRequest(
            model=DEFAULT_CHAT_MODEL,
            messages=[instruction, *samples, input_message],
            temperature=0.1,
        )
    )
    return chat_completion.message.content


def request_review(input_diff) -> str:
    instructions = SystemMessage(
        "You are going to receive a git diff and you are going to provide a review of the changes. Write only the review and nothing else."
    )
    input_message = UserMessage(input_diff.read())
    chat_completion = ChatCompletion.create(
        ChatCompletionRequest(model=DEFAULT_CHAT_MODEL, messages=[instructions, input_message])
    )
    return chat_completion.message.content


def main():
    parser = argparse.ArgumentParser(description="GitGPT - GPT powered git assistant")
    parser.add_argument(
        "command",
        type=str,
        choices=["commit", "review"],
        help="Command to run",
    )
    parser.add_argument(
        "input",
        type=argparse.FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="Input file, defaults to stdin",
    )
    args = parser.parse_args()

    if args.command == "commit":
        print(request_commit_message(args.input))

    if args.command == "review":
        print(request_review(args.input))


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN, format="%(asctime)s %(levelname)s %(message)s")
    main()

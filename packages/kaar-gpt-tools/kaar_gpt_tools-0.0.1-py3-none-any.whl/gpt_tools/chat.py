#!/usr/bin/env python3

import argparse
import logging
import os
import sys

from llm_base.openai import ChatCompletion, ChatCompletionRequest, ChatMessage

LOG = logging.getLogger(__name__)
DEFAULT_LOG_LEVEL = logging.INFO

DEFAULT_USER = "gpt-cli"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODELS = ["gpt-3.5-turbo", "gpt-4"]
DEFAULT_MODEL = "gpt-3.5-turbo"

XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))


class ChatClient:
    def __init__(
        self,
        model: str,
        history: list[ChatMessage] = [],
    ):
        self.model = model
        self.messages = history
        self.template_text = None

    def add_prompt_template(self, template_text: str):
        """Adds template text to be added to each message sent"""
        self.template_text = template_text

    def add_system_prompt(self, prompt: str):
        self.messages.append(ChatMessage(role="system", content=prompt))

    def send(self, input_text: str, echo: bool = False):
        """
        Send a message to the chatbot and return the response.
        If a template text is added its added to the message

        :param input_text: The message to send to the chatbot.
        :param echo: Whether to echo the input text to the console.
        """

        if self.template_text:
            # Use the template for the input test
            input_text = self.template_text.replace("<QUESTION>", input_text)

        if echo:
            print(input_text, end="")

        chat_message = ChatMessage(role="user", content=input_text)
        LOG.debug("Sending message: %s", chat_message)
        self.messages.append(chat_message)
        chat_completion = ChatCompletion.create(
            ChatCompletionRequest(
                model=self.model,
                messages=self.messages,
            )
        )
        LOG.debug("Received message: %s", chat_completion)
        self.messages.append(chat_completion.message)
        return self.messages[-1].content


def main():
    logging.basicConfig(
        stream=sys.stdout,
        level=DEFAULT_LOG_LEVEL,
        format="%(message)s",
    )
    logging.getLogger("gpt.completion").setLevel(DEFAULT_LOG_LEVEL)

    parser = argparse.ArgumentParser(description="OpenAI GPT-3 text completion")
    parser.add_argument(
        "file",
        type=argparse.FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="File to read text from",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=MODELS,
        help="Model to use",
        default=DEFAULT_MODEL,
    )
    parser.add_argument(
        "--instructions",
        "-i",
        type=str,
        help="GPT system instruction",
    )
    parser.add_argument("--message", "-m", type=str, help="Send message")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="enable debug output",
    )
    args = parser.parse_args()

    messages = []

    if args.debug:
        LOG.setLevel(logging.DEBUG)
        logging.getLogger("gpt.completion").setLevel(logging.DEBUG)
        LOG.debug("Verbose output enabled")
        LOG.debug("argv: %s", sys.argv)

    chat = ChatClient(model=args.model, history=messages)
    if args.instructions:
        LOG.debug("Adding instructions: %s", args.instructions)
        chat.add_system_prompt(args.instructions)

    if args.message:
        LOG.debug("Sending message: %s", args.message)
        print(chat.send(args.message))

    if not args.file.isatty():
        LOG.debug("Reading from: %s", args.file.name)
        with args.file as f:
            print(chat.send(f.read(), echo=True))
            return

    LOG.debug("Starting interactive mode")
    try:
        while True:
            print(chat.send(input(">>> ")))

    except EOFError:
        LOG.debug("EOF")
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        LOG.debug("KeyboardInterrupt")
        sys.exit(1)

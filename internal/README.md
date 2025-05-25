# internal

## config

This folder contains the configuration files for the bot.

`get_path(name_in_config: str)` - Returns the path to the configuration file.

`openai` - An instance of the OpenAI API client.

`client` - An instance of the Pyrogram client.

`settings` - An instance of the Settings class.

`tools` - A list of tools for the bot, that are used for boss.

`system_prompt` - The system prompt for the bot.

`other_tools` - A list of tools for the bot, that are used for non-boss.

### ai\_tools.py
`async write_memory(memory, date)` - Writes a memory to the database.

`async read_memory(date = None)` - Reads a memory from the database.

`async send_message(username, message = None)` - Sends a message to the user(to your boss if username is not specified).

`async send_message_boss(message)` - Sends a message to your boss.

`async get_date(format)` - Get current date.

`async get_weather(latitude, longitude)` - Get current temperature for provided coordinates in celsius.

`async block_user(username)` - Block user in telegram.

`functions: dict[str, async function]` - A list of functions that can be used by the bot.

### settings.py
`Settings` - A class that represents the settings for the bot.

## handlers

This folder contains the handlers for the bot.

### telegram.py
`async process_completion(completion: Response, messages, message, client, tools)` - Processes the completion of the ai.

`async handle_me(client: Client, message: Message)` - Handles the message from boss.

`async handle_other(client: Client, message: Message)` - Handles the message from non-boss.

`async channels(client: Client, message: Message)` - Handles the message from channel.

## services

This folder contains the services for the bot.

### ai.py
`async process_history(client: Client, messages: list[Message])` - Processes the history of the conversation.

`async make_completion(client, tools: list, system_prompt: str, history: list[Message], call_id: str = None, output: str = None, lastoutput = None)` - Makes a completion.

### calendar.py
`async delete_event(event_id: str)` - Deletes an event from the calendar.

`async add_event(**kwargs)` - Adds an event to the calendar.

`async get_events(max_results: int = 1)` - Gets events from the calendar.

### email.py
This module isn't ready fully yet

`async send_email(to, subject, text)` - Sends an email to the user.

## main.py
`async main()` - The main function of the bot.
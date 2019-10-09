# Wegbot

Yet another Wegbot rewrite. This time in Python, because the [discord.py](https://github.com/Rapptz/discord.py) rewrite 
fits our use case _so much_ better than [discord.js](https://discord.js.org). This is not a joke.

<br />

### Table of Contents

- [Commands](#commands)
    - [Public commands](#public-commands)
    - [Restricted commands](#restricted-commands)
    - [Owner-only commands](#owner-only-commands)
- [Extensions](#extensions)

<br />

## Commands

Commands are specifically-formatted messages that interact with the bot in different ways. You want the bot 
to do something for you? You put a command in the chat. Note that all commands _depend_ on having been used 
in a public channel, so unless otherwise specified, you cannot DM commands to the bot.

Note that only verified users can use commands.

#### Public commands

These commands are open to public use by all verified Discord members.

- `?roles` - List eligible roles.
    - Notes:
        - The only public version of this command is the parameter-less `?roles`, exactly as written.
        - This command is functionally equivalent to `?roles list`, which is detailed below with [restricted commands](#restricted-commands).

- `?addrole <role_name>` - Request a role.
    - Parameters:
        - `role_name` - The name of the role you want to request, or **all** to request all eligible roles.
    - Notes:
        - Only eligible roles can be requested. Use `?roles` for a list of eligible roles.
        - Multiple roles can be requested by providing a comma-separated list of role names.
        - All eligible roles can be requested at once by using `?addrole all`.

- `?removerole <role_name>` - Relinquish a role.
    - Parameters:
        - `role_name` - The name of the role you want to relinquish.
    - Notes:
        - Roles can be relinquished in the same way that they are requested, so the same notes for `?addrole` apply here.

#### Restricted Commands

These commands are only available to elevated users, known to common folk as "moderators" or "mods". 👀

- `?roles add <role_name>` - Declare a role eligible to be requested. 
    - Parameters:
        - `role_name` - The name of the role to be declared eligible.
    - Notes:
        - Mod roles cannot be declared eligible to be requested, for obvious reasons.

- `?roles remove <role_name>` - Declare a role **no longer** eligible to be requested.
    - Parameters:
        - `role_name` - The name of the eligible role to be declared ineligible.

#### Owner-only Commands

These commands are only available to me (`weg`) as the owner of the bot.

Currently no owner-only commands have been implemented.


## Extensions

Extensions are actions that the bot takes on its own. Extensions may be triggered by user input, or by some events 
firing behind the scenes.

Currently no extensions have been implemented.

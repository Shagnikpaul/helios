<h1 align="center">🤨 <code>API_KEY</code> handling by the bot.</h1>
<br>

## `Question:` How does the bot store the `API_KEY` given by the user?
### `Answer` : It creates a new folder locally in the server where it is hosted where a `.json` file is created whose name is same as that of server's `discord ID`. It is in that file the `API_KEY` is stored.

<br>

## `Question:` Who can use the `API_KEY` for using the  `/weather` command?
### `Answer` : Only those who are in that particular server. 

<br>

## `Question:` What if someone steals the `API_KEY` while I was running the `/server-setup` command?
### `Answer` : In order to prevent that the command is set to be `ephemeral` meaning the command-reply will only be visible to the user running the command.

<br>

## `Question:` What happens to the `API_KEY` when the bot leaves the server?
### `Answer` : Bot will delete that particular server's `.json` file before leaving the server. Alternatively you can also run `/delete-server-data` command to delete your `API_KEY` from the server.

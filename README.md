# WatchBot
Simple Discord bot to monitor a website's uptime and latency. *Used for monitoring [hatch.lol](https://github.com/hatchdotlol)'s API.  
## Setup
1. Install Python if you don't already have it - [download](https://python.org)
2. Install dependencies with `pip install discord.py requests`
3. Configure your bot. Open `config.json` and edit the URL you want to monitor, the wait time (15 seconds by default), the command prefix (if desired), your bot's token (see **Creating Your Bot**), and the role ID of the role you want to be able to run the commands. *I recommend keeping setting it to your administrator or owner role so users don't disable the monitoring.*
4. Run `bot.py`: use `py bot.py` in your terminal on Windows or `python3 bot.py` on Linux.
5. Begin monitoring: type `!begin` in the channel you'd like the bot to send updates to. *If you changed the prefix in the configuration file, use that instead of !*
6. To stop monitoring for any reason, you can use `!stop`.
## Creating Your Bot
If you don't have a Discord bot application set up, this section helps you do it.
1. Log in to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click the button in the top right that says New Application
3. Name the bot and agree to the terms. Then click create.
4. Click on the **Bot** tab on the left, scroll down to **Token** and then click **Reset Token**.
5. Copy the token and store it somewhere safe *and private*.
6. Scroll down to **Privileged Gateway Intents** and enable **Server Members Intent** and **Message Content Intent**.
7. On the left sidebar, click on the **OAuth2** tab, scroll down to **OAuth2 URL Generator** and choose **Bot**, then in the new menu that appears below choose **Administrator** (you may want to select individual permissions instead).
> [!CAUTION]
> Enabling the Administrator permission gives your bot access to everything in whichever server you add it to, which will be destructive if you do not store your token securely. (KEEP YOUR TOKEN PRIVATE!) Also, if you do not own the server you are adding the bot to, you may need to select individual permissions instead, such as *Send Messages*, *Manage Messages*, *Embed Links*, *Attach Files*, *Add Reactions*, *View Channels*, and *Manage Server* if you want it to be able to work in private channels.
8. Select Guild Install from the dropdown after you've selected the bot permissions, and copy the generated URL. Then paste it into a new tab and add the bot to your server.
9. Select the **Installation** tab on the left side and uncheck the **User Install** box. Then, use the dropdown below to set **Install Link** to **None**
10. Select the **Bot** tab again, and toggle **Public Bot** off.
Your bot then should be ready to go! Steps 9 and 10 go through setting your bot as private so people can't add it to their own server. You can now start the bot setup detailed above.

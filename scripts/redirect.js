/*
    NKA (Formerly PyBotDevs) 2022. For enquiries contact PyBotDevs <pybotdevs@outlook.com>
*/

/**
 * @name github
 * @description Redirects to the bot's Github repository page. 
 */
function github()
{
    git_author = "PyBotDevs";
    git_repo = "isobot-lazer";
    window.location = "https://github.com/" + git_author + "/" + git_repo;
}

client_id = "953278050135588905";
/**
 * @name invite
 * @description Redirects to the bot's Discord OAuth2 link.
 * @param {string} client_id
 * @param {string} permissions
 * 
 */
function invite(client_id, permissions)
{
    permission_int = null;
    if (permissions == "all")
    {
        // Default permissions configuration. Includes all bot functionality.
        permission_int = 8;
    }
    else if (permissions == "no_moderation")
    {
        // Invites the bot without any moderation permissions. Useful if inviter does not have admin permissions or the bot is not going to be used for moderation.
        permissions_int = 412387495233;
    }
    else
    {
        return console.warn("Argument \"permissions\" can only be \"all\" or \"no_moderation\".");
    }
    window.location = "https://discord.com/api/oauth2/authorize?client_id=" + client_id + "&permissions=" + permissions_int + "&scope=bot%20applications.commands";
}

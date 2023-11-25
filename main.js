function rd(target) {
    // Redirects the user to a subpage, or another page.
    if (target == "invite") {window.location = "https://discord.com/api/oauth2/authorize?client_id=896437848176230411&permissions=8&scope=bot%20applications.commands";}
    else if (target == "git") {window.location = "https://github.com/pybotdevs/isobot";}
    else if (target == "commands") {window.location = "";}
    else if (target == "changelog") {window.location = "https://github.com/pybotdevs/isobot/releases/latest";}
    else if (target == "server") {window.location = "https://discord.gg/b5pz8T6Yjr";}
	else if (target == "uptime") {window.location = "https://stats.uptimerobot.com/PlKOmI0Aw8";}
    else {console.error("Page target does not exist.");}
}

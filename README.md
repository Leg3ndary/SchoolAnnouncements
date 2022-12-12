# SchoolAnnouncements

My entry for the SCH Hackathon.

Will add more as I go.

## Day 1 - December 3rd 2022

Starting the project, I will be aiming to project announcements from our schools google doc to discord.

```md
1. Finished client, can now save data to a json doc, and return all of it's data
```

## Day 2 - December 4th 2022

```md
1. Worked on parsing data, it's a pain, no commits for today :(
```

## Day 3 - December 5th, 2022

```md
1. Finished parsing the data, data is now usable to an extent
```

## Day 4 - December 6th, 2022

```md
1. Made a few updates to the client
    - Update an internal cache of all of the announcements
    - get_latest method to get the latest announcement regardless of current date.
2. Made the bot
    - Few bugs I have to clear out, will look into tomorrow
    - Made a command to index/search announcements using discord's nice slash command autocompletes
    - Made a task to automatically update and send a webhook some data to send the updates, hope it works tomorrow!
```

## Day 5-7 - December 7th, 2022

I spent these days polishing up my written and recorded submission, the bot is basically done, and will be pushed to prod.

This project uses discord.py v2.1.0, the google docs api, and a few other libraries here and there, these are listed in `requirements.txt`. I used python version 3.9.10 to run this bot.
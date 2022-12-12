# School Announcements

A project by Leg3ndary AKA Ben

All of these topics are addressed in my video! I would recommend [watching](https://youtu.be/aXBSoJvAkOc) it for the most info about my project!

## Section 1 - What???

Everyone who's gone to school knows every morning, you'll have some sort of announcements. "Chess club is on Thursday at 2pm in room 201, join us for some fun! If you would like to join the football team, come to room 123 for so and so important meeting." However, I always somehow seem to miss it, whether this be because I'm too engrossed in my studies (totally), or because my class is just too loud, this is something you probably don't want to miss. Of course, most schools might have this on some bulletin board, or on some website, but who wants to take the time to go read that? In the end, announcements are really just a way to communicate news or information to a wide variety of students, however, I believe the way that it's currently done is outdated, and quite frankly useless. This pushed me to create and propose this new idea, that doesn't disrupt the old way of using the PA system, and just pushes that information quickly and easily to students. Effectively making communication between the school and students, much, much better.

## Section - 2 Communication

This being my first hackathon, I had a multitude of ideas, none of which I'll name for now, but when I saw the prompt, I must say, I was a little discouraged. Sure, communication covers a wide variety of topics, but what could I make that was not only creative, but also interesting and fun to create. I spent a good few hours before the start of the hackathon thinking and thinking. At first I thought of making some sort of letter writter/assistant, it would use machine learning and promote communication between you and someone else. I scratched that on the basis that it would be too complicated and in my opinion not creative enough. I then thought about making some news recommendation app, that would actively send you current news and recommend things based on what you did. This idea was fine except for the fact I also thought it wasn't creative enough, and already implemented in the world. 

Then I heard my schools announcements in class, well, sort of, it was too hard to hear over our class's usual talking, and that's when I thought, why not make some sort of app to forward or make it easier to find announcements? This topic effectively encapsulated the theme communication by strengthening it, and addressed it a creative, meaningful way. I then thought about it for the rest of the day and came up with a basic blueprint, I would take the announcements, save them somehow, and then forward them to my phone, all without having to lift a finger.

## Section 3 - Further information: Usefulness

Interestingly enough, our school has a discord server dedicated for anything school related, it's student run, and only for 2024 graduates, but it has over 200 users/students. As one of the co-creators/admins I decided that this was a great place to try this out. Over 200 students could login to discord every morning, to chat with other students, and "bing" a notification could pop up on their phone, open or closed, by discord giving them the announcements. In fact I will be rolling this out to the server soon after this hackathon!

## Section 4 - Further information: Complexity (only for hackathon participants)

I used many technologies! These included discord.py, google docs api, a bit of regex, along with vscode for my ide. I go much more into detail in my video as there are a few main parts to my presentation!

However, if you still want a short explanation, I used google docs to pull the entire docs elements into json, I then parsed and formatted that into both a markdown file to view the information visually, and json. Through this process I also parsed out club names, announcements, as well as times/dates to add timestamps to each announcements. I then used a popular library known as [discord.py](https://github.com/Rapptz/discord.py) to create a bot and connect to the discord api, along with this I made an automatic "task" that would send the information directly to a webhook. I also made a command that used discord's slash command and autocomplete to make an announcement searching function. My final product was a discord bot that would not only send announcements quickly and easily, it would also let you view past announcements which were also organized.

One thing to note, at around 7:30 in my video, when I was talking about how the announcement date would be formatted differently, I meant sometimes it would be like 7 Dec 2022, instead of 7 December 2022, which was pretty annoying, but it worked out...

## Section 5 - Further information: Presentation (only for hackathon participants)

I don't have any more information I'd like to share about my project other than it was fun to create :).

## Section 6 - Further information: Anything else you want to mention (only for hackathon participants)

This bot is not publicly available, unfortunately I only want it running in 2 servers, my school server and my development server. Sorry!

## Section 7 - Conclusion: Future plans

I will be releasing this project later today! Future plans may include things like school related links, or just to fix that one command T-T. Good luck all other hackathon participants!

I think this project is a perfect submission for this hackathon because not only does it address it's theme well, it shows how your project can be used in real life, and help out real people.

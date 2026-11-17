# Duolingo's character-led app screens

## What it is

Duolingo is a language-learning app. Its own design team makes it. The screens are led by characters: Duo the green owl, and a cast of ten people and animals the company calls its "world characters". They talk, react and cheer inside the lessons.

On February 4, 2026, Leah Lee and Lokesh Fulfagar of Duolingo wrote up a refresh of the app's main tabs. The new tabs shipped on iPhone first.

See it: https://blog.duolingo.com/core-tabs-redesign/

**Best screen: the first picture in that post.** Six app screens sit side by side: lessons, quests, a leaderboard, a video call with a character, a profile and a friends feed. Look at how the same chunky buttons, round shapes and bright flat colours hold six very different screens together.

## How it turned out

- **Apple Design Award, 2023.** Duolingo won the Delight and Fun category on June 5, 2023. Apple named the characters and the game-like features, such as quests and leaderboards, as reasons.
- **People use it daily, and the number is growing.** In its report for July to September 2026, Duolingo counted 64.9 million daily users, up 29 percent in a year. It had 153.1 million monthly users and 13.1 million paying ones.
- **Ratings.** 4.7 out of 5 from about 5.6 million ratings in the US App Store.
- **The maker tests its design and publishes results.** Around late 2019 the team changed the streak (the count of days in a row you have practised) so one lesson a day keeps it going. In its own test, the share of learners still active on day 14 rose by 3.3 percent. It also found that learners with a seven-day streak were 2.4 times as likely to come back the next day. These are the maker's own figures.
- **The maker kept it.** The 2026 tab refresh tidies the look instead of replacing it. The team reports higher use of the tabs but gives no figures.

## What makes it good, measured

I read the button, colour and type values from the code of the live web app at duolingo.com on November 16, 2026. I did not measure the phone app directly. Duolingo's public brand guide has been taken down and now leads to its blog, so none of these values come from it. Facts about characters and the redesign come from Duolingo's own posts.

- **One button, used everywhere.** It is 50 pixels tall with rounded corners and 16 pixels of space at each side. The corner setting is 16 pixels, with 12 as the fallback. The face is one flat colour. Under it sits a 4 pixel edge in a darker shade, like the side of a real key. The default is blue #1cb0f6 on #1899d6.
- **The button moves when pressed.** It drops 4 pixels and the dark edge vanishes, so it looks pushed in. With the pointer over it, it gets 10 percent brighter over 200 milliseconds. Switched off, it turns grey #e5e5e5 with paler text #afafaf.
- **Most colours are named after animals.** The colour table I found holds 72. About a dozen have other names, mostly from space. Owl is the brand green, #58cc02. Macaw is blue #1cb0f6. Cardinal is red #ff4b4b. Bee is yellow #ffc800. Fox is orange #ff9600. Beetle is purple #ce82ff.
- **Greys have animal names too.** From dark to light: eel #4b4b4b, wolf #777777, hare #afafaf, swan #e5e5e5, polar #f7f7f7 and snow #ffffff. Text is mostly eel, a dark grey, not pure black: 22 uses of eel against 2 of black in the two style files I read.
- **Dark mode is built into the names.** Of the 72 colours, 26 carry a second value for dark screens. Owl becomes #93d333. Snow becomes a deep blue-black, #131f24.
- **Its own typefaces.** One family, called duolingo-sans in the code, sets nearly everything. A second, called feather, sets big headlines at 36 pixels in owl green.
- **Big, bold type.** Body text is 20 pixels on lines 28 pixels apart. Headings are 16, 20, 24 or 28 pixels, all at weight 700. Small labels are in capitals with a little extra space between letters. Only two weights are used: 400 and 700.
- **Round corners, two sizes.** In the two style files I read, 12 and 16 pixels are the most common corner sizes.
- **Ten characters, each with their own mouths.** The team says it drew a set of more than 20 mouth shapes for every character, to match the sounds of speech. The mouth and the body are animated as two layers that run at the same time. A character idles (nods, blinks), speaks when you tap a word, then reacts to whether your answer was right.
- **Small files.** The characters are built in Rive, a tool for animation that responds to input. In the video-call feature, the character Lily has eight head moves and eight body moves that mix into 64 idle combinations. Her whole file is under one megabyte.
- **Drawing rules.** A 2020 post by illustrator Megan Barker sets them out: round, friendly shapes; the fewest details that still read clearly; key features pushed almost to caricature; white space around every picture.
- **How the 2026 refresh was chosen.** The team built four directions: bold solid headers, soft gradients, cards, and flat with lots of white space. The final design uses header sizes that depend on the tab's job, titles always on the left, fewer type styles, and white space in place of boxes.

### Why it's here

It is the warm, playful pole of the shelf. The lesson for Designcraft: playful is a system, not decoration. One button that behaves like a toy, a named set of colours, and characters that act as the feedback for right and wrong.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. He said nothing about this one by itself.

Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window." He picked no favourite. It stays on the shelf as one end of the range.

## More details

- Duolingo on the 2026 tab refresh (four directions, final rules, iPhone first): https://blog.duolingo.com/core-tabs-redesign/
- Apple's 2023 Apple Design Awards announcement (Delight and Fun, the reasons): https://www.apple.com/newsroom/2023/06/apple-announces-winners-of-the-2023-apple-design-awards/
- Duolingo's letter to shareholders for July to September 2026 (daily, monthly and paying users): https://www.sec.gov/Archives/edgar/data/0001562088/000162828026069474/q3fy26duolingo9-30x26share.htm
- Duolingo on the streak change and its test results (November 19, 2020): https://blog.duolingo.com/improving-the-streak
- Duolingo on character mouths and how lip movement is timed (November 10, 2022): https://blog.duolingo.com/world-character-visemes
- Rive on Lily's video call (64 idle combinations, file under one megabyte; March 20, 2025): https://rive.app/blog/duolingo-s-ai-powered-video-call-brings-lily-to-life
- Duolingo on its drawing style (July 2, 2020): https://blog.duolingo.com/shape-language-duolingos-art-style/
- The live web app whose code I read: https://www.duolingo.com/
- App Store rating read from Apple's public App Store data on November 16, 2026.
- My measurements: I saved the home page, its two style files and its script files with curl. Button sizes and timings are from the style files. Colour names and values are from a colour table in the scripts. The live site asks for a sign-in before it shows a lesson, so I could not check these values on a lesson screen itself.

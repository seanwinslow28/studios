# The UK government's website and its design system: "Check if you need a UK visa"

## What it is

The UK government runs one website for everything it does. Its name is its address, written in capitals with a dot in the middle. The Government Digital Service, a team inside government, designs it. Since June 22, 2018, the same team has published its design system: a free, public kit of type sizes, colours, parts and page layouts that any government service can build with.

This entry looks at one small service built from that kit. "Check if you need a UK visa" asks three questions and gives an answer. It is plain on purpose.

See it: https://www.gov.uk/check-uk-visa/y/usa

**Best screen: that page, the second question.** One question in large type. Three answers to pick from. One green button. Under it, a short list of what you have answered so far, each with a "Change" link. There is nothing else to look at.

## How it turned out

- **Design of the Year 2013.** The Design Museum in London gave the site, GOV.UK, its overall prize on April 16, 2013, from 98 entries. The museum's director called it "the Paul Smith of websites".
- **D&AD Black Pencil, 2013.** D&AD is the UK's main award for design and advertising. Its Black Pencil is the top level and is not given every year. GOV.UK won one of four given that year, in the Writing for Design category. The government team says it was the first Black Pencil ever given in that category.
- **Reused at scale.** By February 2020 the team said the kit's code ran in more than 300 services and saved about £17 million a year. Those are the maker's own figures. The code package was downloaded 233,523 times in the week of November 9 to 15, 2026.
- **The maker kept it.** The design principles behind it were first published on April 3, 2012. They are still up, and gained an eleventh on April 2, 2025. The code is still worked on: version 6.0.0 came out on February 9, 2026, and 6.6.0 on October 15, 2026.
- **Not confirmed:** I have read that other countries built their systems on this one. I could not find that on a page I could check, so it is not claimed here.

## What makes it good, measured

I read these from the live pages and their style file on November 16, 2026, and from the design system's own guides. I walked the service as a United States passport holder coming for tourism.

- **Steps:** one start page, three questions, one answer page. That is three choices and four presses of the green button.
- **One question per page.** The second question page holds 52 words, three options and one button. It has no pictures. The start page holds 160 words and no form fields at all.
- **Your answers live in the web address.** After three answers the address ends in /y/usa/no/tourism. So the back button works, and an answer page can be saved or sent to someone. Each past answer has its own "Change" link.
- **One typeface, two weights.** GDS Transport, with Arial as the fallback. The government's press release says Margaret Calvert designed the original in the 1960s. Only regular (400) and bold (700) are used.
- **Large type.** Body text is 19 pixels on lines 25 pixels apart, on phones and desktops alike. The question is 36 pixels on a wide screen and 27 on a phone.
- **Each colour has one job.** Text is near-black #0b0c0c on white #ffffff. Links are blue #1a65a6. The button is green #0f7a52. Errors are red #ca3535. Yellow #ffdd00 is used only to show which thing the keyboard is on. The brand blue is #1d70b8.
- **Spacing in steps of five.** The guide's scale runs 5, 10, 15, 20, 25, 30, 40, 50 and 60 pixels. On phones the larger steps shrink, so 60 becomes 40.
- **Narrow on purpose.** The page stops growing at 960 pixels wide, and text sits in the left two-thirds of that. The guide says no more than 75 characters to a line.
- **Big, square controls.** Each round option button is 40 pixels across inside a 44 pixel tap area. Text boxes are 40 pixels tall with a 2 pixel black edge. Buttons and boxes have square corners.
- **The button says it is a button.** It has a 2 pixel darker strip under it (#083d29). It darkens when the pointer is over it and drops 2 pixels when pressed.
- **No animation at all.** The style file has no timed changes and no animations. Every change is instant.
- **You can always see where you are.** A link in keyboard focus turns yellow with a thick black line under it. A focused option gets a 4 pixel yellow ring.
- **Errors show in two places.** Press the button with nothing picked and a red-edged box appears at the top saying "There is a problem", with a link that jumps to the question. The same message sits next to the question in bold red, with a 5 pixel red bar down the side. For people who use a screen reader, the message starts with a hidden word, "Error:", so it does not rely on colour.
- **Written rules, not taste.** The guide says: label the button "Continue", not "Next". Put it on the left. Never mark required fields with a star. Write "(optional)" on the few that are.
- **Readable by everyone.** The guide says text and controls must meet level AA for contrast in WCAG 2.2, the international standard for accessible websites.

### Why it's here

It is the plain pole of the shelf. The lesson for Designcraft: clear is something you build. Ask one thing at a time, give each colour one job, and design the error and the keyboard states before the pretty ones.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. He said nothing about this one by itself.

Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window." He picked no favourite. It stays on the shelf as one end of the range.

## More details

- UK government press release on Design of the Year 2013 (date, 98 entries, the director's phrase, Margaret Calvert): https://www.gov.uk/government/news/govuk-wins-design-of-the-year-2013
- Government Digital Service on the D&AD Black Pencil (category, first in that category): https://gds.blog.gov.uk/2013/07/02/pencils/
- It's Nice That on the 2013 D&AD winners (GOV.UK as one of four Black Pencils): https://www.itsnicethat.com/articles/d-and-ad-2013-winners
- D&AD's own listing (2013, Writing for Design): https://www.dandad.org/work/d-ad-awards-archive/govuk
- Launch of the GOV.UK Design System (June 22, 2018): https://gds.blog.gov.uk/2018/06/22/introducing-the-gov-uk-design-system/
- Government Digital Service on use in more than 300 services and the £17 million estimate (February 28, 2020): https://gds.blog.gov.uk/2020/02/28/podcast-gov-uk-design-system/
- Government design principles (first published 2012, updated 2025): https://www.gov.uk/guidance/government-design-principles
- Type sizes: https://design-system.service.gov.uk/styles/type-scale/
- Colours and the contrast rule: https://design-system.service.gov.uk/styles/colour/
- Spacing steps: https://design-system.service.gov.uk/styles/spacing/
- Page width, two-thirds column, 75 characters: https://design-system.service.gov.uk/styles/layout/
- Rules for question pages: https://design-system.service.gov.uk/patterns/question-pages/
- The code, its versions and dates: https://github.com/alphagov/govuk-frontend
- Download count read from the public npm figures for the govuk-frontend package on November 16, 2026.
- My measurements: I saved each page of the service and its style file with curl, then counted words, options and buttons inside the main part of each page. The error page is what the service returns when the second question is sent with no answer. The design system's guide now gives 1020 pixels as the default page width; the live site measured 960.

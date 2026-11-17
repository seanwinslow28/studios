# Linear, the app and its 2024 redesign

## What it is

Linear is a tool that software teams use to keep track of their work: bugs, tasks, projects and plans. The company of the same name makes it.

In 2024 the team rebuilt the frame of the app: the sidebar, the tabs, the top bars and the colours. They wrote up how they did it on March 28, 2024. The write-up is by co-founder Karri Saarinen, designer Yann-Edern Gillet, and engineers Romain Cascino and Andreas Eldh. They wrote up a lighter refresh on March 12, 2026.

See it: https://linear.app/

**Best screen: the issue view at the top of that page.** It is the app itself, rebuilt in the page's own code, so it is sharp at any size. A narrow sidebar sits on the left. One task fills the middle, with its history underneath. A slim panel of details sits on the right. Nothing on it shouts.

## How it turned out

- **Copied so often the look got a name.** In June 2025 the trade blog LogRocket wrote about "linear design" as a trend named after this product. It said almost every site it had shown the year before still looked the same a year on. My read: that piece is mostly about marketing websites, not app screens, but it shows how far the look spread.
- **The business grew.** On June 10, 2025, TechCrunch reported that Linear raised $82 million at a value of $1.25 billion, with about 80 staff. The company said it had more than 15,000 customers, among them OpenAI, Scale AI and Perplexity.
- **The maker kept it.** The 2026 refresh calls the 2024 work the last major redesign and adjusts it instead of replacing it. The sidebar got dimmer, there are fewer icons and dividing lines, and the grey got warmer.
- **Phone app ratings.** Linear Mobile scores 4.8 out of 5 from 2,375 ratings in the US App Store.
- **No design award found.** I looked and could not confirm one, so none is claimed here.

## What makes it good, measured

I read these from the code of linear.app on November 16, 2026. The app picture at the top of that page is built from the same style settings as the rest of the site. The real app needs an account, so I did not measure it directly. Team size, timeline and the colour method come from Linear's own write-ups.

- **One typeface.** Inter, in one file that can be set to any weight (a "variable" font). The site uses five weights: 300, 400, 510, 590 and 680. The odd numbers are in-between weights, a little heavier than normal without being bold. The font adjusts its own letter shapes for large sizes, so headings need no second typeface. Code is set in Berkeley Mono.
- **Small type, in four steps.** Text in the app picture is 12, 13, 14 or 16 pixels. Sidebar rows are 13 pixels at weight 510.
- **Dense, but on a strict rhythm.** The sidebar is 232 pixels wide. Each row is 28 pixels tall with a 2 pixel gap. The bar above a task is 44 pixels tall. The sidebar in the picture holds 11 rows and 2 group labels. My read: the site's own minimum size for a finger tap is 44 pixels, so these mouse rows are about two-thirds of that. That is how so much fits without feeling cramped.
- **Almost no colour.** The background is near-black, #08090a. Text comes in four greys by importance: #f7f8f8, #d0d6e0, #8a8f98 and #62666d. There is one accent, an indigo: #5e6ad2, with a brighter #7170ff.
- **Lines you barely see.** Dividers are half a pixel to one pixel thick, in white at 5 to 8 percent strength.
- **Corners on a scale.** Corner rounding comes in set steps: 4, 6, 8, 12, 16, 24 and 32 pixels. Sidebar rows use 8. The app window uses 12.
- **A whole theme from three choices.** Before 2024, each colour theme needed 98 separate settings. Now it needs three: a base colour, an accent colour and a contrast level. The team moved to LCH, a way of describing colour where equal steps look equal to the eye. The contrast setting also gives people with weak sight a high-contrast theme.
- **Two speeds of motion.** Quick changes take 100 milliseconds. Regular ones take 250. A hover highlight appears at once and fades out over 150. My read: instant in, soft out is why it feels fast but never flickers.
- **Motion can be turned down.** The site's code checks 41 times whether the visitor has asked their computer for less motion. 17 of those checks cut animation for people who asked. The other 24 add motion only for people who did not.
- **Things line up.** The write-up says labels, icons and buttons were lined up both across and down in the sidebar and tabs.
- **A small team, shipped in stages.** The whole company had three product designers at the time. One co-founder started the concept alone, then two people led the build with help from the rest of the design team. About six weeks of building. It went to staff first behind an on-off switch, then to a share of customers each day, then to everyone.

### Why it's here

It is the calm, dense pole of the shelf. The lesson for Designcraft: density does not come from shrinking everything. It comes from a few strict choices repeated everywhere: one typeface, four greys, one accent, 28 pixel rows.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. He said nothing about this one by itself.

Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window." He picked no favourite. It stays on the shelf as one end of the range.

## More details

- Linear's write-up of the 2024 redesign (team, six weeks, 98 settings down to three, LCH, rollout): https://linear.app/now/how-we-redesigned-the-linear-ui
- Linear's write-up of the 2026 refresh (dimmer sidebar, fewer icons and lines, warmer grey): https://linear.app/now/behind-the-latest-design-refresh
- LogRocket on "linear design" as a trend named after the product (June 7, 2025): https://blog.logrocket.com/ux-design/linear-design
- TechCrunch on the $82 million round, $1.25 billion value, staff and customer count (June 10, 2025): https://techcrunch.com/2025/06/10/atlassian-rival-linear-raises-82m-at-1-25b-valuation/
- The page measured (typeface, sizes, colours, row heights, speeds): https://linear.app/
- Linear Mobile's rating read from Apple's public App Store data on November 16, 2026.
- My measurements: I saved the home page and its 47 style files with curl and read the settings from them. The row, sidebar and bar sizes are from the app picture on the home page, not from the signed-in app.

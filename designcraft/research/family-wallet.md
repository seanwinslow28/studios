# Family, the crypto wallet, and its "Family Values" essay (2024)

## What it is

Family is a crypto wallet for iPhone. It is the kind where you hold your own keys and no company holds your money. A studio called Los Feliz Engineering built it over about two years. The trade press calls Benji Taylor the founder of Family.

On July 8, 2024, an essay called "Family Values" went up on Taylor's own site. It explains how the app was designed, with a short screen recording beside almost every point. The app is known less for how it looks than for how it behaves: how things move, respond and change state.

See it: https://benji.org/family-values

**Best moment: the tray clips in the section on simplicity.** A tray is a panel that slides up over the screen to hold one small task. Watch one tray turn into the next. The panel changes height and its contents swap, but it never leaves the screen. You always know where you are and how you got there.

## How it turned out

- **Bought within the trade.** On November 16, 2023, The Block reported that Aave Companies, the firm behind the crypto lender Aave, had bought the studio and taken on its whole team. Taylor became senior vice president of product and design. The price was not disclosed.
- **Copied, it seems by name.** A web parts library, Cult UI, ships a part called Family Drawer that works the same way as the app's tray. My read: it is named after the app, though its page does not say so. The same team's own website panel, ConnectKit, has over 1,000 stars on GitHub, the site where developers share code.
- **The designer was sought after.** On March 25, 2026, CoinDesk reported that X had hired Taylor as its head of design. X's product lead said one of Taylor's past products was among the best designed he had seen. The article does not say which product he meant.
- **The app itself is being closed.** On February 3, 2026, the owner said it would wind the wallet down to focus on its lending product. Cointelegraph reported the plan: no new sign-ups from April 1, 2026, and the app closing on April 1, 2027. I found no source confirming that sign-ups did stop, and the app's own site still showed a download button on November 16, 2026. The owner's chief said that reaching millions of people takes products built for one purpose, such as saving, not a broad wallet.
- **Few ratings.** 4.7 out of 5 from 144 ratings in the US App Store. That is a small number next to the other apps on this shelf.
- **Not found:** user numbers or a design award. My read: the craft was admired and copied, but it did not make the product last. That is worth knowing before borrowing from it.

## What makes it good, measured

The rules below come from the essay. I counted the essay's clips and read their lengths with ffprobe, a video tool, without saving them. The app's own timings are not published. So the timings come from ConnectKit, the same team's open-source panel for websites, which resizes between steps the way the tray does. I read them from its public code on November 16, 2026.

- **Three principles:** simplicity, fluidity and delight. The essay is about 4,200 words.
- **Shown, not told.** It has 53 clips. They run from 2.7 to 20.2 seconds, with a middle value of 5.4 seconds. All are recorded at 60 frames a second in the tall shape of a phone screen. Together they last 5 minutes 26 seconds.
- **One job per tray.** Each tray holds one piece of content or one main action.
- **Every tray has the same two fixed parts:** a title and an icon. The icon closes the first tray, or steps back through a chain of them.
- **Each tray is a different height from the last.** The essay says this is on purpose, so the change is easy to see.
- **Trays for short tasks, full screens for things that stay.** A tray can also start a longer flow that then takes over the whole screen.
- **Things travel instead of swapping.** Tabs slide in the direction of the tab you tapped. After you confirm a send, the spinner moves down to the Activity tab, where that send will be listed.
- **Words change in place.** When a button goes from "Continue" to "Confirm", the shared letters "Con" stay put and only the rest changes. Commas in a number slide over as you type more digits.
- **Delight is saved for a few moments.** Confetti when you back up your wallet. Deleted items tumble into a bin with a sound. The code you show to receive money ripples when touched.
- **Timings from the web panel:** the box changes size in 200 milliseconds. Old content fades out over 220. New content waits 55, then fades in over 165.
- **It arrives slower than it leaves.** On phones the panel slides in over 300 milliseconds on a curve that goes slightly past its mark and settles. It leaves in 130. My read: that slow-in, fast-out split is why it feels both soft and quick.
- **No double taps.** The panel ignores taps for 360 milliseconds while it changes.
- **Small feedback is fast.** Buttons change colour in 200 milliseconds and shift in 100. The panel's corners are rounded at 20 pixels.

### Why it's here

It is the shelf's example of behaviour over looks. The lesson for Designcraft: keep the person oriented by never letting anything just appear or vanish. One panel that changes shape teaches more than five screens that replace each other.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. This was one of the three the lead recommended, and of those he said: "amazing and very much what I hope Designcraft can produce for me."

He would not name it the house look. Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window."

He agreed it is the starting point for app and product screens when a job names no look of its own: "Those will be the starting points to look at."

## More details

- The essay (principles, tray rules, every example named above): https://benji.org/family-values
- The Block on the purchase (November 16, 2023): https://www.theblock.co/post/263372/aave-rebrands-to-avara-acquires-software-developer-behind-ethereum-wallet-family
- The Block on the wind-down (February 3, 2026): https://www.theblock.co/news/defi/2026-02-03-aave-labs-sunsets-avara-umbrella-brand-388342
- Cointelegraph on the closing dates and the reason given (February 4, 2026): https://cointelegraph.com/news/aave-shuts-down-avara-family-wallet-refocus-defi
- CoinDesk on Taylor's hire at X (March 25, 2026): https://www.coindesk.com/business/2026/03/25/elon-musk-s-x-hires-crypto-savvy-design-lead-as-x-money-payments-push-inches-closer
- Cult UI's Family Drawer: https://www.cult-ui.com/docs/components/family-drawer
- ConnectKit's public code, where the timings were read (1,074 stars on November 16, 2026): https://github.com/family/connectkit
- The app's own site, still up: https://family.co/
- My measurements: clip count and lengths are from the essay page. Timings are from two files in ConnectKit's modal folder. They describe the website panel, not the phone app, and may differ from it.

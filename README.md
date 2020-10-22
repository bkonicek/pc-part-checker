![PC Part Price Checker](https://github.com/bkonicek/pc-part-checker/workflows/PC%20Part%20Price%20Checker/badge.svg)

# PC Parts List
I created this when I was planning to build a new PC. A local reseller kept a Google Sheet with his inventory
and I wanted to monitor it for any price changes.

This is a work in progress and is definitely not going to be pretty code. If you see anything especially
egregious feel free to let me know.

I'm also treating this as a fun project to practice DevOps skills, so it's most likely going to end up incredibly over-engineered.

## Usage
Set the following environment variables:
- `SHEET_ID` - ID of the spreadsheet to pull from
- `ITEM_CATEGORIES` - Comma separated list of Item categories you want
- `ITEM_RANGES` - Comma separated list of ranges on the sheet - should correspond to each of the above Item Categories
- `SHEETS_API_KEY` - API key in Google API console for this app to use
- `DB_HOST` - Hostname and port of the MongoDB server
- `CHECK_INTERVAL` (optional) - Frequency to check for new prices
- `APPRISE_CONFIG_STRING` - Notification definition
- `APPRISE_CONFIG_URL` - Path or URL to config file for apprise notifications

## TODO
- [x] Pull each item and its price per category I'm interested in from the table
- [x] Add most recent price to a db table
- [x] Send alert if any item's price changes (email/slack/sms?) - Use [apprise-api](https://github.com/bkonicek/apprise-api)?
- [ ] Add logging
- [ ] Bulk send price drops instead of individual emails
- [x] Dockerize it
- [ ] Get environment variables from external sources (e.g. KeyVault)
- [x] Add CI
- [x] Add CD
- [ ] Figure out where it should run from

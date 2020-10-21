# PC Parts List
I created this when I was planning to build a new PC. A local reseller kept a Google Sheet with his inventory
and I wanted to monitor it for any price changes.

## Usage
Set the following environment variables:
- `SPREADSHEET_ID` - ID of the spreadsheet to pull from
- `ITEM_CATEGORIES` - Comma separated list of Item categories you want
- `ITEM_RANGES` - Comma separated list of ranges on the sheet - should correspond to each of the above Item Categories
- `API_KEY` - API key in Google API console for this app to use

## TODO
- [x] Pull each item and its price per category I'm interested in from the table
- [ ] Add most recent price to a db table
- [ ] Send alert if any item's price changes (email/slack/sms?) - Look into Apprise
- [ ] Dockerize it
- [ ] Add CI/CD pipeline
- [ ] Figure out where it should run from
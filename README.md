# ✈️ Google Flights Deals API: cheap destinations as clean JSON

Give it an airport and get back the thirty cheapest destinations you can fly to from there, as structured JSON. Each one comes with the price, the typical price for that route, exact dates, airline, stops, duration, a photo, and a booking link.

**The part nobody else gives you: which of them are actually bargains.** A cheap fare and a good deal are not the same thing.

**Actor:** [Google Flights Deals API on Apify Store](https://apify.com/johnvc/google-flights-deals-api?fpr=9n7kx3)

## Video Walkthrough

https://www.youtube.com/watch?v=jREWahDGhJM

## Quick Start

```bash
git clone https://github.com/johnisanerd/Apify-Google-Flights-Deals-API.git
cd Apify-Google-Flights-Deals-API
cp .env.example .env          # paste your Apify token
uv sync
uv run google-flights-deals-api-example.py
```

Get a free Apify API key at [apify.com](https://apify.com?fpr=9n7kx3).

## Why Use This Google Flights Deals API?

- **Bargain detection, not just cheap fares.** Every row carries `average_price`, what that route typically costs, plus `savings`, `savings_percent`, and an `is_below_typical` flag.
- **One call, thirty bookable options.** Each with real dates and a link that goes straight to the booking page.
- **A real filter surface.** Cabin class, max price, max stops, trip length, airline include or exclude.
- **No arrival airport needed.** This answers "where can I go cheaply from here", so the source ignores a destination by design.

## An honest note on the data

Measured across three hubs, roughly **6 to 30% of the feed genuinely beats its typical price**, depending on the airport. The rest are cheap in absolute terms without being discounts, usually short-haul routes. That is the nature of the source, and it is exactly why `is_below_typical` exists: it turns a list of cheap flights into a list you can filter for bargains.

One limit worth knowing: setting `maxDurationMinutes` makes the source stop returning the typical-price baseline, so that single filter turns off bargain detection. Every other filter keeps it, including one way.

## Features

| Feature | Detail |
|---|---|
| Bargain flag | `is_below_typical` is true only when the fare beats its own route's typical price |
| Derived savings | `savings` and `savings_percent`, computed locally on every row |
| Multi-airport | `departureIds` watches several home airports in one run |
| Filters | cabin class, max price, max stops, trip length preset, airline include or exclude |
| Booking links | `flight_link` goes straight to the itinerary |
| Localization | `currency`, `hl`, and `gl` |

## Usage Examples

Nonstop options under a budget:

```python
run_input = {"departureId": "LAX", "maxStops": "nonstop", "maxPrice": 400}
```

Weekend trips from a set of home airports:

```python
run_input = {"departureIds": ["JFK", "EWR", "LGA"], "travelDuration": "weekend"}
```

Business class bargains:

```python
run_input = {"departureId": "LAX", "travelClass": "business"}
```

## Input Parameters

| Parameter | Type | Description |
|---|---|---|
| `departureId` | string | 3-letter IATA code, such as JFK. |
| `departureIds` | array | More airports. Each is one lookup. |
| `tripType` | select | Round trip (default) or one way. Both keep the savings baseline. |
| `outboundDate` / `returnDate` | string | YYYY-MM-DD. Leave blank to let the feed pick cheap dates. |
| `travelDuration` | select | any, one_week, weekend, two_weeks |
| `tripLength` | string | Exact days, as `7` or a range like `5-10`. |
| `travelClass` | select | economy, premium_economy, business, first |
| `maxPrice` | integer | Drop deals above this price. |
| `maxStops` | select | any, nonstop, one_stop, two_stops |
| `maxDurationMinutes` | integer | Drop longer deals. Turns off bargain detection, see above. |
| `includeAirlines` / `excludeAirlines` | string | Comma-separated codes. Mutually exclusive. |
| `maxDealsPerAirport` | integer | Default and maximum 30. |
| `currency`, `hl`, `gl` | string | Currency, language, country. |

## Output Format

One row per destination:

```json
{
  "result_type": "deal",
  "position": 1,
  "departure_id": "JFK",
  "name": "Nantucket",
  "country": "United States",
  "price": 295,
  "average_price": 478,
  "savings": 183.0,
  "savings_percent": 38.3,
  "is_below_typical": true,
  "route": "JFK to ACK",
  "outbound_date": "2026-10-01",
  "return_date": "2026-10-08",
  "flight_duration": 282,
  "stops": 1,
  "airline": "JetBlue",
  "flight_link": "https://www.google.com/travel/flights?tfs=..."
}
```

Negative savings are preserved rather than hidden: knowing a "deal" sits above its typical price is useful information.

This Actor returns a snapshot. It does not track prices over time, keep history, or send alerts. It is the data layer you build a price-alert product on.

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Google Flights Deals API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/google-flights-deals-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Google Flights Deals API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-flights-deals-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-flights-deals-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Google Flights Deals API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/google-flights-deals-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/google-flights-deals-api`, using OAuth when prompted.
5. Ask Claude to run the Google Flights Deals API.

Open Claude on the web: https://claude.ai/referral/uIlpa7nPLg

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-flights-deals-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-flights-deals-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Google Flights Deals API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/google-flights-deals-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Google Flights Deals API to power local lead lists, market research, and place data for your product or AI agent.*

## Featured Tasks

Ready-to-run examples on the Apify Store, each targeting one local-data use case:

- [Extract local business leads from Google Maps by API](https://apify.com/johnvc/google-flights-deals-api/examples/extract-local-business-leads-from-google-maps-by-api?fpr=9n7kx3)
- [Extract phone numbers from Google Maps by zip code](https://apify.com/johnvc/google-flights-deals-api/examples/extract-phone-numbers-from-google-maps-by-zip-code?fpr=9n7kx3)
- [Find roofing contractor leads in Tampa with phone numbers](https://apify.com/johnvc/google-flights-deals-api/examples/find-roofing-contractor-leads-in-tampa-with-phone-numbers?fpr=9n7kx3)
- [Build a list of med spas in Miami with phone numbers](https://apify.com/johnvc/google-flights-deals-api/examples/build-a-list-of-med-spas-in-miami-with-phone-numbers?fpr=9n7kx3)
- [Generate local leads in Claude via Google Maps MCP](https://apify.com/johnvc/google-flights-deals-api/examples/generate-local-leads-in-claude-via-google-maps-mcp?fpr=9n7kx3)
- [Export Google Maps Places to CSV](https://apify.com/johnvc/google-flights-deals-api/examples/export-google-maps-places-to-csv?fpr=9n7kx3)

Last Updated: 2026.09.20

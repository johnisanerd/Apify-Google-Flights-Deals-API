"""
Google Flights Deals API: A Quick Start Example
See more at: https://apify.com/johnvc/google-flights-deals-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-flights-deals-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Flights Deals API on Apify from Python
and read its structured JSON output: the 30 cheapest destinations reachable from
one airport, each with the price, what that route typically costs, the saving
against it, exact dates, airline, stops, duration, and a booking link.

The field worth knowing about is is_below_typical. A cheap fare and a good deal
are not the same thing, and this tells you which is which.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# There is no arrival airport: this Actor answers "where can I go cheaply from
# here", so the source ignores a destination by design.
run_input = {
    "departureId": "JFK",
    "maxDealsPerAirport": 30,   # 30 is both the default and the maximum
    "currency": "USD",
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/google-flights-deals-api").call(run_input=run_input)

# Read structured results from the run's default dataset.
# apify-client 3.x returns a typed Run object, so use the attribute (not run["defaultDatasetId"]).
items = list(client.dataset(run.default_dataset_id).iterate_items())

deals = [i for i in items if i.get("result_type") == "deal"]
errors = [i for i in items if i.get("result_type") == "error"]

bargains = [d for d in deals if d.get("is_below_typical")]
print(f"{len(deals)} destination(s), {len(bargains)} genuinely below typical price\n")

# Sort by how far below typical each one sits, best first.
for d in sorted(bargains, key=lambda x: -(x.get("savings_percent") or 0))[:10]:
    print(f"  {d['name']} ({d.get('country')})")
    print(f"     {d.get('route')}  {d.get('outbound_date')} to {d.get('return_date')}")
    print(f"     ${d['price']} vs ${d['average_price']} typical, "
          f"save ${d.get('savings')} ({d.get('savings_percent')}%)")
    print(f"     {d.get('airline', 'airline not reported')}, "
          f"{d.get('stops')} stop(s), {d.get('flight_duration')} min")
    print(f"     book: {d.get('flight_link', '')[:74]}")

if not bargains:
    print("  Nothing below typical from this airport right now.")
    print("  That is normal: measured across three hubs, only 6 to 30% of the")
    print("  feed beats its own route's typical price on any given day.")

for e in errors:
    print(f"\n[{e['error_type']}] {e['error_message']}")

# --- Other things you can do -------------------------------------------------
#
# Watch several home airports in one run:
#
#   {"departureIds": ["JFK", "EWR", "LGA"]}
#
# Narrow it down. Every filter below keeps the typical-price baseline:
#
#   {"departureId": "LAX", "maxStops": "nonstop", "maxPrice": 400}
#   {"departureId": "LAX", "travelClass": "business"}
#   {"departureId": "LAX", "travelDuration": "weekend"}
#
# One filter is different: maxDurationMinutes makes the source stop returning
# the baseline, which turns off savings and is_below_typical entirely. The
# Actor logs a warning if you set it.
#
# Build your own fare history by scheduling this and storing rows keyed on
# departure, arrival, and date. The Actor itself keeps no history and sends no
# alerts; it is the data layer you build those on.

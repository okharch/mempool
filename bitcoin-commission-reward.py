#!/usr/bin/env python3
import json
import requests

# API endpoint URL
url = "https://mempool.space/api/v1/mining/reward-stats/1"

# Send GET request and get response
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    # Parse JSON data
    data = json.loads(response.text)

    # Extract relevant information
    start_block = data["startBlock"]
    end_block = data["endBlock"]
    total_reward = int(data["totalReward"]) / 1e8  # miner's reward + commission, BTC
    total_fee = int(data["totalFee"]) / 1e8  # commission, BTC
    total_tx = int(data["totalTx"])

    # Calculate average transaction fee (using commission + total fees)
    average_transaction_fee = total_reward / total_tx
    average_commission = total_fee / total_tx

    # Print information
    print(f"Block range: {start_block} - {end_block}")
    print(f"Miner's reward: {total_reward-total_fee:.8f} BTC")
    print(f"Commission: {total_fee:.8f} BTC")
    print(f"Total transaction reward: {total_reward:.8f} BTC")
    print(f"Average transaction fee: {average_transaction_fee:.8f} BTC")
    print(f"Average commission fee: {average_commission:.8f} BTC")
    print(f"Total transactions: {total_tx}")
else:
    print(f"Error: API request failed with status code {response.status_code}")

#! /usr/bin/python3

import argparse
import json
import requests


def calculate_block_stats(count_block):
    url = f"https://mempool.space/api/v1/mining/reward-stats/{count_block}"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)

        total_reward = int(data["totalReward"])   # Reward + commission, BTC
        total_fee = int(data["totalFee"]) # Commission, BTC
        total_tx = int(data["totalTx"])
        end_block = int(data["endBlock"])

        print (f"EndBlock: {end_block}, Url: {url}")

        return {"block": f"{data['startBlock']} - {data['endBlock']}",
            "end_block": end_block,
            "url": url,
            "total_reward": total_reward,
            "total_fee": total_fee,
            "total_transactions": total_tx,
        }
    else:
        raise Exception(f"Error: API request failed with status code {response.status_code}")


def main():
    parser = argparse.ArgumentParser(description="Calculate bitcoin mining reward stats.")
    parser.add_argument(
        "blocks", type=int, default=1, help="Number of past blocks to analyze (default: 1)"
    )

    args = parser.parse_args()

    blocks = abs(args.blocks)

    # Calculate stats for each block from 1 to blocks
    print(f"Fetching stats for the last {blocks} blocks...")
    max_block = 0
    update_max_block = True
    stats = {}
    end_block = 0
    while update_max_block:
        update_max_block = False
        current_block = 0
        # check each block if it has the latest block
        while current_block < blocks:
            current_block += 1
            block_stats = stats.get(current_block)
            # check if there is a block_stats for the current block
            loaded = not (block_stats is None)
            end_block = 0
            if loaded:
                end_block = block_stats["end_block"]
            # if end block is less than the max block
            if not loaded or end_block < max_block:
                block_stats = calculate_block_stats(current_block)
                end_block = block_stats["end_block"]
                if end_block < max_block:
                    update_max_block = True
                stats[current_block] = block_stats
                if end_block > max_block:
                    update_max_block = max_block > 0
                    max_block = end_block


    # Print individual block stats
    print(f"| Block           | Miner      | Commission | Avg. Fee | Avg. Commission | Total Tx | url")
    print(f"| --------------- | ---------- | ---------- | -------- | --------------- | -------- | ---")
    rolling_reward = 0
    rolling_fee = 0
    rolling_transactions = 0
    current_block = 0
    # check each block if it has the latest block
    while current_block < blocks:
        current_block += 1
        block_stats = stats[current_block]
        # calculate current block
        fee = block_stats["total_fee"] - rolling_fee
        reward = block_stats["total_reward"] - rolling_reward
        transactions = block_stats["total_transactions"] - rolling_transactions
        url = block_stats["url"]

        # update rolling (previous)
        rolling_fee = block_stats["total_fee"]
        rolling_reward = block_stats["total_reward"]
        rolling_transactions = block_stats["total_transactions"]


        print(
            f"| {block_stats['block']} |  {reward-fee} | {fee:10} | {int(reward/transactions):8} | {int(fee/transactions):15} | {transactions:8} | {url}"
        )

    # Print total stats
    print(f"| --------------- | ---------- | ---------- | -------- | --------------- | -------- | ---")
    print(
         f"| Total           | {rolling_reward:10} | {rolling_fee:10} | {int(rolling_reward/rolling_transactions):8} | {int(rolling_fee/rolling_transactions):15} | {rolling_transactions:8} |"
    )


if __name__ == "__main__":
    main()

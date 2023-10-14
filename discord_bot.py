import os
import requests
import discord
import dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
dotenv.load_dotenv()
token = os.getenv("DC_SECRET")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("$GM"):
        await message.channel.send("GM Ser!")

    if message.content.startswith("$help"):
        embed = discord.Embed(title="Cryptocurrency Price Checker Help", color=discord.Color.green())
        embed.add_field(name="Command: $hello", value="Say hello to the bot.", inline=False)
        embed.add_field(name="Command: $GM", value="Have someone say good morning because you're single.", inline=False)
        embed.add_field(name="Command: $help", value="Display the help message.", inline=False)
        embed.add_field(name="Command: $trending", value="Look at the top trending coin searches on CoinGecko.", inline=False)
        embed.add_field(name="Command: $search <phrase>", value="Search for namespaces related to the provided phrase.", inline=False)
        embed.add_field(name="Command: $platforms", value="List all asset platforms.", inline=False)
        embed.add_field(name="Command: $nftList <platform_id>", value="Search for NFTs on a particular network. Use $platforms to get platform IDs.", inline=False)
        embed.add_field(name="Command: $exchange <exchange_id>", value="View information about a specific exchange. Use $viewexchangeid to get exchange IDs.", inline=False)
        embed.add_field(name="Command: $viewexchangeid", value="View a list of exchange IDs.", inline=False)

        await message.channel.send(embed=embed)
    # if message.content.startswith("$help"):
    #     await message.channel.send("Hello, welcome to the Cryptocurrency Price Checker!\nTo check the price of a cryptocurrency, type $price followed by the name of the cryptocurrency.\nTo have someone say good morning because you're single, type $GM.\nTo look at the top trending coin searches on CoinGecko, type $trending.\nTo search for namespaces related, type $search followed by a phrase.\nTo list all asset platforms, type $platforms.\nTo search for NFTs on a particular network, type $nftList followed by the network acquired from $platforms.\nTo pass the exchange id, type $exchange follwed by the exchange id.\nTo view exchange id, type $viewexchangeid.")

    if message.content.startswith("$trending"):
        url = "https://api.coingecko.com/api/v3/search/trending"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                trending_coins = data['coins']

                embed = discord.Embed(title="Trending Coins", color=discord.Color.orange())
                for coin in trending_coins:
                    name = coin['item']['name']
                    market_cap_rank = coin['item']['market_cap_rank']
                    symbol = coin['item']['symbol']
                    embed.add_field(name=f"Rank {market_cap_rank}", value=f"Name: {name}, Symbol: {symbol}", inline=False)

                await message.channel.send(embed=embed)

        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    if message.content.startswith("$search"):
        exchange_string = message.content.split("$search ", 1)[1].lower()

        url = f"https://api.coingecko.com/api/v3/search?query={exchange_string}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get(
                'coins')  # Assuming the API response contains an array of coins
                if results:
                    coin_names = [coin.get('name') for coin in results]
                    await message.channel.send("\n".join(coin_names))
                else:
                    await message.channel.send("No search results found.")
            else:
                await message.channel.send(f"Error: Unable to fetch search results. Response content: {response.content}")
        except Exception as e:
            await message.channel.send(
                f"Error: An error occurred while processing the request. {str(e)}")

    if message.content.startswith("$platforms"):
        url = "https://api.coingecko.com/api/v3/asset_platforms?filter=nft"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                embed = discord.Embed(title="NFT Asset Platforms", color=discord.Color.blue())
                for item in data:
                    name = item['name']
                    platform_id = item['id']
                    embed.add_field(name=name, value=f"Platform ID: {platform_id}", inline=False)

                await message.channel.send(embed=embed)

        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    if message.content.startswith("$nftList"):
        asset_platform_id = message.content.split("$nftList ", 1)[1].lower()

        url = f"https://api.coingecko.com/api/v3/nfts/list?order=floor_price_native_asc&asset_platform_id={asset_platform_id}&per_page=100&page=1"

        response = requests.get(url)  # Send the API request and store the response

        if response.status_code == 200:
            try:
                data = response.json()

                if not data:  # Check if the response is empty
                    await message.channel.send("No NFTs found for the specified platform.")
                    return

                nft_info = [{"name": nft["name"]} for nft in data]

                if not nft_info:
                    await message.channel.send("No NFTs found for the specified platform.")
                    return

                # Send the NFT information as an embedded message
                embed = discord.Embed(title="NFT List", color=discord.Color.blue())
                for nft in nft_info:
                    embed.add_field(name=nft["name"], value="", inline=False)

                await message.channel.send(embed=embed)

            except Exception as e:
                await message.channel.send(f"An error occurred: {str(e)}")

    if message.content.startswith("$exchange"):
        exchange_id = message.content.split("$exchange ", 1)[1].lower()

        url = f"https://api.coingecko.com/api/v3/exchanges/{exchange_id}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                exchange_name = data.get('name')
                exchange_country = data.get('country')
                exchange_year_established = data.get('year_established')
                exchange_description = data.get('description')
                exchange_url = data.get('url')
                exchange_image = data.get('image')
                facebook_url = data.get('facebook_url')
                reddit_url = data.get('reddit_url')
                telegram_url = data.get('telegram_url')
                slack_url = data.get('slack_url')
                other_url_1 = data.get('other_url_1')
                other_url_2 = data.get('other_url_2')

                response_message = (
                    f"Exchange Name: {exchange_name}\n"
                    f"Country: {exchange_country}\n"
                    f"Year Established: {exchange_year_established if exchange_year_established else 'None'}\n"
                    f"Description: {exchange_description if exchange_description else 'None'}\n"
                    f"URL: {exchange_url}\n"
                    f"Image: {exchange_image}\n"
                    f"Facebook: {facebook_url if facebook_url else 'None'}\n"
                    f"Reddit: {reddit_url if reddit_url else 'None'}\n"
                    f"Telegram: {telegram_url if telegram_url else 'None'}\n"
                    f"Slack: {slack_url if slack_url else 'None'}\n"
                    f"Other URL 1: {other_url_1 if other_url_1 else 'None'}\n"
                    f"Other URL 2: {other_url_2 if other_url_2 else 'None'}"
                )

                await message.channel.send(response_message)
            else:
                await message.channel.send(f"Error: Unable to fetch exchange data. Response content: {response.content}")
        except Exception as e:
            await message.channel.send(f"Error: An error occurred while processing the request. {str(e)}")

    if message.content.startswith("$viewexchangeid"):
        url = "https://api.coingecko.com/api/v3/exchanges/list"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                num_exchanges_to_display = 10
                exchanges = data[:
                                num_exchanges_to_display]  # Limiting the list to 10 exchanges
                exchange_info = []
                for exchange in exchanges:
                    exchange_id = exchange.get('id')
                    exchange_name = exchange.get('name')
                    exchange_info.append(f"ID: {exchange_id}, Name: {exchange_name}")

                await message.channel.send("\n".join(exchange_info))
            else:
                await message.channel.send("Error: Unable to fetch exchange data.")
        except Exception as e:
            await message.channel.send(
                f"Error: An error occurred while processing the request. {str(e)}")
            
try:
    client.run("MTEzMjUwNjEzMTQ0MTQwMTk1OA.GwILVY.4mNm0QktVCLFNBPShSGzVKJgDVghgvEGC2mo7U")
except Exception as e:
    print(e)
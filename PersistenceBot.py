import discord
import requests
import datetime
import asyncio
from pytz import timezone
import math


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# format = "%Y-%m-%d %H:%M:%S %Z%z"

now = datetime.datetime.now(timezone("Asia/Kolkata"))
current_time = now.strftime("%H:%M:%S")
date = now.strftime("%d-%m-%Y")


def millify(n):
    millnames = ["", " Thousand", " Million", " Billion", " Trillion"]
    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )

    return "{:.2f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])


def format_number(value):
    return format(round(float(value), 2), ",f")[:-4]


### Functions to fetch data
###
### Token Stats


def fetch_persistence_price():
    url = "https://api.coingecko.com/api/v3/coins/persistence?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    response = requests.get(url)
    data = response.json()
    price = data["market_data"]["current_price"]["usd"]
    market_cap = data["market_data"]["market_cap"]["usd"]
    ath = data["market_data"]["ath"]["usd"]
    return price, market_cap, ath


price, market_cap, ath = fetch_persistence_price()

# Supply Stats


def fetch_max_supply():
    url = "https://api.coingecko.com/api/v3/coins/persistence?localization=false&tickers=false&market_data=true&community_data=true&developer_data=true&sparkline=false"
    response = requests.get(url)
    data = response.json()
    return format(int(data["market_data"]["max_supply"]), ",d")


max_supply = fetch_max_supply()


def fetch_circulating_supply():
    url = "https://api.coingecko.com/api/v3/coins/persistence?localization=false&tickers=false&market_data=true&community_data=true&developer_data=true&sparkline=false"
    response = requests.get(url)
    data = response.json()
    return format_number(data["market_data"]["circulating_supply"])


cirulating_supply = fetch_circulating_supply()


def fetch_total_supply():
    url = "https://api.coingecko.com/api/v3/coins/persistence?localization=false&tickers=false&market_data=true&community_data=true&developer_data=true&sparkline=false"
    response = requests.get(url)
    data = response.json()
    return format_number(data["market_data"]["total_supply"])


total_supply = fetch_total_supply()


def fetch_community_pool():
    url = "http://rest.core.persistence.one/cosmos/distribution/v1beta1/community_pool"
    response = requests.get(url)
    data = response.json()
    return format_number(data["pool"][-1]["amount"])


community_pool = fetch_community_pool()

# Staking Stats


def fetch_apr():
    url = "https://chains.cosmos.directory/persistence"
    response = requests.get(url)
    data = response.json()
    return data["chain"]["params"]["calculated_apr"]


apr = fetch_apr()


def fetch_staking_ratio():
    url = "https://7nkwv3z5t1.execute-api.us-east-1.amazonaws.com/prod/summary?app=XPRT&accessKey=3fb087cbc907ff1535c283128ecf55f5"
    response = requests.get(url)
    data = response.json()
    return data["stakingRatio"]


staking_ratio = fetch_staking_ratio()


def fetch_total_stake():
    url = "https://7nkwv3z5t1.execute-api.us-east-1.amazonaws.com/prod/summary?app=XPRT&accessKey=3fb087cbc907ff1535c283128ecf55f5"
    response = requests.get(url)
    data = response.json()
    return data["totalStaked"]


total_stake = fetch_total_stake()


def fetch_unbonding_time():
    url = "http://rest.core.persistence.one/cosmos/staking/v1beta1/params"
    response = requests.get(url)
    data = response.json()
    return data["params"]["unbonding_time"][:-2]


unbonding_time = fetch_unbonding_time()
unbonding_time = float(unbonding_time) / (3600 * 24)


def fetch_active_validators():
    url = "http://rest.core.persistence.one/cosmos/staking/v1beta1/params"
    response = requests.get(url)
    data = response.json()
    return data["params"]["max_validators"]


active_validators = fetch_active_validators()


def fetch_nakamoto_coefficient():
    url = "https://7nkwv3z5t1.execute-api.us-east-1.amazonaws.com/prod/summary?app=XPRT&accessKey=3fb087cbc907ff1535c283128ecf55f5"
    response = requests.get(url)
    data = response.json()
    return data["nakamotoCoefficient"]


nakamoto_coefficient = fetch_nakamoto_coefficient()


def fetch_network_score():
    url = "https://api.coingecko.com/api/v3/coins/persistence?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    response = requests.get(url)
    data = response.json()
    return (
        data["coingecko_score"]
        + data["developer_score"]
        + data["community_score"]
        + data["liquidity_score"]
    ) / 4


network_score = fetch_network_score()


def fetch_inflation():
    url = "http://rest.core.persistence.one/cosmos/mint/v1beta1/inflation"
    response = requests.get(url)
    data = response.json()
    return data["inflation"]


inflation = fetch_inflation()


# Chain Activity


def fetch_cum_VTL():
    url = "https://api.llama.fi/v2/chains"
    response = requests.get(url)
    data = response.json()
    return format_number(data[174]["tvl"])


cum_VTL = fetch_cum_VTL()


def fetch_pstake_VTL():
    url = "https://api.llama.fi/protocols/"
    response = requests.get(url)
    data = response.json()
    for protocol in data:
        if protocol["name"] == "pSTAKE Finance":
            return format_number(protocol["chainTvls"]["Persistence"])


pstake_VTL = fetch_pstake_VTL()


def fetch_dexter_TVL():
    url = "https://api.llama.fi/protocols/"
    response = requests.get(url)
    data = response.json()
    return format_number(data[770]["tvl"])


dexter_VTL = fetch_dexter_TVL()

# End of Fetch Functions


@client.event
async def on_ready():
    channel = client.get_channel(1111980883201765386)

    Persistence_stats = discord.Embed(
        title=f":calendar: Date: {date} :calendar: \n **__Persistence Stats - Update/Minute__**",
        color=0x00FF00,
    )

    Persistence_stats.add_field(
        name="",
        value=f":dollar:` XPRT Price:` **${round(price, 3)}**",
        inline=True,
    )
    Persistence_stats.add_field(
        name="",
        value=f":moneybag: `Market Capitalization:` **${millify(market_cap)}**",
        inline=False,
    )
    # Persistence_stats.add_field(name="", value="\n")

    Persistence_stats.add_field(
        name="",
        value=f"\U0001F680`All-time high:` **${round(ath, 3)}**",
        inline=False,
    )
    Persistence_stats.add_field(name="", value="```Supply Stats```", inline=False)
    Persistence_stats.add_field(
        name="",
        value=f":left_luggage: `Max Supply:` **{(max_supply)}**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f":recycle: `Circulating Supply:` **{(cirulating_supply)}**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f":briefcase: `Total Supply:` **{(total_supply)}**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f":classical_building: `XPRT Community Pool:` **{((community_pool))}**",
        inline=False,
    )

    Persistence_stats.add_field(name="", value="\n")
    Persistence_stats.add_field(name="", value="```Staking Stats```", inline=False)
    Persistence_stats.add_field(
        name="", value=f":trophy: `APR:` **{round(apr*100,2)}%**", inline=False
    )
    Persistence_stats.add_field(
        name="",
        value=f"\U0001F9EE`Staking Ratio:` **{staking_ratio}**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="", value=f"\U00002795`Total Stake:` **{total_stake}**", inline=False
    )
    Persistence_stats.add_field(
        name="",
        value=f":unlock: `Unbonding Period:` **{unbonding_time} Days**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f"\u2705`Active Validators:` **{active_validators}**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f"\U0001F1F3`Nakamoto Coefficient:` **{nakamoto_coefficient}**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f":bar_chart: `Overall Network Score(Observatory):` **{round(network_score,2)}%**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f":printer: `Inflation:` **{round((float(inflation)*100),2)}%**",
        inline=False,
    )

    """Persistence_stats.add_field(name="\n**IBC Data**", value="", inline=False)
        Persistence_stats.add_field(name=":satellite: IBC Volume", value=IBC_Volume,inline=False)
        Persistence_stats.add_field(name=":world_map: IBC Txs", value=IBC_txs,inline=False)
        Persistence_stats.add_field(name=":compass: MAU", value=MAU,inline=False)
        Persistence_stats.add_field(name=" :raised_hand: Peers", value=peers,inline=False)
        Persistence_stats.add_field(name=":mailbox: Channels", value=channels,inline=False)"""

    Persistence_stats.add_field(name="", value="```Chain Activity```", inline=False)
    """Persistence_stats.add_field(
            name="",
            value=f":heavy_multiplication_x:`Total Transactions:` **{total_txs}**",
            inline=False,
        )"""
    Persistence_stats.add_field(
        name="",
        value=f"\U0001F517 `Cumulative Chain TVL:` **{(cum_VTL)}**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f":fist: `pStake for Cosmos TVL:` **{pstake_VTL}**",
        inline=False,
    )
    Persistence_stats.add_field(
        name="",
        value=f":pinched_fingers: `Dexter TVL: `**{(dexter_VTL)}**",
        inline=False,
    )

    Persistence_stats.add_field(
        name="",
        value="```Useful Resources```\n \u200b:lizard: CoinGecko: httpss://www.coingecko.com/en/coins/Persistence\n:test_tube: Persistence: httpss://info.Persistence.zone/token/XPRT\n"
        ":desktop: Monitor: httpss://monitor.bronbro.io/d/xprt-stats\n:mag_right: Mintscan: httpss://www.mintscan.io/Persistence\n"
        ":star: Bro Rating: httpss://monitor.bronbro.io/d/bro-rating/\n"
        ":bar_chart: Dexmos App: httpss://www.dexmos.app/\n",
        inline=False,
    )
    embed = await channel.send(embed=Persistence_stats)
    await asyncio.sleep(60)
    await embed.edit(embed=Persistence_stats)


TOKENA = "MTEwMDczNjE2MDczODgzNjcwNg.GViIk5.E4MxUCgbT2hjxaz1S4I3z6aomSUxLotYz6tpyM"
client.run(TOKENA)

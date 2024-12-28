from nextcord.ext import commands
import random


# from nextcord.ext import commands will not work without import nextcord above it
# get error that nextcord is not defined

class Legacy_Random_Facts(commands.Cog):
    def __init__(self, *args, **kwargs):
        self.whale_facts = ["The blue whale is the biggest animal on earth.",
                            "The blue whale grows to lengths of 25 m.",
                            "A group of whales is called a pod.",
                            "A blue whale is about the size of 20 elephants or 15 school buses.",
                            "Blue whales can live up to 80-90 years.",
                            "Blue whales normally swim alone.",
                            "Blue Whales can consume more than 3,000 kg of krill every day.",
                            "The blue whale's poop can be used as fertilizers.",
                            "The blue whale's poop creates algae in the ocean.",
                            "Blue whales are a species of 'baleen' whale.",
                            "Blue whales don't have teeth.",
                            "Blue whales are the loudest animal on earth.",
                            "Blue whales have a seasonal migration pattern.",
                            "A newborn whale is called a calf.",
                            "Blue whales have been endangered since 1970.",
                            "Different organizations are doing their best to preserve blue whales.",
                            "The early humans hunted whales for survival(aka food).",
                            "People hunt blue whales for oil.",
                            "Blue whales can swim as fast as 50 kilometers per hour.",
                            "Blue whales only have two predators, humans and killer whales.",
                            "Many blue whales have scars from the teeth of the killer whales.",
                            "Killer whales attack blue whales in groups. Studies suggest that killer whales are more "
                            "likely to harass the blue whale for fun and not just merely for hunting.",
                            "The blue whale has an unbelievable sense of hearing. . Under the right circumstances, "
                            "each of them can interact and hear each other as far as 1,600-kilometres away.",
                            "Blue whales have a slow reproductive cycle. They only breed just once every three years.",
                            "A blue whale's milk contains about 35-50% milkfat.",
                            "Blue whales start to get in-heat during their adolescent stage.",
                            "In general, the adult stage of the whales starts as early as 6 years old to 13 years old.",
                            "Blue whales are strong divers, they can dive as deep as 1,640 feet(499.872 m).",
                            "Blue whales once walked on land(at least their ancestors did).",
                            "Although blue whales do not have legs anymore, they still have a pelvis.",
                            "Whales share the same names as cows. If the newborn whales are called 'Calves', "
                            "the female whales are called 'Cows', while the male whales are called 'Bulls.'",
                            "Blue whales love to sing. Except for humans, whales are the only mammals on earth who "
                            "can sing.",
                            "Blue Whales aren't a true blue in color.",
                            "Dolphins are whales, but whales aren't dolphins. Whales have two blowholes, "
                            "unlike dolphins who only have one.",
                            "Whales can store oxygen molecules in their bodies.",
                            "Gray whales can travel over 14,000 miles round trip.",
                            "Sperm whales have the biggest brains of any animal on earth!",
                            "Whales communicate through using sound.",
                            "Sperm whales are the loudest animals on earth",
                            "A 60,000-pound whale can jump fully out of the water.",
                            "Whales have multiple stomachs.",
                            "Whales do not chew their food.",
                            "Whales eat some of the smallest prey on earth."]

    @commands.command(aliases=["Whale_Fact", "whale_fact", "Whale_facts", "Whale_Facts", "whale_facts"])
    async def whale(self, ctx):
        """Gives a random whale fact from a list of whale facts."""
        await ctx.send(random.choice(self.whale_facts))


def setup(bot):
    bot.add_cog(Legacy_Random_Facts(bot))

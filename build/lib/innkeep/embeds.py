import re

from discord import Embed
from discord.colour import Colour


IMAGE_TEMPLATE = 'https://art.hearthstonejson.com/v1/render/latest/enUS/512x/{card_id}.png'
CARD_VIEW_TEMPLATE = 'https://hearthpwn.com/{card_id}'


class CardEmbed(object):
    """
    Represents an embed for a single card, to be rendered and returned.
    as a response to a search query.

    Crucially, and perhaps somewhat awkwardly, this class overrides
    `__getattr__` to forward missing attribute access to its card object. This
    little bit of magic makes card attribute accesses shorter and cleaner.  """

    def __init__(self, card):
        self.card = card

        # This is a discord.py Embed object, and is the thing we
        # will be building.
        self.embed = Embed(
            type='rich',
            title=card['name'],
            url=self.url(card),
        )

    def image(self, card):
        return IMAGE_TEMPLATE.format(card_id=self.id)

    def url(self, card):
        return CARD_VIEW_TEMPLATE.format(card_id=self.id)

    def __getattr__(self, attr):
        """
        This allows card_id like `f = self.faction_cost` instead of
        `f = self.card['faction_cost']`.
        """
        if '_' in attr:
            parts = attr.split('_')
            attr = parts[0] + ''.join(x.title() for x in parts[1:])
        return self.card[attr]

    def has(self, name):
        return name in self.card


class CardImage(CardEmbed):
    """
    Returns an embed with a full size card image.
    """
    def render(self):
        self.embed.set_image(url=self.image(self.card))
        return self.embed


class CardText(CardEmbed):
    """
    This is the default embed.

    This returns an embed with a textual representation of the card's text. It
    also includes a link to the card on Hearthstone API as well as a thumbnail of
    the card image.
    """

    def type_line(self):
        parts = ['{} mana'.format(self.cost)]
        if self.type == 'MINION':
            parts.append('{}/{}'.format(self.attack, self.health))
            if self.has('race'):
                parts.append(self.race.title())
        return ' • '.join(parts)

    def text_line(self):
        """
        This transforms the text line to have all the fancy emojis in
        SUBSTITUTIONS, bolded text, and trace superscripts.
        """
        text = self.text.replace('[x]', '')
        text = text.replace('\n', ' ')
        text = text.replace('$', '')
        text = re.sub("(<b>)(.*?)(</b>)", "**\g<2>**", text)
        text = re.sub("(<i>)(.*?)(</i>)", "_\g<2>_", text)
        return text

    def footer_line(self):
        """
        This constructs the footer which contains faction membership, cycle
        membership and position, cycle rotations, and the latest MWL entry.

        Example:

        `Mage • Spell • TGT`
        """

        parts = [self.type.title(), self.card_class.title(), self.rarity.title(), self.set.title()]
        footer = ' • '.join(parts)
        return footer

    def render(self):
        """
        Builds and returns self.embed.

        A call to self.embed.render() will serialize all of the content
        into a dict suitable to sending to Discord's API.
        """
        self.embed.add_field(
            name=self.type_line(),
            value=self.text_line(),
        )
        self.embed.colour = Colour.green()
        self.embed.set_thumbnail(url=self.image(self.id))
        self.embed.set_footer(text=self.footer_line())
        return self.embed

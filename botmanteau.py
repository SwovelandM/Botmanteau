#botmanteau v1.1 - a moderately annoying discord bot that creates portmanteaus out of user's messages

import discord
from random import randint
from BotToken import BotToken

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def is_vowel(char: str) -> bool:
    return char.lower() in ('a', 'e', 'i', 'o', 'u', 'y')


#make a portmanteau o3o
def portmanteau(word: str, next_word: str) -> str:
    newWord: str = ""
    
    #append first word
    for letter in word:
        if is_vowel(letter):
            break
        
        else:
            newWord += letter
            
    #append second word
    secondPartIdx: int = 0
    for letter in next_word:
        if not is_vowel(letter):
            secondPartIdx += 1
            continue
        
        elif is_vowel(letter):
            newWord += next_word[secondPartIdx:]
            return newWord
        
        
#garbage function lmao 
def canBePortmanteaued(word: str, next_word: str) -> bool:
    return      len(word) >= 2 \
            and len(next_word) >= 2 \
            and not is_vowel(next_word[0]) \
            and not is_vowel(word[0]) \
            and word != next_word \
            and word[0] != next_word[0]


@client.event
async def on_ready():
    print("Botmanteau V1.1 Online")


prevWords = []

@client.event
async def on_message(message: discord.Message = ""):
    try:
        print(f"message: {message.content}")
        words = message.content
        
        #clean up the message
        words = words.replace('\"','')
        words = words.replace(',','')
        words = words.replace('.','')
        words = words.replace('/','')
        words = words.replace('\\','')
        words = words.replace('!','')
        words = words.replace('@','')
        words = words.replace('#','')
        words = words.replace('$','')
        words = words.replace('%','')
        words = words.replace('^','')
        words = words.replace('&','')
        words = words.replace('*','')
        words = words.replace('(','')
        words = words.replace(')','')
        words = words.replace('[','')
        words = words.replace(']','')
        words = words.replace('\[','')
        words = words.replace('\]','')
        words = words.replace('\n','')
        
        words = words.strip().split()
        
        #remove "and" and "the" such as in the case of "pepsi and milk" or "milk the pepsi"
        newWords = []
        if len(words) >= 4:
            return
        
        elif len(words) == 3:
            newWords = [word.lower() for word in words if word != "and" and word != "the"]
            if len(newWords) >= 3:
                return
            
        else:
            newWords = [word.lower() for word in words]
        
        words = newWords
        
        global prevWords
        for word in prevWords:
            if word in words:
                return

        #save current words as to not reply to the bots' own messages
        prevWords = [word for word in words]
        
        #parse through words in cleaned up message;
        #portmanteau if possible
        for idx in range(len(words)):
            try:
                #special case
                if words[idx].lower() == "banana" and words[idx + 1].lower() == "burger":
                    reply_msg = "banurger"
                    await message.reply(reply_msg)
                    return
                
                if canBePortmanteaued(words[idx], words[idx+1]):
                    reply_msg = words[idx] + " + " + words[idx + 1] + ": " + portmanteau(words[idx], words[idx+1])
                    await message.reply(reply_msg.lower())
                    return
            
            except IndexError:
                return
            
    except Exception as e:
        print(e)
        return
        
client.run(BotToken.KEY)